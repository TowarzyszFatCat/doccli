# @TowarzyszFatCat
# v1.4

from requests import get
from os import system
from os import name as system_name
from time import sleep, time
from subprocess import Popen, DEVNULL
from typing import List
from InquirerPy import inquirer

from modules.url_module import get_all_formats
from modules.discord_module import connect_discord, update_discord
from modules.update_checker import check_update
from modules.config_module import load_config, update_config, save_config

import modules.global_variables_module as gvm


# Function to retrieve list of available players
def get_players_list(slug: str, ep: int) -> list:
    players_list: list = get(
        f"https://api.docchi.pl/v1/episodes/find/{slug}/{ep}"
    ).json()

    all_aviable_players: list = []

    for player in players_list:
        player_data: List[str] = []

        supported = ["cda", "Cda", "CDA"]

        if player["player_hosting"] in supported:
            player_data.append(player["player_hosting"])
        else:
            player_data.append(player["player_hosting"] + " [NIEWSPIERANY]")

        player_data.append(player["player"])

        all_aviable_players.append(player_data)

    # Return format: [('hosting name', 'player link'), ... ]
    return all_aviable_players


# Function to let user choose an episode
def choose_ep(serie: list) -> int:
    _ep: List[str] = []

    for i in range(int(serie["episodes"])):
        _ep.append(str(i + 1))

    choosed: int = int(_ep.index(open_menu(_ep, "WYBIERZ ODCINEK:"))) + 1

    return choosed


# Function to let user choose a player
def choose_player(players) -> str:
    number: int = 0

    _players: List[str] = []

    for player in players:
        number += 1
        _players.append(f"{number}. {player[0]}")

    choosed = _players.index(open_menu(_players, "WYBIERZ HOSTA:"))

    choosed_player: str = players[choosed]
    return choosed_player[1]


# Function to clear CLI screen
def clear() -> None:
    system("cls" if system_name == "nt" else "clear")


# Function to handle Discord connection query
def connect_to_discord_querry() -> None:
    querry: str = open_menu(
        ["TAK", "NIE"],
        "Czy chcesz aby twoi znajomi z discorda widzieli co oglądasz?",
    )

    if querry == "TAK":
        update_config("dc_status", "TAK")
        save_config()
    elif querry == "NIE":
        update_config("dc_status", "NIE")
        save_config()


# Function to change search language
def change_search_lang() -> None:
    querry: str = open_menu(
        ["ORYGINALNY", "ANGIELSKI"],
        "Chesz wyszukiwać po oryginalnym tytule, czy tytule angielskim?",
    )

    if querry == "ORYGINALNY":
        update_config("search_lang", "ORYGINALNY")
        save_config()
    elif querry == "ANGIELSKI":
        update_config("search_lang", "ANGIELSKI")
        save_config()


# Function to execute fuzzy finding
def open_menu(choices: List[str], title: str = "") -> str:
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


# Function to retrieve information about all series
def all_series() -> dict:
    all_series_list: list = get(f"https://api.docchi.pl/v1/series/list").json()

    _all_series: list = []

    for serie in all_series_list:
        if gvm.config["search_lang"] == "ORYGINALNY":
            _all_series.append(f"{serie['title']} [{serie['episodes']}]")
        elif gvm.config["search_lang"] == "ANGIELSKI":
            _all_series.append(f"{serie['title_en']}, [{serie['episodes']}]")

    choosed: int = _all_series.index(open_menu(_all_series, "WYSZUKAJ ANIME:"))

    serie: dict = all_series_list[choosed]

    return serie


# Function to search for an anime
def search_for_anime(serie=None, ep=None, players=None) -> List[any]:
    if serie == None:
        serie: dict = all_series()

    if ep == None:
        ep: int = choose_ep(serie=serie)

    players: list = get_players_list(slug=serie["slug"], ep=ep)

    return [choose_player(players=players), serie, ep]


# Function to open MPV player
def open_mpv(URL):

    player = "vlc path" if system_name == "nt" else "mpv"

    try:
        process: Popen = Popen(
            args=[player, URL], shell=False, stdout=DEVNULL, stderr=DEVNULL
        )
    except:
        print(f"[ERROR] Upewnij się że {player} jest zainstalowane w domyślnej ścieżce!")
        exit()

    return process


# Function to let user choose video quality
def choose_quality() -> None:
    quality_list: List[str] = ["NAJLEPSZA", "NAJSZYBSZA", "POZWÓL MI WYBRAĆ ZA KAŻDYM RAZEM"]
    quality_choose: str = open_menu(quality_list, "WYBIERZ JAKOŚĆ: ")
    if quality_choose == quality_list[0]:
        update_config("quality", "NAJLEPSZA")
        save_config()
    elif quality_choose == quality_list[1]:
        update_config("quality", "NAJSZYBSZA")
        save_config()
    elif quality_choose == quality_list[2]:
        update_config("quality", "WYBÓR")
        save_config()


# Function to watch anime
def watch(serie=None, ep=None, cont=False, change_quality=False):
    if cont == True:
        if gvm.config["last_url"] == None:
            print("[BŁĄD] Nie możesz kontynuować niczego")
            exit()
        anime = [gvm.config["last_url"], gvm.config["last_info"], gvm.config["last_ep"]]
    else:
        anime = search_for_anime(serie, ep)
        update_config("last_url", anime[0])
        update_config("last_info", anime[1])
        update_config("last_ep", anime[2])
        save_config()

    aviable_formats = get_all_formats(anime[0])

    mpv_url = ''


    if gvm.config['quality'] == "WYBÓR" or change_quality:
        choosed = choose_format(aviable_formats)
        mpv_url = choosed[1]
    elif gvm.config["quality"] == "NAJLEPSZA":
        mpv_url = aviable_formats[-1][1]   # Url from last item from list
    elif gvm.config["quality"] == "NAJSZYBSZA":
        mpv_url = aviable_formats[0][1]   # Url from last item from list

    process = open_mpv(URL=mpv_url)

    try:
        if gvm.config["dc_status"] == "TAK":
            update_discord(
                state=f"Ep: {anime[2]}", details=anime[1]["title"], time=time()
            )
        elif gvm.config["dc_status"] == "NIE":
            update_discord(state=f"Tajne!", details="Ogląda anime...", time=time())
    except:
        pass

    info = [anime, process]
    watching_menu(info=info)


def choose_format(formats):
    ids = []
    for format in formats:
        ids.append(f"{format[0]}")

    format_choose = open_menu(ids, "WYBIERZ JAKOŚĆ: ")

    return formats[ids.index(format_choose)]

# Function for main menu
def main_menu() -> None:
    try:
        update_discord(state="Używa doccli!", details="Menu główne", time=time())
    except:
        pass

    try:
        if gvm.config["search_lang"] == "ORYGINALNY":
            continue_title = gvm.config["last_info"]["title"]
        elif gvm.config["search_lang"] == "ANGIELSKI":
            continue_title = gvm.config["last_info"]["title_en"]
        continue_ep = gvm.config["last_ep"]
    except:
        continue_title = None
        continue_ep = None

    tabs: List[str] = [
        "Wyszukaj anime",
        f"Kontynuuj: {continue_title} [Ep: {continue_ep}]",
        f'Status aktywności: {gvm.config["dc_status"]}',
        f'Język tytułów: {gvm.config["search_lang"]}',
        f'Domyślna jakość: {gvm.config["quality"]}',
        "Zamknij",
    ]

    option = open_menu(tabs, "WYBIERZ:")

    if option == tabs[0]:
        watch()

    elif option == tabs[1]:
        watch(cont=True)  # CONTINYUE

    elif option == tabs[2]:
        connect_to_discord_querry()
        main_menu()

    elif option == tabs[3]:
        change_search_lang()
        main_menu()

    elif option == tabs[4]:
        choose_quality()
        main_menu()

    elif option == tabs[5]:
        exit()



# Function for watching menu
def watching_menu(info) -> None:
    tabs: List[str] = [
        "Wróć do menu głównego",
        "Wróć do listy odcinków",
        'Zmień jakość',
    ]

    min_ep = 1
    actual_ep = int(info[0][2])
    max_ep = int(info[0][1]["episodes"])

    if actual_ep > min_ep:
        tabs.append("Poprzedni odcinek")

    if actual_ep < max_ep:
        tabs.append("Następny odcinek")

    option: str = open_menu(tabs, "WYBIERZ:")

    if option == tabs[0]:
        info[1].kill()
        main_menu()

    if option == tabs[1]:
        info[1].kill()
        watch(serie=info[0][1])

    if option == tabs[2]:
        info[1].kill()
        watch(cont=True, change_quality=True)

    if option == "Poprzedni odcinek":
        info[1].kill()
        watch(serie=info[0][1], ep=str(actual_ep - 1))

    if option == "Następny odcinek":
        info[1].kill()
        watch(serie=info[0][1], ep=str(actual_ep + 1))


# Start!
if __name__ == "__main__":
    check_update()
    load_config()
    connect_discord()
    main_menu()
