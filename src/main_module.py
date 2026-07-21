import os
import sys
import time
import shutil
import tempfile
import webbrowser
import subprocess
from subprocess import Popen, DEVNULL
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# From pip
from termcolor import colored
from InquirerPy import prompt

# Doccli modules
from storage import ds
from cache import preload_series_cache, get_cached_series_list, get_cached_trending_list
from ui_utils import clear, open_menu
from downloader import w_download_season
from stats import m_stats
from menus_decor import MAIN_MENU, SZUKAJ, NA_CZASIE, MOJA_LISTA, HISTORIA, MOJA_BIBLIOTEKA
from discord_integration import update_rpc, set_running
from docchi_api_connector import get_episodes_count_for_serie, get_players_list, get_details_for_serie, extract_lycoris_direct_link
from anilist_connector import get_details_from_anilist


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


def m_welcome():

    preload_series_cache()

    update_rpc("Menu główne", "Szuka anime do obejrzenia...")

    choices = [
        "Wyszukaj",
        "Anime na czasie"
    ]

    if ds.continue_data[0] is None:
        choices.append("Nie masz nic do wznowienia")
    else:
        choices.append(f"Wznów {ds.continue_data[0]['title']} / {ds.continue_data[0]['title_en']}, Odc: {ds.continue_data[1]}")

    choices.append("Moja Biblioteka (Offline)")
    choices.append("Moja lista")
    choices.append("Historia oglądania")
    choices.append("Ustawienia")
    choices.append("Statystyki doccli")
    choices.append("Dołącz do discorda")
    choices.append("Zamknij")

    prompt = 'Wybierz co chcesz zrobić: '

    ans = open_menu(choices=choices, prompt=prompt, height=10, message=MAIN_MENU)

    if ans == choices[0]:
        m_find()
    elif ans == choices[1]:
        m_trending()
    elif ans == choices[2]:
        if not ds.continue_data:
            m_welcome()
        else:
            w_players(ds.continue_data[0]['slug'], ds.continue_data[1])

    elif ans == choices[3]:
        m_local_library()
    elif ans == choices[4]:
        m_mylist()
    elif ans == choices[5]:
        m_history()
    elif ans == choices[6]:
        m_settings()
    elif ans == choices[7]:
        m_stats()
        m_welcome()
    elif ans == choices[8]:
        m_discord()
    elif ans == choices[9]:
        set_running(False)
        sys.exit()

def m_settings():

    choices = [{
            "type": "list",
            "message": "Czy chcesz aby znajomi na discordzie widzieli co oglądasz?",
            "choices": ["Tak", "Nie"],
        }]

    res = prompt(questions=choices)

    if res[0] == "Nie":
        ds.settings[0] = False
        ds.save()
        m_welcome()
    if res[0] == "Tak":
        clear()
        ds.settings[0] = True
        choices2 = [{"type": "input", "message": "Wpisz co tylko zechcesz! Będzie to wyświetlane w II linijce statusu. Zostaw puste jeśli chcesz aby był wyświetlany domyślny status. [Minimalnie 2 znaki] (Domyślna wartość: 'Używa doccli!') \n", "name": "status_dc"}]
        res2 = prompt(questions=choices2)

        if not res2['status_dc'] == "" and len(res2['status_dc']) > 1:
            ds.settings[1] = res2['status_dc']
            ds.save()
            m_welcome()
        else:
            ds.settings[1] = 'Używa doccli!'
            ds.save()
            m_welcome()


def m_discord():
    webbrowser.open('https://discord.gg/Y4RcwbE5CJ')
    m_welcome()


def m_mylist():
    choices = ['Cofnij']

    for element in ds.mylist:
        choices.append(f"{element['title']} | {element['title_en']}")

    prompt = 'Wybierz anime: '
    ans = open_menu(choices=choices, prompt=prompt, message=MOJA_LISTA)
    if ans == choices[0]:
        m_welcome()
    else:
        index = choices.index(ans)
        m_details(ds.mylist[index - 1])


def m_history():
    choices = ['Cofnij']

    for element in ds.history:
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

    if details in ds.mylist:
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

    # 1. Pobieramy ocenę i opis z nowej funkcji (pamiętaj by zaktualizować importy na górze pliku!)
    stars, description = get_details_from_anilist(str(details["mal_id"]))

    # 2. Wywołujemy open_menu przekazując zmienną 'description' i zmienione 'stars'
    ans = open_menu(
        choices=choices, 
        prompt=prompt, 
        qmark=f'{details["title"]} / {details["title_en"]} \n [Ilość odcinków: {episode_count}] [Ocena: {stars}]', 
        message=genres, 
        height=6, 
        image=details['cover'],
        description=description  # <--- Dodany nowy parametr
    )

    if ans == choices[0]:
        ds.continue_data[0] = details
        w_first(details['slug'])
    elif ans == choices[1]:
        ds.continue_data[0] = details
        w_list(details['slug'])
    elif ans == choices[2]:
        w_download_season(details['slug'], details['title'])
        m_details(details)
    elif ans == choices[3]:
        if details in ds.mylist:
            ds.mylist.remove(details)
            ds.save()
            m_details(details)
        else:
            ds.mylist.append(details)
            ds.save()
            m_details(details)
    elif ans == choices[4]:
        m_find()
    elif ans == choices[5]:
        m_welcome()


def w_first(SLUG):
    ds.continue_data[1] = 1
    ds.save()
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
        ds.continue_data[1] = ans
        ds.save()

        w_players(SLUG, ans)


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

    if ds.settings[0]:
        update_rpc(f"Ogląda: {details['title']} [{str(NUMBER)}/{str(how_many_episodes)}]", ds.settings[1])
    else:
        update_rpc(f"Ogląda anime", ds.settings[1])

    # Save to history
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    ds.history.insert(0, f"[{dt_string}] {details['title']} / {details['title_en']} [Odc: {NUMBER}]")
    ds.save()

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
        ds.continue_data[1] = NUMBER + 1 if NUMBER < how_many_episodes else NUMBER
        ds.save()
        w_players(SLUG, NUMBER + 1 if NUMBER < how_many_episodes else NUMBER)
        
    elif ans == choices[2]:
        kill_process(process)
        update_rpc("Menu główne", "Szuka anime do obejrzenia...")
        ds.continue_data[1] = NUMBER - 1 if NUMBER >= 2 else NUMBER
        ds.save()
        w_players(SLUG, NUMBER - 1 if NUMBER >= 2 else NUMBER)
        
    elif ans == choices[3]:
        kill_process(process)
        update_rpc("Menu główne", "Szuka anime do obejrzenia...")
        w_list(SLUG)
        
    elif ans == choices[4]:
        kill_process(process)
        update_rpc("Menu główne", "Szuka anime do obejrzenia...")
        m_welcome()


def m_local_library():
    clear()
    
    current_dir = os.getcwd()
    downloads_dir = os.path.join(current_dir, "doccli_downloads")
    
    if not os.path.exists(downloads_dir):
        print(colored("[BŁĄD] Twój folder doccli_downloads jeszcze nie istnieje.", "red"))
        print(colored("Najpierw musisz pobrać jakieś anime!", "yellow"))
        print('')
        input(colored("Naciśnij Enter, aby wrócić do menu...", "yellow"))
        m_welcome()
        return
        
    series_list = [d for d in os.listdir(downloads_dir) if os.path.isdir(os.path.join(downloads_dir, d))]
    
    if not series_list:
        print(colored("[INFO] Twój folder doccli_downloads jest pusty.", "yellow"))
        print('')
        input(colored("Naciśnij Enter, aby wrócić do menu...", "yellow"))
        m_welcome()
        return
        
    series_list.append("Wróć do menu głównego")
    
    selected_series = open_menu(
        choices=series_list, 
        prompt='Wybierz serię z dysku: ', 
        height=10, 
        message=MOJA_BIBLIOTEKA
    )
    
    if selected_series == "Wróć do menu głównego":
        m_welcome()
        return

    while True:
        clear()
        series_path = os.path.join(downloads_dir, selected_series)
        
        episodes_list = [f for f in os.listdir(series_path) if os.path.isfile(os.path.join(series_path, f))]
        episodes_list.sort()
        
        if not episodes_list:
            print(colored(f"Brak plików wideo w folderze {selected_series}.", "red"))
            input(colored("Naciśnij Enter, aby wrócić do menu...", "yellow"))
            m_welcome()
            return
            
        choices = ["Oglądaj automatycznie"] + episodes_list + ["Wróć do wyboru serii"]
        
        selected_ep = open_menu(
            choices=choices, 
            prompt=f'Wybierz odcinek ({selected_series}): ', 
            height=10, 
            message=MOJA_BIBLIOTEKA
        )
        
        if selected_ep == "Wróć do wyboru serii":
            m_local_library()
            return
            
        elif selected_ep == "Oglądaj automatycznie":
            for ep in episodes_list:
                file_path = os.path.join(series_path, ep)
                clear()
                print(colored(f"Oglądanie automatyczne: {ep}", "cyan"))
                print(colored("Wciśnij 'Q' w obrębie okna MPV, lub zamknij je aby przerwać seans i wrócić do menu.", "white"))
                
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M")
                ds.history.insert(0, f"[{dt_string}] {selected_series} | Offline [{ep}]")
                ds.save()
                
                try:
                    process = subprocess.run(["mpv", file_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    
                    if process.returncode != 0:
                        print(colored("\n[INFO] Przerwano oglądanie automatyczne.", "yellow"))
                        input("Naciśnij Enter...")
                        break
                except FileNotFoundError:
                    print(colored("[BŁĄD] Nie znaleziono odtwarzacza mpv!", "red"))
                    input("Naciśnij Enter...")
                    m_welcome()
                    return
        else:
            file_path = os.path.join(series_path, selected_ep)
            clear()
            print(colored(f"Odtwarzam z dysku: {selected_ep}", "cyan"))
            print(colored("Wciśnij 'Q' w obrębie okna MPV, lub zamknij je aby przerwać seans i wrócić do menu.", "white"))
            
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M")
            ds.history.insert(0, f"[{dt_string}] {selected_series} | Offline [{selected_ep}]")
            ds.save()
            
            try:
                subprocess.run(["mpv", file_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except FileNotFoundError:
                print(colored("[BŁĄD] Nie znaleziono odtwarzacza mpv!", "red"))
                input("Naciśnij Enter...")
                m_welcome()
                return