from os import path, remove
import json
import modules.global_variables_module as gvm

import logging
logging.basicConfig(
    filename=gvm.LOG_PATH, filemode="w", format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO
    )

# Default configuration settings
default_config: dict = {
    "config_version": None,
    "dc_status": "TAK",
    "search_lang": "ORYGINALNY",
    "last_url": None,
    "last_info": None,
    "last_ep": None,
    "quality": "NAJLEPSZA",
}


def load_config() -> None:

    logging.info(msg="Ladowanie configu...")

    if not path.exists(gvm.CONFIG_PATH):

        logging.info(msg="Nie wykryto configu!")

        with open(gvm.CONFIG_PATH, "x") as f:

            logging.info(msg="Generowanie nowego configu!")

            default_config.update({"config_version": gvm.VERSION})
            json.dump(default_config, f)

            logging.info(msg=f"Nowy config: {default_config}")

            f.close()

    with open(gvm.CONFIG_PATH, "r") as f:

        logging.info(msg="Wykryto config!")

        readed = json.load(f)

        logging.info(msg=f"Wczytany config: {readed}")

        if readed["config_version"] != gvm.VERSION:

            logging.info(msg=f"Wykryto config ze starej wersji! V: {readed['config_version']}")

            f.close()

            logging.info(msg="Usuwanie przestarzalego configu!")

            remove(gvm.CONFIG_PATH)
            load_config()

        else:
            gvm.config = readed

            logging.info(msg=f"Wczytano nowy config: {readed}")

            f.close()


def update_config(var, value) -> None:

    gvm.config.update({f"{var}": value})

    logging.info(msg=f"Zaktualizowano zmienna w configu: '{var}': {value}")



def save_config() -> None:

    logging.info(msg=f"Zapisywanie configu...")

    with open(gvm.CONFIG_PATH, "w") as f:
        json.dump(gvm.config, f)

        logging.info(msg=f"Zapisany config: {gvm.config}")

        f.close()

    load_config()
