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
SERIES_RETRY_AT = 0.0
TRENDING_RETRY_AT = 0.0
CACHE_RETRY_DELAY = 300

def _as_list(value):
    """
    Oba źródła zwracają kod HTTP przy nieudanym zapytaniu, a cache musi trzymać
    wyłącznie listy - inaczej "x in cache" albo iteracja po cache kończy się
    TypeError w miejscu odległym od faktycznej awarii.
    """
    return value if isinstance(value, list) else []

def preload_series_cache():
    global SERIES_CACHE, TRENDING_CACHE, SERIES_RETRY_AT, TRENDING_RETRY_AT
    if SERIES_CACHE is None or TRENDING_CACHE is None:
        clear()
        print(colored(t("cache_conn"), "cyan"))
        print(colored(t("cache_fetch"), "cyan"))
        SERIES_CACHE = _as_list(get_series_list())
        TRENDING_CACHE = _as_list(get_trending_anime_malids())
        now = time.time()
        SERIES_RETRY_AT = now + CACHE_RETRY_DELAY
        TRENDING_RETRY_AT = now + CACHE_RETRY_DELAY
        time.sleep(1)

def get_cached_series_list():
    global SERIES_CACHE, SERIES_RETRY_AT
    if SERIES_CACHE is None:
         preload_series_cache()

    SERIES_CACHE = _as_list(SERIES_CACHE)

    # Pusty cache oznacza nieudane pobranie. Ponawiamy nie częściej niż raz na
    # CACHE_RETRY_DELAY, żeby powrót API nie wymagał restartu doccli.
    if not SERIES_CACHE and time.time() >= SERIES_RETRY_AT:
        SERIES_RETRY_AT = time.time() + CACHE_RETRY_DELAY
        SERIES_CACHE = _as_list(get_series_list())

    return SERIES_CACHE

def get_cached_trending_list():
    global TRENDING_CACHE, TRENDING_RETRY_AT
    if TRENDING_CACHE is None:
         preload_series_cache()

    TRENDING_CACHE = _as_list(TRENDING_CACHE)

    if not TRENDING_CACHE and time.time() >= TRENDING_RETRY_AT:
        TRENDING_RETRY_AT = time.time() + CACHE_RETRY_DELAY
        TRENDING_CACHE = _as_list(get_trending_anime_malids())

    return TRENDING_CACHE