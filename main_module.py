import pathlib
import sys
import time
import re
import tempfile
import subprocess
import json
from InquirerPy import inquirer, prompt
import os
from os import system
from docchi_api_connector import get_series_list, get_episodes_count_for_serie, get_players_list, get_details_for_serie, extract_lycoris_direct_link #, get_skip_times
from anilist_connector import get_trending_anime_malids, get_stars_by_mal_id
from menus_decor import MAIN_MENU, SZUKAJ, NA_CZASIE, MOJA_LISTA, HISTORIA
from subprocess import Popen, DEVNULL
from termcolor import colored
import webbrowser
from discord_integration import update_rpc, set_running
import platform
from zipfile import ZipFile
from datetime import datetime, date
import requests
import shutil
from concurrent.futures import ThreadPoolExecutor

# Zmienne przechowujące pobrane bazy
SERIES_CACHE = None
TRENDING_CACHE = None

def preload_series_cache():
    global SERIES_CACHE, TRENDING_CACHE
    # Pobiera listy tylko przy pierwszym uruchomieniu
    if SERIES_CACHE is None or TRENDING_CACHE is None:
        clear()
        print(colored("[INFO] Łączenie z serwerami Docchi oraz AniList...", "cyan"))
        print(colored("[INFO] Pobieranie bazy tytułów i trendów...", "cyan"))
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

def kill_process(process):
    if not process:
        return
    
    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/F", "/T", "/PID", str(process.pid)], 
            capture_output=True
        )
    else:
        process.terminate()

def clear():
    system("cls" if os.name == "nt" else "clear")


def get_terminal_size():
    columns, rows = os.get_terminal_size()
    return columns, rows


def open_menu(choices, prompt='Prompt', border=True, qmark='', message='', pointer='>', cycle=True, height=10, image=None):
    clear()

    if image:
        try:
            response = requests.get(image)
            image_path = os.path.join(tempfile.gettempdir(), "cover.jpg")
            with open(image_path, 'wb') as file:
                file.write(response.content)

            # Sprawdzamy czy chafa jest zainstalowana w systemie
            if shutil.which('chafa') is not None:
                term_width, term_height = get_terminal_size()
                avail_height = max(5, term_height - height - 5)
                
                os.system(f"chafa -s {term_width}x{avail_height} --align=center {image_path}")
            else:
                print(center_text("Brak narzędzia 'chafa' do wyświetlania okładek."))
                
        except Exception:
            pass


    action = inquirer.fuzzy(
        message=message if message.startswith('[') else center_text(message),    # Message above border
        choices=choices,
        border=border,
        qmark=qmark,    # Before message above border
        prompt=prompt,
        pointer=pointer,
        cycle=cycle,
        height=height,
    ).execute()

    clear() # Remember to always keep things tidy :P

    try:
        return choices[choices.index(action)]
    except ValueError:
        return open_menu(choices=choices, prompt=prompt, border=border, qmark="Nie znaleziono na liście, wyszukaj ponownie", message=message, pointer=pointer, cycle=cycle, height=height)


def m_welcome():

    load()

    preload_series_cache()

    update_rpc("Menu główne", "Szuka anime do obejrzenia...")

    choices = [
        "Wyszukaj",
        "Anime na czasie"
    ]

    if continue_data[0] is None:
        choices.append("Nie masz nic do wznowienia")
    else:
        choices.append(f"Wznów {continue_data[0]['title']} / {continue_data[0]['title_en']}, Odc: {continue_data[1]}")

    choices.append("Moja lista")
    choices.append("Historia oglądania")
    choices.append("Ustawienia")
    choices.append("Statystyki doccli")
    choices.append("Dołącz do discorda")
    choices.append("Zamknij")

    prompt = 'Wybierz co chcesz zrobić: '

    ans = open_menu(choices=choices, prompt=prompt, height=9, message=MAIN_MENU)

    if ans == choices[0]:
        m_find()
    elif ans == choices[1]:
        m_trending()
    elif ans == choices[2]:
        if not continue_data:
            m_welcome()
        else:
            w_players(continue_data[0]['slug'], continue_data[1])
    elif ans == choices[3]:
        m_mylist()
    elif ans == choices[4]:
        m_history()
    elif ans == choices[5]:
        m_settings()
    elif ans == choices[6]:
        m_stats()
    elif ans == choices[7]:
        m_discord()
    elif ans == choices[8]:
        set_running(False)
        sys.exit()


def m_settings():
    # choices = [{
    #     "type": "list",
    #     "message": "Czy chcesz aby openingi i endingi były automatycznie pomijane?",
    #     "choices": ["Tak", "Nie"],
    # }]

    # skip = prompt(questions=choices)

    # if skip[0] == "Tak":
    #     settings[2] = True
    #     save()
    # elif skip[0] == "Nie":
    #     settings[2] = False
    #     save()

    choices = [{
            "type": "list",
            "message": "Czy chcesz aby znajomi na discordzie widzieli co oglądasz?",
            "choices": ["Tak", "Nie"],
        }]

    res = prompt(questions=choices)

    if res[0] == "Nie":
        settings[0] = False
        save()
        m_welcome()
    if res[0] == "Tak":
        clear()
        settings[0] = True
        choices2 = [{"type": "input", "message": "Wpisz co tylko zechcesz! Będzie to wyświetlane w II linijce statusu. Zostaw puste jeśli chcesz aby był wyświetlany domyślny status. [Minimalnie 2 znaki] (Domyślna wartość: 'Używa doccli!') \n", "name": "status_dc"}]
        res2 = prompt(questions=choices2)

        if not res2['status_dc'] == "" and len(res2['status_dc']) > 1:
            settings[1] = res2['status_dc']
            save()
            m_welcome()
        else:
            settings[1] = 'Używa doccli!'
            save()
            m_welcome()


def m_discord():
    webbrowser.open('https://discord.gg/Y4RcwbE5CJ')
    m_welcome()


def m_mylist():
    choices = ['Cofnij']

    for element in mylist:
        choices.append(f"{element['title']} | {element['title_en']}")

    prompt = 'Wybierz anime: '
    ans = open_menu(choices=choices, prompt=prompt, message=MOJA_LISTA)
    if ans == choices[0]:
        m_welcome()
    else:
        index = choices.index(ans)
        m_details(mylist[index - 1])


def m_history():
    choices = ['Cofnij']

    for element in history:
        choices.append(element)

    prompt = 'Wyszukaj: '
    ans = open_menu(choices=choices, prompt=prompt, message=HISTORIA)
    if ans == choices[0]:
        m_welcome()
    else:
        m_history()


def m_find():
    choices = [
        "Po tytule",
        "Po tytule EN",
        "Mal ID",
        "Cofnij"
    ]

    prompt = 'Wybierz jak chcesz wyszukać: '

    ans = open_menu(choices=choices, prompt=prompt, height=4, message=SZUKAJ)

    if ans == choices[0]:
        perform_search('title')
    elif ans == choices[1]:
        perform_search('title_en')
    elif ans == choices[2]:
        perform_search('mal_id')
    elif ans == choices[3]:
        m_welcome()


def m_stats():

    ep_played = 0
    q_mylist = 0

    for ep in history:
        ep_played += 1

    for quantity in mylist:
        q_mylist += 1

    ti_c = pathlib.Path(PATH_config).stat().st_mtime
    dt_c = datetime.fromtimestamp(ti_c).strftime("%d/%m/%Y, %H:%M:%S")

    creation_dt = date.fromtimestamp(ti_c)
    now_dt = date.today()
    delta_dt = now_dt - creation_dt


    print(colored("Używasz doccli już od:", "white"), colored(delta_dt.days, "green"), colored("dni!", "white"))
    print(colored("Pierwsze uruchomienie doccli:", "white"), colored(dt_c, "green"))
    print('')
    print(colored("Odtworzone odcinki:", "white"), colored(ep_played, "red"))
    print(colored("Pozycje zapisane na liście:", "white"), colored(q_mylist, "red"))
    print('')
    input(colored("Naciśnij enter aby wrócić do menu głównego...", "yellow"))

    m_welcome()


def perform_search(search_key):
    all_series_json = get_cached_series_list()
    
    # Dynamiczne wyciąganie odpowiedniego klucza
    choices = [serie[search_key] for serie in all_series_json]

    prompt = 'Szukaj: '
    ans = open_menu(choices=choices, prompt=prompt, message=SZUKAJ)
    
    ans_index = choices.index(ans)
    ans_details = all_series_json[ans_index]

    m_details(details=ans_details)


def m_trending():
    # Pobieranie danych z cache
    trending_anime_malids = get_cached_trending_list()
    all_anime_list = get_cached_series_list()

    top_anime = []

    for anime in all_anime_list:
        if anime['mal_id'] in trending_anime_malids:
            order = trending_anime_malids.index(anime['mal_id'])
            slug = anime['slug']
            title = anime['title']
            title_en = anime['title_en']
            
            top_anime.append([order, slug, title, title_en])

    # Sortowanie względem miejsca w trendach
    top_anime.sort(key=lambda x: x[0])
    
    choices = ["Cofnij"]
    for anime in top_anime:
        choices.append(f"{anime[0] + 1}. {anime[2]} / {anime[3]}")

    prompt = 'Wybierz: '

    ans = open_menu(choices=choices, prompt=prompt, message=NA_CZASIE)
    
    if ans == choices[0]:
        m_welcome()
    else:
        ans_index = choices.index(ans)
        ans_slug = top_anime[ans_index - 1][1]
        m_details(get_details_for_serie(SLUG=ans_slug))


def m_details(details):
    choices = [
        "Oglądaj od pierwszego odcinka",
        "Lista odcinków",
        "Pobierz cały sezon"
    ]

    if details in mylist:
        choices.append("Usuń z mojej listy")
    else:
        choices.append("Dodaj do mojej listy")

    choices.append("Wyszukiwarka")
    choices.append("Menu główne")

    prompt = 'Wybierz co chcesz zrobić: '

    genres = "[ "
    for genre in details['genres']:
        genres += genre + ","

    genres += " ]"

    episode_count = get_episodes_count_for_serie(details['slug'])

    ans = open_menu(choices=choices, prompt=prompt, qmark=f'{details["title"]} / {details["title_en"]} \n [Ilość odcinków: {episode_count}] [Ocena: {get_stars_by_mal_id(str(details["mal_id"]))}]', message=genres, height=6, image=details['cover'])

    if ans == choices[0]:
        continue_data[0] = details
        w_first(details['slug'])
    elif ans == choices[1]:
        continue_data[0] = details
        w_list(details['slug'])
    elif ans == choices[2]:
        w_download_season(details['slug'], details['title'])
    elif ans == choices[3]:
        if details in mylist:
            mylist.remove(details)
            save()
            load()
            m_details(details)
        else:
            mylist.append(details)
            save()
            load()
            m_details(details)
    elif ans == choices[4]:
        m_find()
    elif ans == choices[5]:
        m_welcome()


def w_first(SLUG):
    continue_data[1] = 1
    save()
    w_players(SLUG, 1)


def w_list(SLUG):
    last_episode = get_episodes_count_for_serie(SLUG)

    if last_episode == 404:
        clear()
        print(colored("Nie znaleziono strony [Błąd 404]", "red"))
        time.sleep(3)
        m_details(get_details_for_serie(SLUG))

    choices = list(range(1, last_episode + 1))
    choices.append('Cofnij')

    prompt = 'Wybierz odcinek: '

    ans = open_menu(choices=choices, prompt=prompt)
    if ans == "Cofnij":
        m_details(get_details_for_serie(SLUG))

    else:
        continue_data[1] = ans
        save()

        w_players(SLUG, ans)


def w_download_season(SLUG, TITLE):
    how_many_episodes = get_episodes_count_for_serie(SLUG)

    if how_many_episodes == 404:
        clear()
        print(colored("Nie znaleziono strony [Błąd 404]", "red"))
        time.sleep(3)
        m_details(get_details_for_serie(SLUG))

    current_dir = os.getcwd()
    safe_title = re.sub(r'[\\/*?:"<>|]', "", TITLE).strip()
    series_dir = os.path.join(current_dir, "doccli_downloads", safe_title)
    
    os.makedirs(series_dir, exist_ok=True)

    clear()
    print(colored(f"[INFO] Przygotowywanie do pobrania {TITLE} ({how_many_episodes} odcinków)...", "cyan"))
    print(colored(f"[INFO] Lokalizacja zapisu: {series_dir}", "yellow"))
    
    for ep_number in range(1, how_many_episodes + 1):
        players = get_players_list(SLUG, ep_number)
        
        if players == 404 or not players:
            print(colored(f"\n[BŁĄD] Nie znaleziono źródeł dla odcinka {ep_number}. Pomijam...", "red"))
            continue

        print(colored(f"\n[INFO] Rozpoczynam pobieranie odcinka {ep_number}/{how_many_episodes}...", "cyan"))
        
        file_name_template = os.path.join(series_dir, f"{safe_title} - Odcinek {ep_number:02d}.%(ext)s")
        downloaded = False
        total_sources = len(players)

        for index, player in enumerate(players, 1):
            target_url = player['player']

            if "lycoris" in target_url.lower():
                extracted = extract_lycoris_direct_link(target_url)
                if extracted:
                    target_url = extracted
            
            print(f"\r\033[K" + colored(f"[*] Sprawdzam źródło {index}/{total_sources}...", "yellow"), end="", flush=True)
            
            command = [
                "yt-dlp",
                "-q",
                "--progress",
                "--no-warnings",
                target_url,
                "-o",
                file_name_template
            ]
            
            result = subprocess.run(command, stderr=subprocess.DEVNULL)
            
            if result.returncode == 0:
                downloaded = True
                print("\n" + colored(f"[+] Sukces! Pobrano odcinek {ep_number}.", "green"))
                break

        if not downloaded:
            print("\n" + colored(f"[BŁĄD] Żadne ze źródeł dla odcinka {ep_number} nie zadziałało.", "red"))
        
    print(colored(f"\n[ZAKOŃCZONO] Proces pobierania serii {TITLE} dobiegł końca!", "green"))
    input(colored("Naciśnij Enter, aby wrócić...", "yellow"))
    
    m_details(get_details_for_serie(SLUG))


def w_players(SLUG, NUMBER, err=''):
    players = []

    # Check if site is fine
    if get_players_list(SLUG, NUMBER) == 404:
        clear()
        print(colored("Nie znaleziono strony [Błąd 404]", "red"))
        time.sleep(3)
        m_details(get_details_for_serie(SLUG))

    for player in get_players_list(SLUG, NUMBER):
        player_info = [player['player_hosting'], player['player']]
        players.append(player_info)



    print(colored("Trwa analizowanie i sprawdzanie źródeł na żywo...", "cyan"))
    
    def check_link(player):
        hosting_name, url = player[0], player[1]
        url_lower = url.lower()
        
        if "lycoris" in url_lower:
            return "ok" if extract_lycoris_direct_link(url) else "error"
            
        elif "mega" in url_lower:
            return "mega" if shutil.which('megatools') is not None else "error"
            
        else:
            try:
                res = subprocess.run(
                    ["yt-dlp", "-q", "--simulate", "--no-warnings", url],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=15 # czas zalezny od predkosci pc oraz sieci
                )
                return "ok" if res.returncode == 0 else "error"
            except:
                return "error"

    # Jednoczesne sprawdzanie wszystkich linków naraz
    with ThreadPoolExecutor(max_workers=15) as executor:
        results = list(executor.map(check_link, players))

    choices = []
    

    for player, status in zip(players, results):
        hosting_name = str(player[0])
        source_link = player[1]


        if status == "ok":
            prefix = "✅ "  # Działa
        elif status == "mega":
            prefix = "🟡 "  # Mega
        else:
            prefix = "❌ "  # Nie działa
            
        display_line = (prefix + hosting_name).ljust(25) + " | Link źródła: " + source_link

        choices.append(display_line)

    choices.append("Wróć do menu")


    last_option = choices[-1]

    prompt = 'Wybierz źródło: '

    ans = open_menu(choices=choices, prompt=prompt, qmark=err)

    if ans == last_option:
        m_welcome()

    ans_index_in_choices = choices.index(ans)
    ans_index = players[ans_index_in_choices]

    process = mpv_play(ans_index[1])


    # Wait 3 sec and check if started playing
    print("Rozpoczynanie odtwarzania...")
    time.sleep(3)                                      # CZAS ZALEZNY OD PREDKOSCI LACZA
    if process == None or process.poll() is not None:
        w_players(SLUG, NUMBER, err='Wybrane źródło nie jest dostępne, lub nie jest wspierane! Sprawdź czy źródło działa używając linku bezpośredniego. Możesz zgłosić niedziałające źródła na discordzie.')

    w_default(SLUG, NUMBER, process)


def mpv_play(URL): #, SKIP_TIMES

    mpv_exec = "mpv.exe" if os.name == "nt" else "mpv"

    if shutil.which('mpv') is None:
        print(colored("[BŁĄD]", "red"), colored("Aby program działał wymagana jest instalacja", "white"), colored("mpv", "green"), '\n')
        sys.exit()
    if shutil.which('yt-dlp') is None:
        print(colored("[BŁĄD]", "red"), colored("Aby program działał wymagana jest instalacja", "white"), colored("yt-dlp", "green"), '\n')
        sys.exit()
        
    temp_dir = tempfile.gettempdir()
    chapters_file = os.path.join(temp_dir, "doccli_chapters")

    if "lycoris" in URL.lower():
        direct_url = extract_lycoris_direct_link(URL)
        if direct_url:
            URL = direct_url
            print(colored("[+] Sukces! Znaleziono bezpośredni link wideo.", "green"))
        else:
            print(colored("[-] Nie udało się zdekodować linku. Próbuję odtworzyć domyślnie...", "yellow"))

    if "mega" in URL:
        if shutil.which('megatools') is None:
            print(colored("[UWAGA]", "yellow"), colored("Aby oglądać z tego źródła wymagana jest instalacja", "white"), colored("megatools", "green"), '\n')
            sys.exit()

        video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm']
        files_in_directory = os.listdir(temp_dir)

        for file in files_in_directory:
            if file.lower().endswith(tuple(video_extensions)):
                file_path = os.path.join(temp_dir, file)
                try:
                    os.remove(file_path)
                except OSError:
                    pass # Omijamy błędy usuwania, np. zablokowane pliki na Windowsie

        mega_url = URL.replace('embed', 'file')
        before_files = set(os.listdir(temp_dir))
        
        # Uwaga: megadl na Windowsie wymaga dodania go do zmiennych środowiskowych PATH
        os.system(f'megadl {mega_url} --path {temp_dir}')
        
        after_files = set(os.listdir(temp_dir))
        new_files = after_files - before_files
        video_files = [file for file in new_files if file.lower().endswith(tuple(video_extensions))]

        try:
            process = Popen(args=[mpv_exec,
                                  "--save-position-on-quit",
                                  "--input-terminal=no",
                                  f"--chapters-file={chapters_file}",
                                  os.path.join(temp_dir, video_files[0])],
                            shell=False,
                            stdout=DEVNULL,
                            stderr=DEVNULL,)
            return process
        except IndexError:
            return

    else:
        process = Popen(args=[mpv_exec,
                              "--save-position-on-quit",
                              "--input-terminal=no",
                              f"--chapters-file={chapters_file}",
                              URL],
                        shell=False,
                        stdout=DEVNULL,
                        stderr=DEVNULL)
        return process
        #f"--script-opts=doccli_skip-opening_start={SKIP_TIMES[0]},doccli_skip-opening_end={SKIP_TIMES[1]},doccli_skip-ending_start={SKIP_TIMES[2]},doccli_skip-ending_end={SKIP_TIMES[3]}",


def w_default(SLUG, NUMBER, process):
    how_many_episodes = get_episodes_count_for_serie(SLUG)

    details = get_details_for_serie(SLUG)

    if settings[0]:
        update_rpc(f"Ogląda: {details['title']} [{str(NUMBER)}/{str(how_many_episodes)}]", settings[1])
    else:
        update_rpc(f"Ogląda anime", settings[1])

    # Save to history
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    history.insert(0, f"[{dt_string}] {details['title']} / {details['title_en']} [Odc: {NUMBER}]")
    save()

    choices = [
        "Zmień źródło",
        "Następny odcinek",
        "Poprzedni odcinek",
        "Lista odcinków",
        "Menu główne"
    ]

    prompt = 'Co chcesz zrobić? '

    ans = open_menu(choices=choices, prompt=prompt, qmark=f'Odcinek: {NUMBER}/{how_many_episodes}', height=5)

    if ans == choices[0]:
        kill_process(process)
        update_rpc("Menu główne", "Szuka anime do obejrzenia...")
        w_players(SLUG, NUMBER)

    elif ans == choices[1]:
        kill_process(process)
        update_rpc("Menu główne", "Szuka anime do obejrzenia...")
        continue_data[1] = NUMBER + 1 if NUMBER < how_many_episodes else NUMBER
        save()
        w_players(SLUG, NUMBER + 1 if NUMBER < how_many_episodes else NUMBER)
        
    elif ans == choices[2]:
        kill_process(process)
        update_rpc("Menu główne", "Szuka anime do obejrzenia...")
        continue_data[1] = NUMBER - 1 if NUMBER >= 2 else NUMBER
        save()
        w_players(SLUG, NUMBER - 1 if NUMBER >= 2 else NUMBER)
        
    elif ans == choices[3]:
        kill_process(process)
        update_rpc("Menu główne", "Szuka anime do obejrzenia...")
        w_list(SLUG)
        
    elif ans == choices[4]:
        kill_process(process)
        update_rpc("Menu główne", "Szuka anime do obejrzenia...")
        m_welcome()


def center_text(text: str) -> str:
    # Odejmujemy 1 od szerokości terminala
    terminal_width = os.get_terminal_size().columns - 1
    art_lines = text.splitlines()
    
    # Zostawiamy oryginalne .center() bez rstrip()
    return "\n".join(line.center(terminal_width) for line in art_lines)


# SAVING SECTION
if os.name == "nt": # WIN
    PATH_config = os.path.join(os.getenv("APPDATA"), "doccli")
else:               # LINUX/MACOS
    PATH_config = os.path.join(os.path.expanduser("~"), ".config", "doccli")

PATH_mylist = os.path.join(PATH_config, "mylist.json")
PATH_continue = os.path.join(PATH_config, "continue.json")
PATH_settings = os.path.join(PATH_config, "settings.json")
PATH_history = os.path.join(PATH_config, "history.json")


def load():
    if not os.path.exists(PATH_config):
        os.makedirs(PATH_config)

    if not os.path.exists(PATH_mylist):
        with open(PATH_mylist, 'w') as file:
            file.write('[]')
    if not os.path.exists(PATH_continue):
        with open(PATH_continue, 'w') as file:
            global continue_data
            continue_data = [None, None]
            json.dump(continue_data, file, indent=4)
    if not os.path.exists(PATH_settings):
        with open(PATH_settings, 'w') as file:
            global settings
            settings = [True, "Używa doccli!", True]
            json.dump(settings, file, indent=4)
    if not os.path.exists(PATH_history):
        with open(PATH_history, 'w') as file:
            file.write('[]')

    with open(PATH_mylist, 'r') as json_file:
        loaded_data = json.load(json_file)
        global mylist
        mylist = loaded_data

    with open(PATH_continue, 'r') as json_file:
        loaded_data = json.load(json_file)
        continue_data = loaded_data

    with open(PATH_history, 'r') as json_file:
        loaded_data = json.load(json_file)
        global history
        history = loaded_data

    with open(PATH_settings, 'r') as json_file:
        loaded_data = json.load(json_file)
        settings = loaded_data
        # New update bypass
        if len(settings) != 3:
            settings.append(True)
            save()


def save():
    with open(PATH_mylist, 'w') as json_file:
        json.dump(mylist, json_file, indent=4)
    with open(PATH_continue, 'w') as json_file:
        json.dump(continue_data, json_file, indent=4)
    with open(PATH_settings, 'w') as json_file:
        json.dump(settings, json_file, indent=4)
    with open(PATH_history, 'w') as json_file:
        json.dump(history, json_file, indent=4)
