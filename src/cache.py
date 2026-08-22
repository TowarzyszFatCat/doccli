import time

# From pip
from termcolor import colored

# Doccli modules
from anilist_connector import get_trending_anime_malids
from docchi_api_connector import get_series_list
from ui_utils import clear
from i18n import t

SERIES_CACHE = None
TRENDING_CACHE = None
TRENDING_RETRY_AT = 0.0
TRENDING_RETRY_DELAY = 300

def preload_series_cache():
    global SERIES_CACHE, TRENDING_CACHE, TRENDING_RETRY_AT
    if SERIES_CACHE is None or TRENDING_CACHE is None:
        clear()
        print(colored(t("cache_conn"), "cyan"))
        print(colored(t("cache_fetch"), "cyan"))
        SERIES_CACHE = get_series_list()
        TRENDING_CACHE = _as_list(get_trending_anime_malids())
        TRENDING_RETRY_AT = time.time() + TRENDING_RETRY_DELAY
        time.sleep(1)

def _as_list(value):
    return value if isinstance(value, list) else []

def get_cached_series_list():
    global SERIES_CACHE
    if SERIES_CACHE is None:
         preload_series_cache()
    return SERIES_CACHE

def get_cached_trending_list():
    global TRENDING_CACHE, TRENDING_RETRY_AT
    if TRENDING_CACHE is None:
         preload_series_cache()

    TRENDING_CACHE = _as_list(TRENDING_CACHE)

    # Pusta lista oznacza, że AniList nie odpowiedział. Próba ponowna co
    # TRENDING_RETRY_DELAY, żeby powrót API nie wymagał restartu doccli.
    if not TRENDING_CACHE and time.time() >= TRENDING_RETRY_AT:
        TRENDING_RETRY_AT = time.time() + TRENDING_RETRY_DELAY
        TRENDING_CACHE = _as_list(get_trending_anime_malids())

    return TRENDING_CACHE