from os import path

VERSION: str = "v1.4"
config = {}

ROOT_DIR = path.dirname(path.abspath('doccli.py'))
CONFIG_PATH = path.join(ROOT_DIR, "doccli.config")
