import re
import time
import subprocess
import json
import difflib


# From pip
from requests import get
from termcolor import colored
from curl_cffi import requests as cffi_requests

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

def anidb_curl(url):
    """
    Używa curl_cffi, aby ominąć Cloudflare.
    """
    try:
        response = cffi_requests.get(url, impersonate="chrome110", timeout=10)
        if response.status_code == 200:
            return response.text, response.url
    except Exception:
        pass
    return "", ""

def get_english_players(details, ep_number):
    """
    Pobiera absolutnie wszystkie angielskie źródła z anidb.app omijając CF
    i flagując SUB/DUB na podstawie zawartości JSON-a.
    Zawiera system punktacji sezonów oraz offset Absolute Numbering.
    """
    
    players = []
    titles_to_try = [details.get('title_en'), details.get('title')]
    
    anidb_id = None
    
    for t in titles_to_try:
        if not t or t == "Nieznany" or t == "Brak":
            continue
            
        query = str(t).replace(' ', '+')
        search_page, final_url = anidb_curl(f"https://anidb.app/browse?q={query}")
        
        if not search_page or "Just a moment" in search_page:
            continue
            
        if "/anime/" in final_url:
            match = re.search(r'/anime/.*?-([0-9]+)', final_url)
            if match:
                anidb_id = match.group(1)
                break

        matches = re.findall(r'/anime/([^"\'\>]+)-([0-9]+)["\']', search_page)
            
        if matches:
            target_slug = str(t).lower().replace(' ', '-').replace(':', '')
            
            best_id = None
            best_ratio = 0.45 
            
            for slug, anime_id in matches:
                ratio = difflib.SequenceMatcher(None, target_slug, slug.lower()).ratio()
                
                target_numbers = re.findall(r'\d+', target_slug)
                slug_numbers = re.findall(r'\d+', slug.lower())
                
                if target_numbers:
                    for num in target_numbers:
                        if num in slug_numbers:
                            ratio += 0.5 
                        else:
                            ratio -= 0.5 
                            
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_id = anime_id
                    
            if best_id:
                anidb_id = best_id
                break

    if not anidb_id:
        return []

    eps_json, _ = anidb_curl(f"https://anidb.app/api/frontend/anime/{anidb_id}/episodes")
    
    if not eps_json: 
        return []
    
    try:
        eps_data = json.loads(eps_json)
        if isinstance(eps_data, dict):
            eps_data = eps_data.get('data', eps_data.get('episodes', []))
    except:
        return []
        
    ep_id = None
    
    # 1. Klasyczne szukanie (gdy odcinek 1 = 1)
    for ep in eps_data:
        if isinstance(ep, dict) and str(ep.get('number')) == str(ep_number):
            ep_id = ep.get('id')
            break
            
    # 2. System Absolute Numbering (np. gdy odcinek 1 = 25)
    if not ep_id and len(eps_data) > 0:
        valid_eps = [ep for ep in eps_data if isinstance(ep, dict) and ep.get('number') is not None]
        try:
            valid_eps.sort(key=lambda x: float(x['number']))
            target_index = int(ep_number) - 1
            if 0 <= target_index < len(valid_eps):
                ep_id = valid_eps[target_index]['id']
        except Exception:
            pass
            
    if not ep_id: 
        return []
        
    langs_json, _ = anidb_curl(f"https://anidb.app/api/frontend/episode/{ep_id}/languages")
    
    if not langs_json: 
        return []
    
    try:
        langs_data = json.loads(langs_json)
        if isinstance(langs_data, dict):
            langs_data = langs_data.get('data', langs_data.get('languages', []))
    except:
        return []
        
    source_counter = 1
    
    for lang in langs_data:
        if not isinstance(lang, dict):
            continue
            
        embed_url = lang.get('embed_url')
        if not embed_url: 
            continue
        
        embed_url = embed_url.replace('\\/', '/')
        
        lang_str = str(lang).lower()
        if 'eng' in lang_str or 'dub' in lang_str:
            label = "dubbing"
        elif 'jpn' in lang_str or 'sub' in lang_str or 'ja' in lang_str:
            label = "napisy"
        else:
            label = "źródło"
            
        embed_page, _ = anidb_curl(embed_url)
        
        m3u8_match = re.search(r"file:\s*['\"]([^'\"]+)['\"]", embed_page)
        if not m3u8_match:
            m3u8_match = re.search(r"['\"](https?://[^'\"]+\.(?:m3u8|mp4)[^'\"]*)['\"]", embed_page)
            
        if m3u8_match:
            master_url = m3u8_match.group(1)
            hosting = f"anidb.app ({label} {source_counter})"
            players.append({
                "player_hosting": hosting,
                "player": master_url
            })
            source_counter += 1
            
    return players