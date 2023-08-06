import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="picsellia",
    version="5.1.21-rc0",
    author="Pierre-Nicolas Tiffreau CTO @ Picsell.ia",
    author_email="pierre-nicolas@picsellia.com",
    description="Python SDK training module for Picsell.ia",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://www.picsellia.com',
    keywords=['SDK', 'Picsell.ia', 'Computer Vision', 'Deep Learning'],
    packages=setuptools.find_packages(),
    install_requires=[
        "Pillow>=8.0, <=8.4",
        "requests==2.27.1",
        "beartype==0.9.1",
        "tqdm==4.62.2",
        "rich==11.2.0",
        "pydantic==1.9.0",
        "picsellia-connexion-services==0.0.11"
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.8'
    ],
    package_data={
        "": ["conf/default_logging.conf"],
    },
    python_requires='>=3.6.9',
)
