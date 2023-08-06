import logging
import os
import random
import uuid
import warnings
import zipfile

from beartype import beartype
from beartype.roar import BeartypeDecorHintPep585DeprecationWarning

from picsellia import exceptions as exceptions
from picsellia.bcolors import bcolors

warnings.filterwarnings("ignore", category=BeartypeDecorHintPep585DeprecationWarning)
import sys

from picsellia.decorators import exception_handler

logger = logging.getLogger('picsellia')

try:
    download_bar_mode = os.environ["PICSELLIA_SDK_DOWNLOAD_BAR_MODE"]
except KeyError:
    download_bar_mode = "1"

try:
    print_section_handler = os.environ["PICSELLIA_SDK_SECTION_HANDLER"]
except KeyError:
    print_section_handler = "0"

@exception_handler
@beartype
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

@exception_handler
@beartype
def train_valid_split_obj_simple(dict_annotations, prop=0.8):
    """Perform Optimized train test split for Object Detection.
       Uses optimization to find the optimal split to have the desired repartition of instances by set.
    Arguments:
        prop (float) : Percentage of Instances used for training.
        dict_annotations (dict) : annotation from dl_annotations

    Raises:
        ResourceNotFoundError: If not annotations in the Picsell.ia Client yet."""

    if dict_annotations is None:
        raise exceptions.ResourceNotFoundError("No dict_annotations passed")

    list_im = [i for i in range(len(dict_annotations['images']))]
    random.shuffle(list_im)
    nb_im = int(prop * len(dict_annotations['images']))
    train_list = list_im[:nb_im]
    test_list = list_im[nb_im:]
    index_url = []
    for e in range(len(list_im)):
        if e in train_list:
            index_url.append(1)
        elif e in test_list:
            index_url.append(0)
    return index_url


@exception_handler
@beartype
def get_labels_repartition_obj_detection(dict_annotations, index_url):
    """Perform train test split scanning for Object Detection.
    Returns:
        cate (array[str]) : Array of the classes names
        cnt_train (array[int]) : Array of the number of object per class for the training set.
        cnt_eval (array[int]) : Array of the number of object per class for the evaluation set.

    Raises:
        ResourceNotFoundError: If not annotations in the Picsell.ia Client yet."""

    if dict_annotations is None:
        raise exceptions.ResourceNotFoundError("No dict_annotations passed")

    cate = [v["name"] for v in dict_annotations["categories"]]
    cnt_train = [0] * len(cate)
    cnt_eval = [0] * len(cate)

    for img, index in zip(dict_annotations['images'], index_url):
        internal_picture_id = img["internal_picture_id"]
        for ann in dict_annotations["annotations"]:
            if internal_picture_id == ann["internal_picture_id"]:
                for an in ann['annotations']:
                    try:
                        idx = cate.index(an['label'])
                        if index == 1:
                            cnt_train[int(idx)] += 1
                        else:
                            cnt_eval[int(idx)] += 1
                    except Exception:
                        pass
    return cnt_train, cnt_eval, cate


@exception_handler
@beartype
def zipdir(path):
    zipf = zipfile.ZipFile(path.split('.')[0] + '.zip', 'w', zipfile.ZIP_DEFLATED)
    for filepath in os.listdir(path):
        zipf.write(os.path.join(path, filepath), filepath)

        if os.path.isdir(os.path.join(path, filepath)):
            for fffpath in os.listdir(os.path.join(path, filepath)):
                zipf.write(os.path.join(path, filepath, fffpath), os.path.join(filepath, fffpath))

    zipf.close()
    return path.split('.')[0] + '.zip'


@exception_handler
@beartype
def is_uuid(string):
    try:
        uid = uuid.UUID(string, version=4)
        return str(uid) == string
    except Exception:
        return False

# No exception handling: exception needs to be raised
def check_status_code(response):
    status = int(response.status_code)
    if status in [200, 201, 202, 203]:
        try:
            response_data = response.json()
            if "success" in response_data:
                logger.debug(response_data["success"])
            if "unknown" in response_data:
                logger.warning("Some data could not be used {}".format(response_data["unknown"]))
        except Exception as e:
            logger.debug('Platform has returned (status code {}) : {}'.format(response.status_code, response.text))
        return
    elif status == 204:
        logger.debug('Resource deleted.')
        return
    elif status in [208, 400, 401, 402, 403, 404, 409, 500]:
        try:
            response_data = response.json()
            if "error" in response_data:
                message = response_data["error"]
            elif "message" in response_data:
                message = response_data["message"]
            else:
                message = response.url
        except Exception as e:
            message = ""
            logger.warning('Platform has returned (status code {}) : {}'.format(response.status_code, response.text))
        
        if status == 208:
            raise exceptions.PicselliaError("An object has already this name in S3.")
        if status == 400:
            raise exceptions.InvalidQueryError("Invalid query : {}".format(message))
        if status == 401:
            raise exceptions.UnauthorizedError("Unauthorized : {}".format(message))
        if status == 402:
            raise exceptions.UnsufficientRessourcesError("{}".format(message))
        if status == 403:
            raise exceptions.ForbiddenError("Forbidden : {}".format(message))
        if status == 404:
            raise exceptions.ResourceNotFoundError("Resource not found: {}".format(message))
        if status == 409:
            raise exceptions.ResourceConflictError("This resouce already exists : {}".format(message))
        if status == 500:
            raise exceptions.PicselliaError("Internal server error. Please contact support. {}".format(message))
    else:
        raise Exception("Unknown error (Status code : {}), please contact support".format(status))


@exception_handler
@beartype
def generate_requirements_json(requirements_path: str):
    """Generate a json file with the requirements from the requirements.txt file

    Arguments:
        requirements_path ([str]): [absolute path to requirements.txt file]

    Raises:
        exceptions.ResourceNotFoundError: [Filepath does match]
        Exception: [Wrong requirements file]

    Returns:
        [dict]: {
            'requirements': []{
                'package': (str) package name,
                'version': (str) package version
            }
        }
    """
    js = {"requirements": []}
    try:
        with open(requirements_path, 'r') as f:
            lines = f.readlines()
    except Exception:
        raise exceptions.ResourceNotFoundError("{} does not exists".format(requirements_path))
    try:
        for line in lines:
            if line[0] != "#":
                try:
                    package, version = line.split("==")
                except Exception:
                    package, version = line, ""
                tmp = {
                    "package": package.rstrip(),
                    "version": version.rstrip()
                }
                js["requirements"].append(tmp)
    except Exception:  # pragma: no cover
        raise Exception("Malformed requirements file")
    return js

def print_line_return():
    sys.stdout.write("\n")

def print_start_section():
    if print_section_handler == "1":
        sys.stdout.write("-----")

def print_stop_section():
    if print_section_handler == "1":
        sys.stdout.write("--*--")

def print_start_chapter_name(name: str):
    if print_section_handler == "1":
        sys.stdout.write("--#--{}".format(name))

def print_logging_buffer(length: int):
    if print_section_handler == "1":
        sys.stdout.write('--{}--'.format(length))
