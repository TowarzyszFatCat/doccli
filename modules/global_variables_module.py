from os import path, name as system_name, environ

VERSION: str = "v2.0"
config: dict = {}

ROOT_DIR = environ['HOME']

CONFIG_PATH = path.join(ROOT_DIR, "doccli.config")
LOG_PATH = path.join(ROOT_DIR, "doccli.log")
