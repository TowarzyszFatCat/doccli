# @TowarzyszFatCat
# v1.3.6

from requests import get
from os import system, getpid
from os import name as system_name
from time import sleep, time
from subprocess import Popen, DEVNULL, run, PIPE
from pypresence import Presence
from typing import List


# GLOBAL VARIABLES
# Client id from discord developer portal
RPC = Presence(client_id='1206583480771936318')
dc_status : bool = True
version : str = 'v1.3.6'

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
    while True:

        querry : str = fzf(['TAK', 'NIE'], '--header=Czy chcesz aby twoi znajomi z discorda widzieli co oglądasz?')[0]
        
        global dc_status

        if querry == 'TAK':
            dc_status = True
            break
        elif querry == 'NIE':
            dc_status = False
            break


def fzf(choices: List[str], fzf_options: str = '') -> List[str]:
    if fzf_options is None:
        fzf_options = ''

    command : List[str] = ['fzf',fzf_options]
    choices_bytes = '\n'.join(choices).encode()

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
#        _all_series.append(f"{serie['title_en']}, [{serie['episodes']}]")
        _all_series.append(f"{serie['title']} [{serie['episodes']}]")
    
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


def open_mpv(quality, anime):
    try:
        process : Popen = Popen(args=['mpv', f'--ytdl-format={quality}', anime[0]], shell=False, stdout=DEVNULL)
    except:
        print('[ERROR] Błąd podczas uruchamiania MPV!')
        exit()

    return process


def choose_quality() -> None:
    quality : str = ''
    quality_list : List[str] = ["NAJLEPSZA","NAJGORSZA"]
    quality_choose : str = fzf(quality_list,'--header=WYBIERZ JAKOŚĆ: ')[0]
    if quality_choose == quality_list[0]:
        quality = 'best'
    elif quality_choose == quality_list[1]:
        quality = 'worst'

    return quality


def watch(serie = None, ep = None):
    anime = search_for_anime(serie, ep)
    quality = choose_quality()
    process = open_mpv(quality=quality, anime=anime)

    try:
        if dc_status:
            update_discord(state=f"Ep: {anime[2]}",details=anime[1]['title'], time=time())
        else:
            update_discord(state=f"Tajne!",details='Ogląda anime...', time=time())
    except:
        pass
        
    info = [anime, quality, process]
    watching_menu(info=info)


def main_menu() -> None:
    try:
        update_discord(state="Używa doccli!", details="Menu główne",time=time())
    except:
        pass

    tabs : List[str] = ['Wyszukaj anime',f'Status aktywności: {dc_status}','Zamknij']

    option = fzf(tabs, '--header=WYBIERZ:')[0]

    if option == tabs[0]:
        
        watch()

    elif option == tabs[1]:
        connect_to_discord_querry()
        main_menu()

    elif option == tabs[2]:
        exit()


def watching_menu(info) -> None:
    tabs : List[str] = ['Wróć do menu głównego','Wróć do listy odcinków']

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
    
    if option == 'Poprzedni odcinek':
        info[2].kill()
        watch(serie=info[0][1],ep=str(actual_ep - 1))

    if option == 'Następny odcinek':
        info[2].kill()
        watch(serie=info[0][1],ep=str(actual_ep + 1))
    
# Start!
if __name__ == "__main__":
    check_update()
    connect_discord()
    main_menu()
