from os import path, remove
import json
import modules.global_variables_module as gvm


# Default configuration settings
default_config = {
    "config_version": None,
    "dc_status": "TAK",
    "search_lang": "ORYGINALNY",
    "last_url": None,
    "last_info": None,
    "last_ep": None,
    "quality": "NAJLEPSZA",
}


def load_config():
    if not path.exists(gvm.CONFIG_PATH):
        with open(gvm.CONFIG_PATH, "w") as f:
            default_config.update({"config_version": gvm.VERSION})
            json.dump(default_config, f)
            f.close()

    with open(gvm.CONFIG_PATH, "r") as f:
        readed = json.load(f)

        if readed["config_version"] != gvm.VERSION:
            print("[INFO] Wykryto config ze starej wersji! Podmienianie...")
            f.close()
            remove(gvm.CONFIG_PATH)
            load_config()
        else:
            gvm.config = readed
            f.close()


def update_config(var, value):
    gvm.config.update({f"{var}": value})


def save_config():
    with open(gvm.CONFIG_PATH, "w") as f:
        json.dump(gvm.config, f)
        f.close()

    load_config()

