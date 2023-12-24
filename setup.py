from os import path as os_path

from loguru import logger
from setuptools import find_packages
from setuptools import setup


def read_long_description():
    with open('README.md', 'r') as f:
        long_description = f.read()
    return long_description


def read_version():
    version_file = os_path.join(os_path.dirname(__file__), 'cadmus', 'version.py')
    with open(version_file) as file:
        exec(file.read())
    version = locals()['__version__']
    logger.debug(f"Building {PACKAGE_NAME} v{version}")
    return version


PACKAGE_NAME = 'zf-cadmus'
PACKAGE_VERSION = read_version()
AUTHOR_NAME = 'zeffmuks'
AUTHOR_EMAIL = 'zeffmuks@gmail.com'

setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    description='pd supercharges your development workflows',
    long_description=read_long_description(),  # This is the important part
    long_description_content_type='text/markdown',  # This tells PyPI the content is in Markdown
    install_requires=[
        "annotated-types",
        "anyio",
        "Authlib",
        "certifi",
        "cffi",
        "charset-normalizer",
        "cryptography",
        "distro",
        "h11",
        "httpcore",
        "httpx",
        "idna",
        "loguru",
        "openai",
        "pycparser",
        "pydantic",
        "pydantic_core",
        "requests",
        "sniffio",
        "tqdm",
        "typing_extensions",
        "urllib3",
        "validators",
        "weaviate-client"
    ],
    packages=find_packages(
        include=['cadmus', 'cadmus.*'],
        exclude=['venv', 'venv.*']
    )
)
