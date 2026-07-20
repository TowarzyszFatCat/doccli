import pathlib
import sys
import time
import re
import tempfile
import subprocess
import json
from InquirerPy import inquirer, prompt
from PIL import Image
import os
import textwrap
from os import system
from docchi_api_connector import get_series_list, get_episodes_count_for_serie, get_players_list, get_details_for_serie, extract_lycoris_direct_link #, get_skip_times
from anilist_connector import get_trending_anime_malids, get_details_from_anilist
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn, TaskProgressColumn
from menus_decor import MAIN_MENU, SZUKAJ, NA_CZASIE, MOJA_LISTA, HISTORIA, MOJA_BIBLIOTEKA
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
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.console import Group
from rich.align import Align

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


def open_menu(choices, prompt='Prompt', border=True, qmark='', message='', pointer='>', cycle=True, height=10, image=None, description=None):
    clear()

    # nie mam pojęcia co tu sie dzieje ale działa
    if image:
        try:
            response = requests.get(image)
            image_path = os.path.join(tempfile.gettempdir(), "cover.png")
            with open(image_path, 'wb') as file:
                file.write(response.content)

            term_width, term_height = get_terminal_size()
            
            avail_height = max(5, term_height - height - 6) 
            chafa_height = max(3, avail_height)

            img_ratio = 0.7
            margin_ratio = 0.0

            try:
                img = Image.open(image_path).convert("RGBA")
                img_w, img_h = img.size
                
                pad_pixels = int(img_w * 0.15) 
                new_w = pad_pixels + img_w
                
                padded_img = Image.new("RGBA", (new_w, img_h), (0, 0, 0, 0))
                padded_img.paste(img, (pad_pixels, 0))
                padded_img.save(image_path, "PNG")
                
                img_ratio = new_w / img_h
                margin_ratio = pad_pixels / img_h
            except Exception:
                pass

            if shutil.which('chafa') is not None:
                char_aspect = 2.0 
                chafa_units_h = chafa_height * char_aspect
                
                rendered_cols = int(chafa_units_h * img_ratio)
                margin_cols = int(chafa_units_h * margin_ratio)
                
                text_start_col = rendered_cols + margin_cols + 4
                
                if text_start_col >= term_width - 15:
                    text_start_col = int(term_width * 0.4)
                    
                text_width = term_width - text_start_col - 2

                print("\0337", end="")
                sys.stdout.flush()

                os.system(f"chafa -s {term_width}x{chafa_height} {image_path}")
                
                if description:
                    clean_desc = description.replace('<br>', '\n')
                    wrapped_desc = textwrap.wrap(clean_desc, width=text_width)
                    
                    header_text = "Tłumaczenie maszynowe opisu z AniList:"
                    colored_header = colored(header_text, "cyan") 
                    
                    wrapped_desc.insert(0, colored_header)
                    wrapped_desc.insert(1, "") 
                else:
                    wrapped_desc = []

                for i, line in enumerate(wrapped_desc[:avail_height]):
                    row = i + 2 
                    print(f"\033[{row};{text_start_col}H{line}", end="")

                menu_row = avail_height + 2
                print(f"\033[{menu_row};1H", end="")
                sys.stdout.flush()
                    
            else:
                print(center_text("Brak narzędzia 'chafa' do wyświetlania okładek."))
                
        except Exception as e:
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
        if not continue_data:
            m_welcome()
        else:
            w_players(continue_data[0]['slug'], continue_data[1])

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
    elif ans == choices[8]:
        m_discord()
    elif ans == choices[9]:
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


def get_folder_size(folder_path="doccli_downloads"):
    total_size = 0
    if os.path.exists(folder_path):
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
    return total_size

def get_user_rank(hours):
    if hours < 10:
        return "[cyan]🌱 Niedzielny Widz[/cyan]"
    elif hours < 25:
        return "[green]🌸 Nowicjusz[/green]"
    elif hours < 50:
        return "[orange]🗡️ Uczeń Shounenów[/orange]"
    elif hours < 100:
        return "[blue]🥷 Genin[/blue]"
    elif hours < 250:
        return "[violet]⭐ Otaku[/violet]"
    elif hours < 500:
        return "[magenta]⚔️ Łowca Demonów[/magenta]"
    elif hours < 1000:
        return "[red]🔥 Weteran [/red]"
    else:
        return "[yellow]👑 Hikikomori[yellow]"

def m_stats():
    clear()

    ep_played = len(history)
    q_mylist = len(mylist)

    ti_c = pathlib.Path(PATH_config).stat().st_mtime
    dt_c = datetime.fromtimestamp(ti_c).strftime("%d/%m/%Y")

    creation_dt = date.fromtimestamp(ti_c)
    now_dt = date.today()
    delta_dt = now_dt - creation_dt

    total_minutes = ep_played * 21
    hours = total_minutes // 60
    minutes = total_minutes % 60
    
    size_bytes = get_folder_size()
    size_gb = round(size_bytes / (1024 ** 3), 2)

    last_watched = "Brak danych"
    if history:
        raw_history = str(history[0]) 
        if "]" in raw_history:
            clean_title = raw_history.split("]", 1)[1].strip()
        else:
            clean_title = raw_history
            
        if len(clean_title) > 35:
            last_watched = clean_title[:32] + "..."
        else:
            last_watched = clean_title

    user_rank = get_user_rank(hours)

    console = Console()

    # AKTYWNOŚĆ
    table_activity = Table(show_header=False, box=None, padding=(0, 2))
    table_activity.add_column("Statystyka", style="cyan", width=25)
    table_activity.add_column("Wartość", justify="right", style="bold")
    table_activity.add_row("Obecna Ranga:", user_rank)
    table_activity.add_row("Odtworzone odcinki:", f"[bold red]{ep_played}[/bold red]")
    table_activity.add_row("Czas oglądania (21m/odc):", f"[yellow]{hours}h {minutes}m[/yellow]")
    table_activity.add_row("Ostatnio oglądane:", f"[magenta]{last_watched}[/magenta]")

    # BIBLIOTEKA
    table_app = Table(show_header=False, box=None, padding=(0, 2))
    table_app.add_column("Statystyka", style="cyan", width=25)
    table_app.add_column("Wartość", justify="right", style="bold")
    table_app.add_row("Zapisane na liście:", f"[bold red]{q_mylist}[/bold red]")
    table_app.add_row("Zajęte miejsce na dysku:", f"[green]{size_gb} GB[/green]")
    table_app.add_row("Pierwsza instalacja doccli:", f"[white]{dt_c}[/white]")
    table_app.add_row("Wiek profilu:", f"[white]{delta_dt.days} dni[/white]")

    # RANGI
    table_legend = Table(show_header=False, box=None, padding=(0, 2))
    table_legend.add_column("Ranga", style="bold", width=30) 
    table_legend.add_column("Wymaganie", justify="right", style="dim white")
    table_legend.add_row("[cyan]🌱 Niedzielny Widz[/cyan]", "0 - 9 godz.")
    table_legend.add_row("[green]🌸 Nowicjusz[/green]", "10 - 24 godz.")
    table_legend.add_row("[yellow]🗡️ Uczeń Shounenów[/yellow]", "25 - 49 godz.")
    table_legend.add_row("[blue]🥷 Genin[/blue]", "50 - 99 godz.")
    table_legend.add_row("[violet]⭐ Otaku[/violet]", "100 - 249 godz.")
    table_legend.add_row("[magenta]⚔️ Łowca Demonów[/magenta]", "250 - 499 godz.")
    table_legend.add_row("[red]🔥 Weteran [/red]", "500 - 999 godz.")
    table_legend.add_row("[yellow]👑 Hikikomori[yellow]", "1000+ godz.")


    panel_activity = Panel(table_activity, title="[bold yellow]🎬 Twój Profil[/bold yellow]", border_style="cyan", expand=False)
    panel_app = Panel(table_app, title="[bold yellow]📁 Biblioteka i Dane[/bold yellow]", border_style="cyan", expand=False)
    panel_legend = Panel(table_legend, title="[bold yellow]🏆 Legenda Rang[/bold yellow]", border_style="cyan", expand=False)


    dashboard = Group(
        Align.center(panel_activity),
        Align.center(panel_app),
        Align.center(panel_legend)
    )

    main_panel = Panel(
        dashboard, 
        title="[bold magenta]📊 STATYSTYKI DOCCLI[/bold magenta]", 
        border_style="blue", 
        expand=False,
        padding=(1, 4)
    )

    console.print(Align.center(main_panel))
    
    print('\n')
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
    print(colored(f"[INFO] Przygotowywanie do pobrania {TITLE} ({how_many_episodes} odcinki)...", "cyan"))
    print(colored(f"[INFO] Lokalizacja zapisu: {series_dir}", "yellow"))
    
    for ep_number in range(1, how_many_episodes + 1):
        players = get_players_list(SLUG, ep_number)
        
        if players == 404 or not players:
            print(colored(f"\n[BŁĄD] Nie znaleziono źródeł dla odcinka {ep_number}. Pomijam...", "red"))
            continue
        
        file_name_template = os.path.join(series_dir, f"{safe_title} - Odcinek {ep_number:02d}.%(ext)s")
        downloaded = False
        total_sources = len(players)

        for index, player in enumerate(players, 1):
            target_url = player['player']

            if "lycoris" in target_url.lower():
                extracted = extract_lycoris_direct_link(target_url)
                if extracted:
                    target_url = extracted
            
            print(f"\r\033[K" + colored(f"[*] Sprawdzam źródło {index}/{total_sources} (Odcinek {ep_number}/{how_many_episodes})...", "yellow"), end="", flush=True)
            
            command = [
                "yt-dlp",
                "--newline",
                "--no-warnings",
                "--merge-output-format", "mp4",
                target_url,
                "-o",
                file_name_template
            ]
            
            print()
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold cyan]{task.description}"),
                BarColumn(bar_width=40, complete_style="green", finished_style="bold green"),
                TaskProgressColumn(),
                TimeRemainingColumn(),
            ) as progress:                
                task_id = progress.add_task(description=f"Pobieranie odc. {ep_number} [bold yellow](Ścieżka VIDEO)", total=100)
                
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                
                current_percent = 0.0

                for line in process.stdout:
                    match = re.search(r'\[download\]\s+([\d\.]+)%', line)
                    if match:
                        try:
                            percent = float(match.group(1))
                            
                            if percent < current_percent - 50:
                                progress.update(task_id, description=f"Pobieranie odc. {ep_number} [bold yellow](Ścieżka AUDIO)")
                                
                            current_percent = percent
                            progress.update(task_id, completed=percent)
                        except ValueError:
                            pass
                            
                process.wait()
                
                if process.returncode == 0:
                    downloaded = True
                    progress.update(task_id, completed=100, description=f"[bold green]Ukończono odc. {ep_number}!")
                    break

        if not downloaded:
            print(colored(f"[BŁĄD] Żadne ze źródeł dla odcinka {ep_number} nie zadziałało.", "red"))
        
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
                history.insert(0, f"[{dt_string}] {selected_series} | Offline [{ep}]")
                save()
                
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
            history.insert(0, f"[{dt_string}] {selected_series} | Offline [{selected_ep}]")
            save()
            
            try:
                subprocess.run(["mpv", file_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except FileNotFoundError:
                print(colored("[BŁĄD] Nie znaleziono odtwarzacza mpv!", "red"))
                input("Naciśnij Enter...")
                m_welcome()
                return


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
