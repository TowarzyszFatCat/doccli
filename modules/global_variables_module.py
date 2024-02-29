from os import path, name as system_name, environ

VERSION: str = "v2.1"
config: dict = {}

ROOT_DIR = environ['USERPROFILE']

CONFIG_PATH = path.join(ROOT_DIR, "doccli.config")
LOG_PATH = path.join(ROOT_DIR, "doccli.log")
