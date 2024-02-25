# @TowarzyszFatCat
# v1.4

# Import necessary libraries
from requests import get
from os import system, getpid, path, remove
from os import name as system_name
from time import sleep, time
from subprocess import Popen, DEVNULL, run, PIPE
from pypresence import Presence
from typing import List
import json
from yt_dlp import YoutubeDL
from InquirerPy import inquirer


# GLOBAL VARIABLES
# Initialize Discord RPC
RPC = Presence(client_id="1206583480771936318")
version: str = "v1.4"

# Set up file paths
ROOT_DIR = path.dirname(path.abspath(__file__))
CONFIG_PATH = path.join(ROOT_DIR, "doccli.config")

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

config = {}


# Function to connect to Discord
def connect_discord() -> None:
    try:
        print(
            "[INFO] Łączenie z discordem... Jeżeli zajmuje to zbyt długo, możesz anulować łączenie za pomocą <CTRL C>"
        )
        RPC.connect()
        RPC.clear(getpid())
    except:
        print("[ERROR] Błąd podczas łączenia z discordem!")


# Function to retrieve list of available players
def get_players_list(slug: str, ep: int) -> list:
    players_list: list = get(
        f"https://api.docchi.pl/v1/episodes/find/{slug}/{ep}"
    ).json()

    all_aviable_players: list = []

    for player in players_list:
        player_data: List[str] = []

        unsupported = ["Mega", "mega", "MEGA", "zoro", "Zoro", "ZORO", 'GOOGLE DRIVE']

        if player["player_hosting"] in unsupported:
            player_data.append(player["player_hosting"] + " [NIEWSPIERANY]")
        else:
            player_data.append(player["player_hosting"])

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


# Function to update Discord presence
def update_discord(state: str, details: str, time: time) -> None:
    RPC.update(
        state=f"{state}",
        details=f"{details}",
        large_image="icon_1",
        large_text="CLI do oglądania anime z docchi.pl",
        start=int(time),
        buttons=[
            {
                "label": "Pobierz doccli",
                "url": "https://github.com/TowarzyszFatCat/doccli",
            },
            {
                "label": "Odwiedź docchi.pl",
                "url": "https://docchi.pl/",
            },
        ],
    )


# Function to check for program updates
def check_update() -> None:
    response = get(
        "https://api.github.com/repos/TowarzyszFatCat/doccli/releases/latest"
    )

    if response.json()["name"] != version:
        print(f"Wersja programu: {version}")
        print(f'Dostępna jest nowa: {response.json()["name"]}')
        print(f"Możesz pobrać nową wersję na stronie programu!\n")
        input("Naciśnij enter by pominąć...")


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
        cycle=True,
        height=10,
    ).execute()
    return choices[choices.index(action)]


# Function to retrieve information about all series
def all_series() -> dict:
    all_series_list: list = get(f"https://api.docchi.pl/v1/series/list").json()

    _all_series: list = []

    for serie in all_series_list:
        if config["search_lang"] == "ORYGINALNY":
            _all_series.append(f"{serie['title']} [{serie['episodes']}]")
        elif config["search_lang"] == "ANGIELSKI":
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
    try:
        process: Popen = Popen(
            args=["mpv", URL], shell=False, stdout=DEVNULL, stderr=DEVNULL
        )
    except:
        print("[ERROR] Błąd podczas uruchamiania MPV!")
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
        if config["last_url"] == None:
            print("[BŁĄD] Nie możesz kontynuować niczego")
            exit()
        anime = [config["last_url"], config["last_info"], config["last_ep"]]
    else:
        anime = search_for_anime(serie, ep)
        update_config("last_url", anime[0])
        update_config("last_info", anime[1])
        update_config("last_ep", anime[2])
        save_config()

    aviable_formats = get_all_formats(anime[0])

    mpv_url = ''


    if config['quality'] == "WYBÓR" or change_quality:
        choosed = choose_format(aviable_formats)
        mpv_url = choosed[1]
    elif config["quality"] == "NAJLEPSZA":
        mpv_url = aviable_formats[-1][1]   # Url from last item from list
    elif config["quality"] == "NAJSZYBSZA":
        mpv_url = aviable_formats[0][1]   # Url from last item from list

    process = open_mpv(URL=mpv_url)

    try:
        if config["dc_status"] == "TAK":
            update_discord(
                state=f"Ep: {anime[2]}", details=anime[1]["title"], time=time()
            )
        elif config["dc_status"] == "NIE":
            update_discord(state=f"Tajne!", details="Ogląda anime...", time=time())
    except:
        pass

    info = [anime, process]
    watching_menu(info=info)


def get_all_formats(url):
    with YoutubeDL({'quiet': True}) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict['formats']

        aviable_formats = []


        # For CDA
        for format in formats:
            format_info = []

            try:
                format_info.append(format['height'])
                format_info.append(format['url'])
                aviable_formats.append(format_info)
            except:
                format_info.append('Nieznany format')
                format_info.append(format['url'])
                aviable_formats.append(format_info)

        return aviable_formats

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
        if config["search_lang"] == "ORYGINALNY":
            continue_title = config["last_info"]["title"]
        elif config["search_lang"] == "ANGIELSKI":
            continue_title = config["last_info"]["title_en"]
        continue_ep = config["last_ep"]
    except:
        continue_title = None
        continue_ep = None

    tabs: List[str] = [
        "Wyszukaj anime",
        f"Kontynuuj: {continue_title} [Ep: {continue_ep}]",
        f'Status aktywności: {config["dc_status"]}',
        f'Język tytułów: {config["search_lang"]}',
        f'Domyślna jakość: {config["quality"]}',
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


# Function to load configuration
def load_config():
    if not path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w") as f:
            default_config.update({"config_version": version})
            json.dump(default_config, f)
            f.close()

    with open(CONFIG_PATH, "r") as f:
        readed = json.load(f)

        if readed["config_version"] != version:
            print("[INFO] Wykryto config ze starej wersji! Podmienianie...")
            f.close()
            remove(CONFIG_PATH)
            load_config()
        else:
            global config
            config = readed
            f.close()

# Function to update configuration
def update_config(var, value):
    config.update({f"{var}": value})


# Function to save configuration
def save_config():
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f)
        f.close()

    load_config()


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
