from __doccli_old.modules.main_module_old import m_welcome
from requests import get
from termcolor import colored
import threading
from __doccli_old.apis.discord_old import start_rpc, set_running

VERSION = "v2.10"

def check_update() -> None:

    response = get(
        "https://api.github.com/repos/TowarzyszFatCat/doccli/releases/latest"
    )

    if response.json()["name"] != VERSION:

        print(colored("Wersja programu:", "white"), colored(VERSION, "red"))
        print(colored('Najnowsza wersja:', "white"), colored(f"{response.json()['name']}", "green"))
        print('')
        print(colored("Dostępna jest nowa wersja __doccli_old!", "white"))
        print('')
        input(colored("Naciśnij enter by pominąć...", "yellow"))


if __name__ == "__main__":
    check_update()
    set_running(True)
    thread = threading.Thread(target=start_rpc)
    thread.start()
    m_welcome()

