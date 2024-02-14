# @TowarzyszFatCat
# v1.3.2
# Small presence fix

from requests import get
from os import system, getpid
from os import name as system_name
from time import sleep, time
from subprocess import Popen, DEVNULL
from pypresence import Presence

# Client id from discord developer portal
RPC = Presence(client_id='1206583480771936318')

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

        player_data : list = []

        player_data.append(player['player_hosting'])
        player_data.append(player['player'])

        all_aviable_players.append(player_data)

    # Return format: [('hosting name', 'player link'), ... ]
    return(all_aviable_players)


# Search for series.
def search() -> list:
    search_prompt : str = str(input("Wyszukaj: "))
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
    
    choosed_number : int = int(input("Wybierz: "))

    return all_aviable_series[choosed_number - 1]


# Let someone choose episode.
def choose_ep(serie : list) -> int:

    return int(input(f'Wybierz odcinek od 1 do {serie[3]}: '))
    

# Let someone choose player.
def choose_player(players) -> str:

    number : int = 0

    for player in players:

        number += 1

        print(f'{number}. {player[0]}')
    
    choose_prompt : int = int(input(f'Wybierz hosta (mega.nz nie jest wspierany): '))
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
    

# It looks terrible ik!
if __name__ == "__main__":
    try:
        connect_discord()
    except:
        pass

    # Always run program
    while True:
        try:
            try:
                update_discord(state="Używa doccli!", details="Szuka czegoś do obejrzenia...",time=time())
            except:
                pass

            clear()

            print("[INFO] Naciśnij <CTRL + C> aby wyjść!")

            search_prompt : list = search()

            if len(search_prompt) == 0:
                print("[INFO] Brak rezultatów!")
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
            except:
                print('[ERROR] Błąd podczas uruchamiania MPV!')
                exit()
            
            try:
                # Status will stay while program is running.
                update_discord(state=f"Ep: {ep}",details=serie[1], time=time())
            except:
                pass

            print("[INFO] Naciśnij <CTRL + C> aby wyłączyć program lub zamknij odtwarzacz by wrócić do wyszukiwarki!")

            # Check if mpv is still running, if no exit.
            while process.poll() is None:
                sleep(1)
            else:
                continue

        except KeyboardInterrupt:
            exit()
