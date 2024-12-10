import requests.exceptions
from requests import get

def check_service_availability() -> str:
    try:
        req = get(f"https://api.docchi.pl/v1/")
        if req.status_code == 200:
            return "ONLINE"
    except:
        return "OFFLINE"


# Get list of players for episode
def get_players_list(slug, episode):
    req = get(f"https://api.docchi.pl/v1/episodes/find/{slug}/{episode}")
    return req.status_code, req.json()


# Get list of how much episodes series contains
def get_episodes_count_for_serie(slug):
    req = get(f"https://api.docchi.pl/v1/episodes/count/{slug}")
    return req.status_code, req.json()


# Get all hentais list
def get_hentai_list():  # XD
    req = get(f"https://api.docchi.pl/v1/series/hentai")
    return req.status_code, req.json()


# Get all series list
def get_series_list():
    req = get(f"https://api.docchi.pl/v1/series/list")
    return req.status_code, req.json()


# Get detail info about the Series
def get_details_for_serie(slug):
    req = get(f"https://api.docchi.pl/v1/series/find/{slug}")
    return req.status_code, req.json()