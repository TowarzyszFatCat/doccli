from requests import get


# Get list of players for episode
def get_players_list(SLUG, NUMBER):
    request = get(f"https://api.docchi.pl/v1/episodes/find/{SLUG}/{NUMBER}")
    if request.status_code == 200:
        return request.json()
    else:
        print(request.status_code)


# Get list of how much episodes series contains
def get_episodes_count_for_serie(SLUG):
    request = get(f"https://api.docchi.pl/v1/episodes/count/{SLUG}")
    if request.status_code == 200:
        return len(request.json())
    else:
        print(request.status_code)


# Get all hentais list
def get_hentai_list():  # XD
    request = get(f"https://api.docchi.pl/v1/series/hentai")
    if request.status_code == 200:
        return request.json()
    else:
        print(request.status_code)


# Get all series list
def get_series_list():
    request = get(f"https://api.docchi.pl/v1/series/list")
    if request.status_code == 200:
        return request.json()
    else:
        print(request.status_code)


# Get detail info about the Series
def get_details_for_serie(SLUG):
    request = get(f"https://api.docchi.pl/v1/series/find/{SLUG}")
    if request.status_code == 200:
        return request.json()
    else:
        print(request.status_code)