# @TowarzyszFatCat
# v1.3.1
# Rewrite update

from requests import get
from os import system, getpid
from os import name as system_name
from time import sleep, time
from subprocess import Popen, DEVNULL
from pypresence import Presence
from credintials import client_id

# Client id from discord developer portal
RPC = Presence(client_id=client_id)

def connect_discord() -> None:
    try:
        print("[INFO] Connecting with DRP RPC... If it takes too long to connect, abort it by pressing <CTRL C>")
        RPC.connect()
        RPC.clear(getpid())
    except:
        print("[ERROR] Failed to connect with DRP RPC!")


# Get list of all aviable players.
def get_players_list(slug : str, ep : int) -> list:
    players_list : list = get(f'https://api.docchi.pl/v1/episodes/find/{slug}/{ep}').json()
    
    all_aviable_players : list = []

    for player in players_list:

        player_data : list = []

        player_data.append(player['player_hosting'])
        player_data.append(player['player'])

        all_aviable_players.append(player_data)

    # Return format: [('hosting name', 'player link'), ... ]
    return(all_aviable_players)


# Search for series.
def search() -> list:
    search_prompt : str = str(input("Search: "))
    series_list : list = get(f'https://api.docchi.pl/v1/series/related/{search_prompt}').json()

    all_aviable_series : list = []

    for serie in series_list:

        serie_data : list = []

        serie_data.append(serie['slug'])
        serie_data.append(serie['title'])
        serie_data.append(serie['cover']) # Future plans
        serie_data.append(serie['episodes'])

        all_aviable_series.append(serie_data)

    # Return format: [('slug', 'title', 'cover url', 'episodes number'), ... ]
    return(all_aviable_series)


# Let someone choose serie.
def choose_serie(all_aviable_series : list) -> list:

    number : int = 0

    for serie in all_aviable_series:

        number += 1

        print(f'{number}. {serie[1]} [ep: {serie[3]}]')
    
    choosed_number : int = int(input("Choose: "))

    return all_aviable_series[choosed_number - 1]


# Let someone choose episode.
def choose_ep(serie : list) -> int:

    return int(input(f'Choose ep from 1 to {serie[3]}: '))
    

# Let someone choose player.
def choose_player(players) -> str:

    number : int = 0

    for player in players:

        number += 1

        print(f'{number}. {player[0]}')
    
    choose_prompt : int = int(input(f'Choose host (mega.nz not working): '))
    choosed_player : str = players[choose_prompt - 1]
    return choosed_player[1]


# Clear cli
def clear() -> None:
    system('cls' if system_name == 'nt' else 'clear')


def update_discord(state : str, details : str, time : time) -> None:
    RPC.update(
        state=f"{state}",
        details=f"{details}",
        large_image="doccli_icon",
        large_text="A cli to watch anime from docchi.pl",
        start=int(time),
        buttons=[
            {
                "label": "Download doccli",
                "url": "https://github.com/TowarzyszFatCat/doccli"
            },
            {
                     "label": "Visit docchi.pl",
                     "url": "https://docchi.pl/",
            }
        ]
        )
    

# It looks terrible ik!
if __name__ == "__main__":
    connect_discord()
    update_discord(state="Using doccli", details="Searching...",time=time())

    # Always run program
    while True:
        try:
            clear()

            print("[INFO] Press <CTRL + C> if you want to exit !")

            search_prompt : list = search()

            if len(search_prompt) == 0:
                print("[INFO] No results!")
                continue
            clear()

            serie : list = choose_serie(all_aviable_series=search_prompt)
            clear()

            ep : int = choose_ep(serie=serie)
            clear()
    
            players : list = get_players_list(slug=serie[0], ep=ep)

            choosed_player : str = choose_player(players=players)
            clear()

            # Start mpv in separate process.
            try:
                process : Popen = Popen(args=['mpv', choosed_player], shell=False, stdout=DEVNULL)
            except FileNotFoundError:
                print('[ERROR] Make sure you installed MPV!')
                exit()

            # Status will stay while program is running.
            update_discord(state=f"Ep: {ep}",details=serie[1], time=time())

            print("[INFO] Press <CTRL + C> to exit all or close MPV to return to search bar!")

            # Check if mpv is still running, if no exit.
            while process.poll() is None:
                sleep(1)
            else:
                continue

        except KeyboardInterrupt:
            exit()