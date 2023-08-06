
from functools import partial
import json
import logging
import os
from typing import List
from beartype import beartype

from picsellia.decorators import exception_handler
from picsellia import exceptions
from picsellia.bcolors import bcolors
import warnings
from beartype.roar import BeartypeDecorHintPep585DeprecationWarning
warnings.filterwarnings("ignore", category=BeartypeDecorHintPep585DeprecationWarning)
from picsellia.utils import generate_requirements_json, is_uuid
from picsellia.types.schemas import ProjectSchema
from picsellia.sdk.connexion import Connexion
from picsellia.sdk.dao import Dao
from picsellia.sdk.dataset import Dataset
from picsellia.sdk.experiment import Experiment
from picsellia.sdk.model import Model
from picsellia.sdk.scan import Scan
from picsellia.sdk.worker import Worker

logger = logging.getLogger('picsellia')


class Project(Dao):

    def __init__(self, connexion: Connexion, data: dict):
        project = ProjectSchema(**data)
        super().__init__(connexion, project.id)
        self._name = project.name

    @property
    def name(self) -> str:
        return self._name

    def __str__(self,): return "{}Project '{}' {} (id: {})".format(bcolors.BOLD, self.name, bcolors.ENDC, self.id)

    @exception_handler
    @beartype
    def get_resource_url_on_platform(self,) -> str:
        """Get platform url of this resource.

        Examples:
            ```python
                print(foo_dataset.get_resource_url_on_platform())
                >>> https://app.picsellia.com/project/62cffb84-b92c-450c-bc37-8c4dd4d0f590
            ```

        Returns:
            Url on Platform for this resource
        """

        return "{}/project/{}".format(self.connexion.host, self.id)

    @exception_handler
    @beartype
    def list_experiments(self) -> List[Experiment]:
        """List all project's experiments

        Examples:
            ```python
                experiments = my_project.list_experiments()
            ```

        Returns:
            A list of (Experiment) objects, that you can manipulate
        """
        experiments_response = self.connexion.get(
            '/sdk/v1/project/{}/experiments'.format(self.id)).json()
        return list(map(partial(Experiment, self.connexion), experiments_response["experiments"]))

    @exception_handler
    @beartype
    def delete_all_experiments(self,) -> None:
        """Delete all experiments of this project

        :warning: **DANGER ZONE**: Be very careful here!

        Examples:
            ```python
                my_project.delete_all_experiments()
            ```
        """
        self.connexion.delete('/sdk/v1/project/{}/experiments'.format(self.id))
        logger.info("All experiment of project {} deleted.".format(self.name))

    @exception_handler
    @beartype
    def create_experiment(self, name: str = None, description: str = '', previous: Experiment = None,
                          dataset: Dataset = None, source: Model = None, with_artifacts: bool = False,
                          with_logs: bool = False) -> Experiment:
        """Create an experiment in this project.

        You have the same options as when creating experiments from the UI.
            - You can attach a dataset
            - You can fork a Model (it will automatically attach its files and parameters
                to the experiment)
            - You can start from a previous experiment (it will automatically attach its files and parameters
                to the new experiment)

        Examples:
            ```python
                dataset = client.get_dataset("COCO", "first_version")
                base_model = client.get_model("picsellia/yolov5")
                my_experiment = my_project.create_experiment(
                    name="new_experiment",
                    dataset=dataset,
                    source=base_model,
                )
            ```
        Arguments:
            name (str, optional): Name of experiment. Defaults to None.
            description (str, optional): Description of experiment. Defaults to ''.
            previous ((Experiment), optional): Previous experiment, if you want to base the new one on it.
                                             Defaults to None.
            dataset ((Dataset), optional): Dataset to attach. Defaults to None.
            source ((Model), optional): Model to use as source. Defaults to None.
            with_artifacts (bool, optional): Set true if you want to add files from the previous experiment.
                                             Defaults to False.
            with_logs (bool, optional): Set true if you want to add datas from the previous experiment.
                                        Defaults to False.

        Returns:
             A new (Experiment) of this project
        """
        data = ({
            "name": name,
            "description": description,
            "previous": previous.id if previous else None,
            "dataset": dataset.id if dataset else None,
            "source": source.id if source else None,
            "with_artifacts": with_artifacts,
            "with_logs": with_logs
        })
        # Filter None values
        filtered = {k:v for k,v in data.items() if v is not None}
        experiment_response = self.connexion.post(
            '/sdk/v1/project/{}/experiment'.format(self.id), data=json.dumps(filtered)).json()
        logger.info("Experiment {} created".format(name))
        return Experiment(self.connexion, experiment_response["experiment"])

    @exception_handler
    @beartype
    def update(self, **kwargs) -> None:
        """Update a project

        Examples:
            ```python
                my_project.update(description="This is a cool project")
            ```
        """
        self.connexion.patch('/sdk/v1/project/{}'.format(self.id), data=json.dumps(kwargs)).json()
        logger.info("Project {} updated.".format(self.name))

    @exception_handler
    @beartype
    def delete(self,) -> None:
        """Delete a project.

        :warning: **DANGER ZONE**: Be very careful here!

        It will delete the project and all experiments linked.

        Examples:
            ```python
                my_project.delete()
            ```
        """
        self.connexion.delete('/sdk/v1/project/{}'.format(self.id))
        logger.info("Project {} deleted.".format(self.name))

    @exception_handler
    @beartype
    def get_experiment(self, name: str = None, id: str = None, tree: bool = False,
                       with_artifacts: bool = False, with_logs: bool = False) -> Experiment:
        """Retrieve an existing experiment.

        You can also to download attached files and setup according project folder tree.

        You must specify either the Experiment's name or its id.

        Examples:
            ```python
                my_experiment = my_project.get_experiment(name="test_experiment")
                my_experiment = my_project.get_experiment(id="superid", with_artifacts=True, with_logs=True)
            ```
        Arguments:
            name (str, optional): Experiment's name. Defaults to None.
            id (str, optional): Experiment's id. Defaults to None.
            tree (bool, optional): Whether to create folder tree or not. Defaults to False.
            with_artifacts (bool, optional): Whether to download every experiment's Artifacts or not. Defaults to False.
            with_logs (bool, optional): Whether to retrieve experiment's Logs or not. Defaults to False.

        Raises:
            Exception: Experiment not found

        Returns:
            An (Experiment) object that you can manipulate
        """
        identifier = None
        if id is not None:
            identifier = id
        elif name is not None:
            identifier = name
        else:
            raise exceptions.PicselliaError('No corresponding experiment found, please enter an experiment id or an experiment name')
        experiment = self._get_experiment(identifier=identifier, with_artifacts=with_artifacts, with_logs=with_logs)

        experiment.download_artifacts_and_prepare_tree(tree, with_artifacts)

        return experiment

    @exception_handler
    @beartype
    def _get_experiment(self, identifier: str,
                        with_artifacts: bool = False, with_logs: bool = False) -> Experiment:
        data = {
            'with_artifacts': with_artifacts,
            'with_logs': with_logs
        }
        if is_uuid(identifier):
            r = self.connexion.get(
                '/sdk/v1/experiment/{}'.format(identifier), data).json()
        else:
            r = self.connexion.get(
                '/sdk/v1/project/{}/experiment?name={}'.format(self.id, identifier), data).json()
        return Experiment(self.connexion, r["experiment"])

    @exception_handler
    @beartype
    def attach_dataset(self, dataset: Dataset) -> None:
        """Attach a dataset to this project.

        Retrieve or create a dataset and attach it to this project.

        Examples:
            ```python
                foo_dataset = client.create_dataset("foo", "first")
                my_project.attach_dataset(foo_dataset)
            ```
        Arguments:
            dataset (Dataset): A dataset to attach to the project.
        """
        self.connexion.post('/sdk/v1/project/{}/attach_dataset/{}'.format(self.id, dataset.id))
        logger.info("Dataset {}/{} successfully attached to project {}"
                    .format(dataset.name, dataset.version, self.name))

    @exception_handler
    @beartype
    def list_datasets(self,) -> List[Dataset]:
        """Retrieve all dataset attached to this project

        Examples:
            ```python
            datasets = my_project.list_datasets()
            ```

        Returns:
            A list of (Dataset) object attached to this project
        """
        r = self.connexion.get(
            '/sdk/v1/project/{}/datasets'.format(self.id)).json()
        return list(map(partial(Dataset, self.connexion), r["datasets"]))

    @exception_handler
    @beartype
    def list_workers(self,) -> List[Worker]:
        """List workers of this project.

        List all collaborators working on this project.

        Examples:
            ```python
                workers = my_project.list_workers()
                print([worker.get_infos() for worker in workers])
            ```

        Returns:
            A list of (Worker) that you can manipulate :woman_technologist: :man_technologist:
        """
        r = self.connexion.get('/sdk/v1/project/{}/workers'.format(self.id)).json()
        return list(map(partial(Worker, self.connexion), r["workers"]))


    @exception_handler
    @beartype
    def create_scan(self, name: str, config: dict, nb_worker: int = 1) -> Scan:
        """Initialize a new scan.

        See full documentation https://docs.picsellia.com/experiments/hyperparameter-tuning/config

        Arguments:
            name (str): Scan's name
            config (dict): config dictionnary
            nb_worker (int, optional): Number of worker to instantiate (if running remote). Defaults to 1.

        Returns:
            A (Scan) object that you can manipulate
        """
        if "script" in config.keys():
            path = config["script"]
            filename = os.path.split(path)[-1]
            object_name = os.path.join(self.id, filename)
            response = self.connexion.upload_file(path, object_name)
        else:
            object_name = None
            filename = None

        if "requirements" in config.keys():
            requirements = config["requirements"]
            if isinstance(requirements, str):
                j = generate_requirements_json(requirements)
                config["requirements"] = j["requirements"]

            elif isinstance(requirements, list):
                for e in requirements:
                    assert isinstance(
                        e, dict), "Requirements must be a list of dict"
                    assert "package" in e.keys(), "The dictionnaries must contain the key package"
                    assert "version" in e.keys(), "The dictionnaries must contain the key version"

            else:
                raise exceptions.InvalidQueryError(
                    "Please remove the key requirements from config dict if you don't want to specify any requirements")
        
        if "data" in config:
            data_list = config["data"]
            files = []
            assert isinstance(data_list, list), "data must be a list of filenames"

            for path in data_list:
                fname = os.path.split(path)[-1]
                object_name = os.path.join(self.id, fname)
                response = self.connexion.upload_file(path, object_name)
                if response.status_code == 204:
                    files.append({"filename": fname, "object_name": object_name})
        
            config["data"] = files

        data = {
            "name": name,
            "config": config,
            "nb_worker": nb_worker,
        }
        if filename != None:
            data["filename"] = filename

        if object_name != None:
            data["object_name"] = object_name

        r = self.connexion.post(
            '/sdk/v1/project/{}/scan'.format(self.id), data=json.dumps(data)).json()
        return Scan(self.connexion, r["scan"])
