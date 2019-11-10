import pathlib
import pytoml as toml
import os


BASE_DIR = pathlib.Path(__file__).parent.parent
PACKAGE_NAME = 'app'


def load_config(path):
    print(os.getcwd())
    with open(path) as f:
        conf = toml.load(f)
    return conf

