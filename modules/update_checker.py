from requests import get
from modules.global_variables_module import VERSION

import logging
logging.basicConfig(
    filename="doccli.log", filemode="w", format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO
    )


def check_update() -> None:

    logging.info(msg="Checking for updates...")

    response = get(
        "https://api.github.com/repos/TowarzyszFatCat/doccli/releases/latest"
    )

    logging.info(msg=f"Response: {response.json()['name']}")

    if response.json()["name"] != VERSION:

        logging.info(msg="Detected new app version!")

        print(f"Wersja programu: {VERSION}")
        print(f'Dostępna jest nowa: {response.json()["name"]}')
        print(f"Możesz pobrać nową wersję na stronie programu!\n")
        input("Naciśnij enter by pominąć...")
