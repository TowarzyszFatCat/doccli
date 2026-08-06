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

def preload_series_cache():
    global SERIES_CACHE, TRENDING_CACHE
    if SERIES_CACHE is None or TRENDING_CACHE is None:
        clear()
        print(colored(t("cache_conn"), "cyan"))
        print(colored(t("cache_fetch"), "cyan"))
        SERIES_CACHE = get_series_list()
        TRENDING_CACHE = get_trending_anime_malids()
        time.sleep(1)

def get_cached_series_list():
    global SERIES_CACHE
    if SERIES_CACHE is None:
         preload_series_cache()
    return SERIES_CACHE

def get_cached_trending_list():
    global TRENDING_CACHE
    if TRENDING_CACHE is None:
         preload_series_cache()
    return TRENDING_CACHE