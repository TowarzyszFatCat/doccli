import os
import sys
import re
import time
import shutil
import tempfile
import webbrowser
import subprocess
from subprocess import Popen, DEVNULL
import threading
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
from anilist_connector import get_details_from_anilist, update_anilist_progress, get_anilist_plan_to_watch, sync_anilist_list_status, get_anilist_history, get_duration_by_malid, sync_history_with_anilist
from player import mpv_play, kill_process, delayed_tracker
from local_lib import m_local_library


def m_welcome():

    preload_series_cache()
    sync_history_with_anilist()

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

    prompt_txt = 'Wybierz co chcesz zrobić: '

    # Status anilist
    has_token = ds.settings.get("anilist_token") != ""
    
    if has_token:
        status_txt = "🟢 STATUS: Połączono z kontem AniList!"
    else:
        status_txt = "🔴 STATUS: Brak połączenia z AniList (Skonfiguruj w Ustawieniach)"    

    dynamic_menu_art = MAIN_MENU + "\n" + status_txt + "\n"

    ans = open_menu(choices=choices, prompt=prompt_txt, height=10, message=dynamic_menu_art)

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
    current_dl_path = ds.settings.get("download_path", "") if ds.settings.get("download_path", "") != "" else "Domyślny"
    current_quality = ds.settings.get("player_quality", "best")

    choices = [
        "Ustawienia Discord RPC",
        "Połącz / Zaktualizuj konto AniList",
        f"Zmień folder pobierania (Obecnie: {current_dl_path})",
        f"Zmień domyślną jakość wideo (Obecnie: {current_quality})",
        "Wróć do menu głównego"
    ]
    
    prompt_text = 'Wybierz co chcesz skonfigurować: '
    ans = open_menu(choices=choices, prompt=prompt_text, height=7)
    
    if ans == choices[0]:
        rpc_choices = [{
                "type": "list",
                "message": "Czy chcesz aby znajomi na discordzie widzieli co oglądasz?",
                "choices": ["Tak", "Nie"],
            }]
        res = prompt(questions=rpc_choices)

        if res[0] == "Nie":
            ds.settings["rpc_enabled"] = False
            ds.save()
            m_welcome()
        if res[0] == "Tak":
            clear()
            ds.settings["rpc_enabled"] = True
            choices2 = [{"type": "input", "message": "Wpisz co tylko zechcesz! Będzie to wyświetlane w II linijce statusu. Zostaw puste jeśli chcesz aby był wyświetlany domyślny status. [Minimalnie 2 znaki] (Domyślna wartość: 'Używa doccli!') \n", "name": "status_dc"}]
            res2 = prompt(questions=choices2)

            if not res2['status_dc'] == "" and len(res2['status_dc']) > 1:
                ds.settings["rpc_status"] = res2['status_dc']
                ds.save()
                m_welcome()
            else:
                ds.settings["rpc_status"] = 'Używa doccli!'
                ds.save()
                m_welcome()
                
    elif ans == choices[1]:
        clear()
        CLIENT_ID = "16904"
        print(colored("Zaraz otworzy się przeglądarka z prośbą o autoryzację aplikacji doccli na Twoim koncie AniList.", "cyan"))
        print(colored("Po zatwierdzeniu, skopiuj Token (długi ciąg znaków) i wklej go poniżej.\n", "cyan"))
        
        auth_url = f"https://anilist.co/api/v2/oauth/authorize?client_id={CLIENT_ID}&response_type=token"
        try:
            webbrowser.open(auth_url)
        except:
            print(colored(f"Nie udało się otworzyć przeglądarki! Wejdź ręcznie w ten link:\n{auth_url}\n", "yellow"))
            
        questions = [{"type": "input", "message": "Wklej swój AniList Access Token (lub zostaw puste by anulować):", "name": "token"}]
        res = prompt(questions)
        
        if res['token']:
            ds.settings["anilist_token"] = res['token'].strip()
            ds.save()
            print(colored("\n[+] Pomyślnie zapisano token! Od teraz doccli będzie automatycznie zapisywać postęp.", "green"))
            time.sleep(3)
        m_settings()

    elif ans == choices[2]:
        clear()
        print(colored(f"[INFO] Obecny folder pobierania: {current_dl_path}", "cyan"))
        print(colored("Wpisz pełną ścieżkę do nowego folderu (np. D:\\Anime lub /home/user/Wideo).", "yellow"))
        print(colored("Zostaw to pole puste i wciśnij ENTER, aby przywrócić domyślny folder wewnątrz programu.\n", "yellow"))
        
        questions = [{"type": "input", "message": "Podaj nową ścieżkę:", "name": "new_path"}]
        res = prompt(questions)
        new_input = res['new_path'].strip()
        
        if new_input == "":
            ds.settings["download_path"] = ""
            ds.save()
            print(colored("\n[+] Przywrócono domyślny folder pobierania!", "green"))
        else:
            try:
                # Tworzy podany folder, jeśli jeszcze nie istnieje
                os.makedirs(new_input, exist_ok=True)
                ds.settings["download_path"] = new_input
                ds.save()
                print(colored(f"\n[+] Pomyślnie zmieniono folder zapisu na: {new_input}", "green"))
            except Exception as e:
                print(colored(f"\n[-] Błąd podczas tworzenia folderu (Nieprawidłowa ścieżka?): {e}", "red"))
        
        time.sleep(3)
        m_settings()
        
    elif ans == choices[3]:
        quality_choices = ["Źródłowa", "1080p", "720p", "480p", "360p", "Cofnij"]
        chosen = open_menu(choices=quality_choices, prompt="Wybierz domyślną jakość dla odtwarzacza:", height=7)
        
        if chosen != "Cofnij":
            if chosen == "Źródłowa" or chosen.startswith("best"):
                ds.settings["player_quality"] = "best"
            else:
                ds.settings["player_quality"] = chosen
            ds.save()
            print(colored(f"\n[+] Pomyślnie zmieniono jakość na: {ds.settings['player_quality']}", "green"))
            time.sleep(2)
        m_settings()

    elif ans == choices[4]:
        m_welcome()


def m_discord():
    webbrowser.open('https://discord.gg/Y4RcwbE5CJ')
    m_welcome()


def m_mylist():
    has_token = ds.settings.get("anilist_token") != ""
    
    if has_token:
        clear()
        print(colored("[INFO] Trwa automatyczna synchronizacja z AniList...", "cyan"))
        
        token = ds.settings["anilist_token"]
        mal_ids = get_anilist_plan_to_watch(token)
        
        if mal_ids is not None:
            all_series = get_cached_series_list()
            
            for series in all_series:
                if series['mal_id'] in mal_ids:
                    if series not in ds.mylist:
                        ds.mylist.append(series)
                        
            for local_anime in ds.mylist:
                if local_anime['mal_id'] not in mal_ids:
                    threading.Thread(target=sync_anilist_list_status, args=(local_anime['mal_id'], token, True), daemon=True).start()
                        
            ds.save()

    choices = ['Cofnij']
    
    display_list = list(reversed(ds.mylist))
    
    for element in display_list:
        choices.append(f"{element['title']} | {element['title_en']}")

    prompt_txt = 'Wybierz anime: '
    ans = open_menu(choices=choices, prompt=prompt_txt, message=MOJA_LISTA)
    
    if ans == choices[0]:
        m_welcome()
    else:
        index = choices.index(ans)
        m_details(display_list[index - 1])


def m_history():
    choices = ['Cofnij']
    display_map = {}
    
    for item in ds.history[:50]:  
        display_text = f"[{item['dt_string']}] [{item['source']}] {item['title']} [Odc: {item['episode']}]"
        choices.append(display_text)
        display_map[display_text] = item

    prompt = 'Wybierz wpis aby przejść do szczegółów: '
    ans = open_menu(choices=choices, prompt=prompt, message=HISTORIA)
    
    if ans == choices[0]:
        m_welcome()
    else:
        selected_item = display_map[ans]
        if selected_item.get('slug'):
            details = get_details_for_serie(selected_item['slug'])
            if details and details != 404:
                m_details(details)
            else:
                print(colored("Błąd: Nie udało się pobrać szczegółów z serwera.", "red"))
                time.sleep(2)
                m_history()
        else:
            print(colored("To anime nie ma przypisanego profilu w Docchi.", "yellow"))
            time.sleep(3)
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
    
    choices = [serie[search_key] for serie in all_series_json]
    choices.append("Cofnij")
    
    prompt = 'Szukaj: '
    ans = open_menu(choices=choices, prompt=prompt, message=SZUKAJ)
    
    if ans == "Cofnij":
        m_find()
        return
        
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
        "Pobierz cały sezon",
        "Pobierz wybrane odcinki"
    ]

    if details in ds.mylist:
        choices.append("Usuń z mojej listy")
    else:
        choices.append("Dodaj do mojej listy")

    choices.append("Wyszukiwarka")
    choices.append("Menu główne")

    prompt_txt = 'Wybierz co chcesz zrobić: '

    genres = "[ "
    for genre in details['genres']:
        genres += genre + ","

    genres += " ]"

    stars, description, episode_count = get_details_from_anilist(str(details["mal_id"]))

    max_ep = episode_count if isinstance(episode_count, int) else 9999

    ans = open_menu(
        choices=choices,
        prompt=prompt_txt,
        qmark=f'{details["title"]} / {details["title_en"]} \n [Ilość odcinków: {episode_count}] [Ocena: {stars}]',
        message=genres,
        height=7,
        image=details['cover'],
        description=description 
    )

    if ans == choices[0]:
        ds.continue_data[0] = details
        w_first(details['slug'])
        
    elif ans == choices[1]:
        ds.continue_data[0] = details
        w_list(details['slug'])
        
    elif ans == choices[2]: 
        w_download_season(details['slug'], details['title'], base_download_dir=ds.settings["download_path"])
        m_details(details)
        
    elif ans == choices[3]: 
        questions = [{
            "type": "input", 
            "message": f"Wpisz numery do pobrania (np. 3 lub 4-6 lub 1,3,5 lub 1,7-8,11) [Wszystkich odc: {episode_count}]:", 
            "name": "episodes_input"
        }]
        res = prompt(questions)
        
        if res['episodes_input']:
            episodes_to_download = set()
            
            for part in res['episodes_input'].split(','):
                part = part.strip()
                if not part: 
                    continue
                    
                if '-' in part:
                    try:
                        start, end = map(int, part.split('-'))
                        start, end = min(start, end), max(start, end)
                        start_safe = max(1, start)
                        end_safe = min(max_ep, end)
                        episodes_to_download.update(range(start_safe, end_safe + 1))
                    except ValueError: 
                        pass 
                else:
                    try:
                        ep = int(part)
                        if 1 <= ep <= max_ep:
                            episodes_to_download.add(ep)
                    except ValueError: 
                        pass 

            ep_list = sorted(list(episodes_to_download))
            
            if not ep_list:
                print(colored("Błąd: Nie podano poprawnych numerów odcinków!", "red"))
                time.sleep(2)
            else:
                w_download_season(details['slug'], details['title'], ep_list, base_download_dir=ds.settings["download_path"])
                
        m_details(details)
        
    elif ans == choices[4]:
        has_token = ds.settings.get("anilist_token") != ""
        token = ds.settings["anilist_token"] if has_token else ""
        
        if details in ds.mylist:
            ds.mylist.remove(details)
            ds.save()
            if has_token:
                threading.Thread(target=sync_anilist_list_status, args=(details['mal_id'], token, False), daemon=True).start()
            m_details(details)
        else:
            ds.mylist.append(details)
            ds.save()
            if has_token:
                threading.Thread(target=sync_anilist_list_status, args=(details['mal_id'], token, True), daemon=True).start()
            m_details(details)
            
    elif ans == choices[5]:
        m_find()
        
    elif ans == choices[6]:
        m_welcome()


def w_first(SLUG):
    ds.continue_data[1] = 1
    ds.save()
    w_players(SLUG, 1)


def w_list(SLUG):
    # Pobieramy dane o anime, w które właśnie kliknęliśmy (m_details je tam zapisało przed wywołaniem w_list)
    details = ds.continue_data[0]
    
    last_episode = 0
    
    # BŁYSKAWICZNA ŚCIEŻKA
    if details and details.get('slug') == SLUG and details.get('mal_id'):
        stars, desc, ep_count = get_details_from_anilist(str(details['mal_id']))
        
        if isinstance(ep_count, int):
            last_episode = ep_count
            
        elif isinstance(ep_count, str) and "Wydano:" in ep_count:
            match = re.search(r'Wydano:\s*(\d+)', ep_count)
            if match:
                last_episode = int(match.group(1))

    # ŚCIEŻKA AWARYJNA
    if last_episode <= 0:
        clear()
        print(colored("[INFO] Trwa pobieranie ilości odcinków z bazy... (Może to potrwać dłuższą chwilę)", "yellow"))
        last_episode = get_episodes_count_for_serie(SLUG)

    if last_episode == 404 or last_episode <= 0:
        clear()
        print(colored("Nie znaleziono strony lub brak dostępnych odcinków [Błąd 404]", "red"))
        time.sleep(3)
        fallback_details = details if details else get_details_for_serie(SLUG)
        m_details(fallback_details)
        return

    choices = list(range(1, last_episode + 1))
    choices.append('Cofnij')

    prompt = 'Wybierz odcinek: '

    ans = open_menu(choices=choices, prompt=prompt)
    
    if ans == "Cofnij":
        fallback_details = details if details else get_details_for_serie(SLUG)
        m_details(fallback_details)
    else:
        ds.continue_data[1] = ans
        ds.save()
        w_players(SLUG, ans)


def w_players(SLUG, NUMBER, err=''):
    players = []

    if get_players_list(SLUG, NUMBER) == 404:
        clear()
        print(colored("Nie znaleziono strony [Błąd 404]", "red"))
        time.sleep(3)
        m_details(get_details_for_serie(SLUG))

    for player in get_players_list(SLUG, NUMBER):
        player_info = [player['player_hosting'], player['player']]
        players.append(player_info)

    print(colored("Trwa analizowanie, sprawdzanie źródeł na żywo i pobieranie jakości...", "cyan"))
    
    def check_link(player):
        hosting_name, url = player[0], player[1]
        url_lower = url.lower()
        
        if "lycoris" in url_lower:
            direct = extract_lycoris_direct_link(url)
            return ("ok", "Auto") if direct else ("error", "")
            
        elif "mega" in url_lower:
            return ("mega", "MEGA") if shutil.which('megatools') is not None else ("error", "")
            
        else:
            try:
                res = subprocess.run(
                    ["yt-dlp", "--print", "%(resolution)s", "--no-warnings", url],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=15 
                )
                
                if res.returncode == 0:
                    lines = [l for l in res.stdout.strip().split('\n') if l]
                    if lines and lines[-1] != "NA":
                        raw_res = lines[-1].strip().lower()
                        
                        # --- UNIFIKACJA ROZDZIELCZOŚCI ---
                        if "x" in raw_res:
                            # Przerabia "1920x1080" na "1080p"
                            resolved_res = f"{raw_res.split('x')[-1]}p"
                        elif raw_res.isdigit():
                            # Przerabia samo "1080" na "1080p"
                            resolved_res = f"{raw_res}p"
                        else:
                            # Zostawia w spokoju to, co już ma np. "1080p"
                            resolved_res = raw_res
                    else:
                        resolved_res = "Nieznana"
                        
                    return ("ok", resolved_res)
                    
                # System zapasowy dla źródeł odrzucających komendę --print
                res_fallback = subprocess.run(
                    ["yt-dlp", "-q", "--simulate", "--no-warnings", url],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=15 
                )
                
                if res_fallback.returncode == 0:
                    return ("ok", "Nieznana")
                    
                return ("error", "")
            except:
                return ("error", "")

    with ThreadPoolExecutor(max_workers=15) as executor:
        results = list(executor.map(check_link, players))

    choices = []
    
    for player, result in zip(players, results):
        status, res_text = result
        hosting_name = str(player[0])
        source_link = player[1]

        if status == "ok":
            prefix = f"✅ [{res_text}] "
        elif status == "mega":
            prefix = "🟡 [MEGA] "
        else:
            prefix = "❌ [Brak] "
            
        display_line = (prefix + hosting_name).ljust(40) + " | Link źródła: " + source_link
        choices.append(display_line)

    current_quality = ds.settings.get("player_quality", "best")
    choices.append(f"Zmień maksymalną jakość (Obecnie: {current_quality})")
    choices.append("Wróć do menu")

    prompt = 'Wybierz źródło: '
    ans = open_menu(choices=choices, prompt=prompt, qmark=err)

    if ans == choices[-1]: # Wróć do menu
        m_welcome()
        return
        
    if ans == choices[-2]: # Zmiana jakości
        quality_choices = ["Źródłowa", "1080p", "720p", "480p", "360p"]
        chosen = open_menu(choices=quality_choices, prompt="Wybierz preferowaną jakość:", height=6)
        
        if chosen == "Źródłowa" or chosen.startswith("best"):
            ds.settings["player_quality"] = "best"
        else:
            ds.settings["player_quality"] = chosen
            
        ds.save() # Zapisujemy od razu na dysk!
        w_players(SLUG, NUMBER, err=f'Zmieniono jakość odtwarzacza na {ds.settings["player_quality"]}')
        return

    ans_index_in_choices = choices.index(ans)
    ans_index = players[ans_index_in_choices]

    process = mpv_play(ans_index[1], quality=ds.settings.get("player_quality", "best"))

    print("Rozpoczynanie odtwarzania...")
    time.sleep(3)                                      
    if process == None or process.poll() is not None:
        w_players(SLUG, NUMBER, err='Wybrane źródło nie jest dostępne, lub nie jest wspierane!')

    w_default(SLUG, NUMBER, process)


def w_default(SLUG, NUMBER, process):
    details = ds.continue_data[0]
    if not details or details.get('slug') != SLUG:
        details = get_details_for_serie(SLUG)
        
    how_many_episodes = 0
    
    # BŁYSKAWICZNA ŚCIEŻKA
    if details and details.get('mal_id'):
        stars, desc, ep_count = get_details_from_anilist(str(details['mal_id']))
        
        if isinstance(ep_count, int):
            how_many_episodes = ep_count
        elif isinstance(ep_count, str) and "Wydano:" in ep_count:
            match = re.search(r'Wydano:\s*(\d+)', ep_count)
            if match:
                how_many_episodes = int(match.group(1))

    # ŚCIEŻKA AWARYJNA
    if how_many_episodes <= 0:
        clear()
        print(colored("[INFO] Trwa pobieranie ilości odcinków z bazy... (Może to potrwać dłuższą chwilę)", "yellow"))
        how_many_episodes = get_episodes_count_for_serie(SLUG)
        if how_many_episodes == 404:
            how_many_episodes = NUMBER 

    if ds.settings["rpc_enabled"]:
        update_rpc(f"Ogląda: {details.get('title', 'Anime')} [{str(NUMBER)}/{str(how_many_episodes)}]", ds.settings["rpc_status"])
    else:
        update_rpc(f"Ogląda anime", ds.settings["rpc_status"])

    threading.Thread(target=delayed_tracker, args=(details, NUMBER, process, how_many_episodes), daemon=True).start()

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
        next_ep = NUMBER + 1 if NUMBER < how_many_episodes else NUMBER
        ds.continue_data[1] = next_ep
        ds.save()
        w_players(SLUG, next_ep)
        
    elif ans == choices[2]:
        kill_process(process)
        update_rpc("Menu główne", "Szuka anime do obejrzenia...")
        prev_ep = NUMBER - 1 if NUMBER >= 2 else NUMBER
        ds.continue_data[1] = prev_ep
        ds.save()
        w_players(SLUG, prev_ep)
        
    elif ans == choices[3]:
        kill_process(process)
        update_rpc("Menu główne", "Szuka anime do obejrzenia...")
        w_list(SLUG)
        
    elif ans == choices[4]:
        kill_process(process)
        update_rpc("Menu główne", "Szuka anime do obejrzenia...")
        m_welcome()
