# @TowarzyszFatCat
# v1.3.7

from requests import get
from os import system, getpid, path, remove
from os import name as system_name
from time import sleep, time
from subprocess import Popen, DEVNULL, run, PIPE
from pypresence import Presence
from typing import List
import json


# GLOBAL VARIABLES
# Client id from discord developer portal
RPC = Presence(client_id='1206583480771936318')
#dc_status : bool = True
version : str = 'v1.3.7'

default_config = {
    "config_version" : None,
    "dc_status" : "TAK",
    "search_lang": "ORYGINALNY",
    "last_url" : None,
    "last_info" : None,
    "last_ep" : None,
    "quality" : 'NAJLEPSZA'
}

config = {}


def connect_discord() -> None:
    try:
        print("[INFO] Łączenie z discordem... Jeżeli zajmuje to zbyt długo, możesz anulować łączenie za pomocą <CTRL C>")
        RPC.connect()
        RPC.clear(getpid())
    except:
        print("[ERROR] Błąd podczas łączenia z discordem!")


# Get list of all aviable players.
def get_players_list(slug : str, ep : int) -> list:
    players_list : list = get(f'https://api.docchi.pl/v1/episodes/find/{slug}/{ep}').json()
    
    all_aviable_players : list = []

    for player in players_list:

        player_data : List[str] = []

        unsupported = ["Mega", "mega", "MEGA"]

        if player['player_hosting'] in unsupported:
            player_data.append(player['player_hosting'] + " [NIEWSPIERANY]")
        else:
            player_data.append(player['player_hosting'])

        player_data.append(player['player'])

        all_aviable_players.append(player_data)

    # Return format: [('hosting name', 'player link'), ... ]
    return(all_aviable_players)

# Let someone choose episode.
def choose_ep(serie : list) -> int:

    _ep : List[str] = []

    for i in range(int(serie['episodes'])):
        _ep.append(str(i+1))

    choosed : int = int(_ep.index(fzf(_ep, '--header=WYBIERZ ODCINEK:')[0])) + 1

    return choosed
    

# Let someone choose player.
def choose_player(players) -> str:

    number : int = 0

    _players : List[str] = []

    for player in players:

        number += 1

        _players.append(f'{number}. {player[0]}')

    choosed = _players.index(fzf(_players, '--header=WYBIERZ HOSTA:')[0])

    choosed_player : str = players[choosed]
    return choosed_player[1]


# Clear cli
def clear() -> None:
    system('cls' if system_name == 'nt' else 'clear')


def update_discord(state : str, details : str, time : time) -> None:
    RPC.update(
        state=f"{state}",
        details=f"{details}",
        large_image="icon_1",
        large_text="CLI do oglądania anime z docchi.pl",
        start=int(time),
        buttons=[
            {
                "label": "Pobierz doccli",
                "url": "https://github.com/TowarzyszFatCat/doccli"
            },
            {
                     "label": "Odwiedź docchi.pl",
                     "url": "https://docchi.pl/",
            }
        ]
        )
    
def check_update() -> None:
    response = get("https://api.github.com/repos/TowarzyszFatCat/doccli/releases/latest")

    if response.json()["name"] != version:
        print(f'Wersja programu: {version}')
        print(f'Dostępna jest nowa: {response.json()["name"]}')
        print(f'Możesz pobrać nową wersję na stronie programu!\n')
        input("Naciśnij enter by pominąć...")


def connect_to_discord_querry() -> bool:
    querry : str = fzf(['TAK', 'NIE'], '--header=Czy chcesz aby twoi znajomi z discorda widzieli co oglądasz?')[0]

    if querry == 'TAK':
        update_config('dc_status', "TAK")
        save_config()
    elif querry == 'NIE':
        update_config('dc_status', "NIE")
        save_config()


def change_search_lang() -> bool:
    querry : str = fzf(['ORYGINALNY', 'ANGIELSKI'], '--header=Chesz wyszukiwać po oryginalnym tytule, czy tytule angielskim?')[0]

    if querry == 'ORYGINALNY':
        update_config('search_lang', "ORYGINALNY")
        save_config()
    elif querry == 'ANGIELSKI':
        update_config('search_lang', "ANGIELSKI")
        save_config()


def fzf(choices: List[str], fzf_options: str = '') -> List[str]:
    if fzf_options is None:
        fzf_options = ''

    choices_bytes = '\n'.join(choices).encode()

    command : List[str] = ['fzf',fzf_options]

    try:
        command_result = run(command, input=choices_bytes, check=True, stdout=PIPE)
        results = command_result.stdout.decode().strip().split('\n')

        return results
    except:
        pass



def all_series() -> dict:
    all_series_list : list = get(f'https://api.docchi.pl/v1/series/list').json()

    _all_series : list = []

    for serie in all_series_list:
        if config['search_lang'] == "ORYGINALNY":
            _all_series.append(f"{serie['title']} [{serie['episodes']}]")
        elif config['search_lang'] == "ANGIELSKI":
            _all_series.append(f"{serie['title_en']}, [{serie['episodes']}]")
    
    # number = 0
    # for serie in all_series_list:
    #     img_url = serie['cover']
    #     img_data = get(img_url).content
    #     with open(f'temp/{number}', 'wb') as img_file:
    #         img_file.write(img_data)
    #     number += 1
        
    
    choosed : int = _all_series.index(fzf(_all_series, '--header=WYSZUKAJ ANIME:')[0])
    
    serie : dict = all_series_list[choosed]

    return serie


def search_for_anime(serie = None, ep = None, players = None) -> List[any]:
    if serie == None:
        serie : dict = all_series()

    if ep == None:
        ep : int = choose_ep(serie=serie)

    players : list = get_players_list(slug=serie['slug'], ep=ep)

    return [choose_player(players=players), serie, ep]


def open_mpv(quality, URL):
    try:
        process : Popen = Popen(args=['mpv', f'--ytdl-format={quality}', URL], shell=False, stdout=DEVNULL)
    except:
        print('[ERROR] Błąd podczas uruchamiania MPV!')
        exit()

    return process


def choose_quality() -> None:
    quality_list : List[str] = ["NAJLEPSZA","NAJSZYBSZA"]
    quality_choose : str = fzf(quality_list,'--header=WYBIERZ JAKOŚĆ: ')[0]
    if quality_choose == quality_list[0]:
        update_config('quality', 'NAJLEPSZA')
        save_config()
    elif quality_choose == quality_list[1]:
        update_config('quality', 'NAJSZYBSZA')
        save_config()


def watch(serie = None, ep = None, cont = False):
    if cont == True:
        if config['last_url'] == None:
            print("[BŁĄD] Nie możesz kontynuować niczego")
            exit()
        anime = [config['last_url'],config['last_info'],config['last_ep']]
    else:
        anime = search_for_anime(serie, ep)
        update_config('last_url', anime[0])
        update_config('last_info', anime[1])
        update_config('last_ep', anime[2])
        save_config()
    

    if config['quality'] == "NAJLEPSZA":
        mpv_quality = 'best'
    elif config['quality'] == "NAJSZYBSZA":
        mpv_quality = 'worst'
    
    process = open_mpv(quality=mpv_quality, URL=anime[0])

    try:
        if config['dc_status'] == "TAK":
            update_discord(state=f"Ep: {anime[2]}",details=anime[1]['title'], time=time())
        elif config['dc_status'] == "NIE":
            update_discord(state=f"Tajne!",details='Ogląda anime...', time=time())
    except:
        pass
        
    info = [anime, mpv_quality, process]
    watching_menu(info=info)


def main_menu() -> None:
    try:
        update_discord(state="Używa doccli!", details="Menu główne",time=time())
    except:
        pass

    try:
        if config['search_lang'] == 'ORYGINALNY':
            continue_title = config["last_info"]["title"]
        elif config['search_lang'] == 'ANGIELSKI':
            continue_title = config["last_info"]["title_en"]
        continue_ep = config["last_ep"]
    except:
        continue_title = None
        continue_ep = None

    tabs : List[str] = ['Wyszukaj anime', f'Kontynuuj: {continue_title} [Ep: {continue_ep}]',f'Status aktywności: {config["dc_status"]}',f'Język tytułów: {config["search_lang"]}',f'Domyślna jakość: {config["quality"]}','Zamknij']

    option = fzf(tabs, '--header=WYBIERZ:')[0]

    if option == tabs[0]:
        watch()

    elif option == tabs[1]:
        watch(cont=True) # CONTINYUE

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


def load_config():
    if not path.exists("doccli.config"):
        with open('doccli.config', 'w') as f:
            default_config.update({"config_version" : version})
            json.dump(default_config, f)
            f.close()

    with open("doccli.config","r") as f:
        readed = json.load(f)

        if readed['config_version'] != version:
            print("[INFO] Wykryto config ze starej wersji! Podmienianie...")
            f.close()
            remove("doccli.config")
            load_config()
        else:
            global config
            config = readed
            f.close()
    

def update_config(var, value):
    config.update({f"{var}": value})


def save_config():
    with open("doccli.config","w") as f:
        json.dump(config, f)
        f.close()

    load_config()



def watching_menu(info) -> None:
    tabs : List[str] = ['Wróć do menu głównego','Wróć do listy odcinków', f'Zmień domyślną jakość: {config["quality"]}']

    min_ep = 1
    actual_ep = int(info[0][2])
    max_ep = int(info[0][1]['episodes'])

    if actual_ep > min_ep:
        tabs.append('Poprzedni odcinek')

    if actual_ep < max_ep:
        tabs.append('Następny odcinek')


    option : str = fzf(tabs, '--header=WYBIERZ:')[0]


    if option == tabs[0]:
        info[2].kill()
        main_menu()

    if option == tabs[1]:
        info[2].kill()
        watch(serie=info[0][1])

    if option == tabs[2]:
        info[2].kill()
        choose_quality()
        watch(cont=True)
    
    if option == 'Poprzedni odcinek':
        info[2].kill()
        watch(serie=info[0][1],ep=str(actual_ep - 1))

    if option == 'Następny odcinek':
        info[2].kill()
        watch(serie=info[0][1],ep=str(actual_ep + 1))
    
# Start!
if __name__ == "__main__":
    check_update()
    load_config()
    connect_discord()
    main_menu()
