from InquirerPy import inquirer
from os import system, name as system_name

import logging
import modules.global_variables_module as gvm
logging.basicConfig(
    filename=gvm.LOG_PATH, filemode="w", format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO
    )


def clear() -> None:

    logging.info(msg="Czyszczenie terminalu...")

    system("cls" if system_name == "nt" else "clear")


def open_menu(choices, title: str = "") -> str:

    logging.info(msg=f"Otwieranie menu z tytulem: {title}")

    clear()
    action = inquirer.fuzzy(
        message=title,
        choices=choices,
        border=True,
        qmark='',
        amark='',
        prompt='Szukaj:',
        pointer='>',
        cycle=True,
        height=10,
    ).execute()
    return choices[choices.index(action)]
