from os import path, name as system_name, environ

VERSION: str = "v2.2"
config: dict = {}

ROOT_DIR = environ['USERPROFILE'] if system_name == "nt" else environ['HOME']

CONFIG_PATH = path.join(ROOT_DIR, "doccli.config")
LOG_PATH = path.join(ROOT_DIR, "doccli.log")
