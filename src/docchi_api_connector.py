import re
import time

# From pip
from requests import get

# Get list of players for episode
def get_players_list(SLUG, NUMBER):
    request = get(f"https://api.docchi.pl/v1/episodes/find/{SLUG}/{NUMBER}")
    if request.status_code == 200:
        return request.json()
    else:
        return request.status_code


# japidi ale to jest wolne gowno nie uzywac pod zadnym pozorem chyba ze program by chodzil za szybko :P
# Get list of how much episodes series contains
def get_episodes_count_for_serie(SLUG):
    request = get(f"https://api.docchi.pl/v1/episodes/count/{SLUG}")
    if request.status_code == 200:
        return len(request.json())
    else:
        return request.status_code


# Get all hentais list
def get_hentai_list():  # XD
    request = get(f"https://api.docchi.pl/v1/series/hentai")
    if request.status_code == 200:
        return request.json()
    else:
        return request.status_code


# Get all series list
def get_series_list():
    request = get(f"https://api.docchi.pl/v1/series/list")
    if request.status_code == 200:
        return request.json()
    else:
        return request.status_code


# Get detail info about the Series
def get_details_for_serie(SLUG):
    request = get(f"https://api.docchi.pl/v1/series/find/{SLUG}")
    if request.status_code == 200:
        return request.json()
    else:
        return request.status_code


def extract_lycoris_direct_link(embed_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://docchi.pl/"
    }
    
    try:
        request = get(embed_url, headers=headers, timeout=5)
        
        if request.status_code == 200:
            # szuka w całym kodzie jakiegokolwiek linku z końcówką .mp4
            match = re.search(r'(https?://[^"\']+\.mp4)', request.text, re.IGNORECASE)
            
            if match:
                return match.group(1)
    except:
        pass
    
    return None