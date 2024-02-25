from InquirerPy import inquirer
from os import system, name as system_name

def clear() -> None:
    system("cls" if system_name == "nt" else "clear")


def open_menu(choices, title: str = "") -> str:
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