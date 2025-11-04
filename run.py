import time

from main_module import m_welcome
from requests import get
from termcolor import colored
import threading
from discord_integration import start_rpc, set_running

from docchi_api_connector import get_skip_times

VERSION = "v2.12"

def check_update() -> None:

    response = get(
        "https://api.github.com/repos/TowarzyszFatCat/doccli/releases/latest"
    )

    if response.json()["name"] != VERSION:

        print(colored("Wersja programu:", "white"), colored(VERSION, "red"))
        print(colored('Najnowsza wersja:', "white"), colored(f"{response.json()['name']}", "green"))
        print('')
        print(colored("Dostępna jest nowa wersja doccli!", "white"))
        print('')
        input(colored("Naciśnij enter by pominąć...", "yellow"))


if __name__ == "__main__":
    check_update()
    set_running(True)
    thread = threading.Thread(target=start_rpc)
    thread.start()
    m_welcome()

