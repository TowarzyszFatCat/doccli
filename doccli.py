# @TowarzyszFatCat
# v1.3
# Multisupport update!

from requests import get
from os import system
from os import name as system_name
from time import sleep, time
from subprocess import Popen, DEVNULL
from pypresence import Presence

client_id = '1206583480771936318'
RPC = Presence(client_id)
try:
    print("[INFO] Connecting with DRP RPC... If it takes too long to connect, abort it by pressing <CTRL C>")
    RPC.connect()
    RPC.update(state="Using doccli", details="Searching...", large_image="doccli_icon")
except:
    print("Failed to connect with DRP RPC!")


# Get list of all aviable players.
def get_players_list(slug, number):
    players_list = get(f'https://api.docchi.pl/v1/episodes/find/{slug}/{number}').json()
    
    all_aviable_players = []

    for player in players_list:

        player_data = []

        player_data.append(player['player_hosting'])
        player_data.append(player['player'])

        all_aviable_players.append(player_data)

    # Return format: [('hosting name', 'player link'), ... ]
    return(all_aviable_players)


# Search for series.
def search(name):
    series_list = get(f'https://api.docchi.pl/v1/series/related/{name}').json()

    all_aviable_series = []

    for serie in series_list:

        serie_data = []

        serie_data.append(serie['slug'])
        serie_data.append(serie['title'])
        serie_data.append(serie['cover']) # Future plans
        serie_data.append(serie['episodes'])

        all_aviable_series.append(serie_data)

    # Return format: [('slug', 'title', 'cover url', 'episodes number'), ... ]
    return(all_aviable_series)


# Let someone choose serie.
def choose_serie():

    all_aviable_series = search(input("Search: "))
    number = 0

    for serie in all_aviable_series:

        number += 1

        print(f'{number}. {serie[1]} [ep: {serie[3]}]')
    
    choosed_number = int(input("Choose: "))

    return all_aviable_series[choosed_number - 1]


# Let someone choose episode.
def choose_ep(serie):

    return input(f'Choose ep from 1 to {serie[3]}: ')
    

# Let someone choose player.
def choose_player(players):

    number = 0

    for player in players:

        number += 1

        print(f'{number}. {player[0]}')
    
    choose_prompt = int(input(f'Choose host (mega.nz not working): '))
    choosed_player = players[choose_prompt - 1]
    return choosed_player[1]


# Clear cli
def clear():
    system('cls' if system_name == 'nt' else 'clear')


def update_discord(state, details, time):
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
    try:
        clear()

        serie = choose_serie()

        clear()

        ep = choose_ep(serie)

        clear()

        players = get_players_list(serie[0], ep)
        choosed_player = choose_player(players)

        clear()

        print("[INFO] Press <CTRL + C> to exit!")

        # Start mpv in separate process.
        try:
            process = Popen(['mpv', choosed_player], shell=False, stdout=DEVNULL)
        except FileNotFoundError:
            print('[ERROR] Make sure you installed MPV!')
            exit()

        # Status will stay while program is running.
        update_discord(f"Ep: {ep}",serie[1], time())

        # Check if mpv is still running, if no exit.
        while process.poll() is None:
            sleep(5)
        else:
            print("Exiting...")

            
    except KeyboardInterrupt:
        print("")