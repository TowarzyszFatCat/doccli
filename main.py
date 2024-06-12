from menu_module import m_welcome
from requests import get
from termcolor import colored

VERSION = "v2.5.1"

def check_update() -> None:

    response = get(
        "https://api.github.com/repos/TowarzyszFatCat/doccli/releases/latest"
    )

    if response.json()["name"] != VERSION:

        print(colored("Wersja programu:", "white"), colored(VERSION, "red"))
        print(colored('Najnowsza wersja:', "white"), colored(f"{response.json()["name"]}", "green"))
        print('')
        print(colored("Dostępna jest nowa wersja doccli!", "white"))
        print('')
        input(colored("Naciśnij enter by pominąć...", "yellow"))


if __name__ == "__main__":
    check_update()
    m_welcome()
