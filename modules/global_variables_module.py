from os import path

VERSION: str = "v2.0"
config = {}

ROOT_DIR = path.dirname(path.abspath('doccli.py'))
CONFIG_PATH = path.join(ROOT_DIR, "doccli.config")
