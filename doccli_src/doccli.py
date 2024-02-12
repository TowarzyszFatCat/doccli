# @TowarzyszFatCat
# v1.0

import requests as rq
import os
import time
from discordrp import Presence
import subprocess

client_id = '1206583480771936318'

# Get list of all aviable players.
def get_players_list(slug, number):
    players_list = rq.get(f'https://api.docchi.pl/v1/episodes/find/{slug}/{number}').json()
    
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
    series_list = rq.get(f'https://api.docchi.pl/v1/series/related/{name}').json()

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
    os.system('clear')

def discord(state, details):
    with Presence(client_id) as presence:
        print("Connected")
        presence.set(
            {
                "state": f"{state}",
                "details": f"{details}",
                "timestamps": {"start": int(time.time())},
            }
        )
        print("Presence updated")

        while True:
            time.sleep(15)



def play_ep(choosed_player):
    subprocess.Popen(['mpv', choosed_player], shell=False)


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

        print("Press <CTRL + C> two times to exit!")

        play_ep(choosed_player)

        discord(f"Ep: {ep}",serie[1])
    except KeyboardInterrupt:
        print("")
