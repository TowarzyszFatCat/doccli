import pathlib
import sys
import time
import json
from InquirerPy import inquirer, prompt
import os
from os import system
from api_connector import get_series_list, get_episodes_count_for_serie, get_players_list, get_details_for_serie
from subprocess import Popen, DEVNULL
from termcolor import colored
import webbrowser
from discord_integration import update_rpc, set_running
import platform
from zipfile import ZipFile
from datetime import datetime, date
import requests
import shutil


def clear():
    if platform.system() == "Linux" or platform.system() == "Darwin":
        system("clear")
    elif platform.system() == "Windows":
        system("cls")

def get_terminal_size():
    columns, rows = os.get_terminal_size()
    return columns, rows


def open_menu(choices, prompt='Prompt', border=True, qmark='', message='', pointer='>', cycle=True, height=10, image=None):
    clear()

    if image:
        if shutil.which('timg') is None:
            print(colored("[UWAGA]", "yellow"), colored("Aby wyświetlać okładki wymagana jest instalacja", "white"), colored("timg", "green"), '\n')
        else:
            response = requests.get(image)
            image_path = "/tmp/cover.jpg"
            with open(image_path, 'wb') as file:
                file.write(response.content)
            os.system(f"timg -C -g {get_terminal_size()[0]}x{get_terminal_size()[1] - height - 4} {image_path}")


    action = inquirer.fuzzy(
        message=message,    # Message above border
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

    update_rpc("Menu główne", "Szuka anime do obejrzenia...")

    choices = [
        "Wyszukaj",
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

    ans = open_menu(choices=choices, prompt=prompt, height=8)

    if ans == choices[0]:
        m_find()
    elif ans == choices[1]:
        if not continue_data:
            m_welcome()
        else:
            w_players(continue_data[0]['slug'], continue_data[1])
    elif ans == choices[2]:
        m_mylist()
    elif ans == choices[3]:
        m_history()
    elif ans == choices[4]:
        m_settings()
    elif ans == choices[5]:
        m_stats()
    elif ans == choices[6]:
        m_discord()
    elif ans == choices[7]:
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

    message = ''
    if not mylist:
        message = ("Nic tu nie ma!")

    for element in mylist:
        choices.append(f"{element['title']} | {element['title_en']}")

    prompt = 'Wybierz anime: '
    ans = open_menu(choices=choices, prompt=prompt, qmark=message)
    if ans == choices[0]:
        m_welcome()
    else:
        index = choices.index(ans)
        m_details(mylist[index - 1])

def m_history():
    choices = ['Cofnij']

    message = ''
    if not history:
        message = ("Nic tu nie ma!")

    for element in history:
        choices.append(element)

    prompt = 'Wyszukaj: '
    ans = open_menu(choices=choices, prompt=prompt, qmark=message)
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

    ans = open_menu(choices=choices, prompt=prompt, height=4)

    if ans == choices[0]:
        f_title()
    elif ans == choices[1]:
        f_title_EN()
    elif ans == choices[2]:
        f_malid()
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

def f_title():
    all_series_json = get_series_list()

    all_series_names = []

    for serie in all_series_json:
        all_series_names.append(serie['title'])

    choices = all_series_names

    prompt = 'Szukaj: '

    ans = open_menu(choices=choices, prompt=prompt)
    ans_index = all_series_names.index(ans)
    ans_details = all_series_json[ans_index]

    m_details(details=ans_details)


def f_title_EN():
    all_series_json = get_series_list()

    all_series_names = []

    for serie in all_series_json:
        all_series_names.append(serie['title_en'])

    choices = all_series_names

    prompt = 'Szukaj: '

    ans = open_menu(choices=choices, prompt=prompt)
    ans_index = all_series_names.index(ans)
    ans_details = all_series_json[ans_index]

    m_details(details=ans_details)


def f_malid():
    all_series_json = get_series_list()

    all_series_ids = []

    for serie in all_series_json:
        all_series_ids.append(serie['mal_id'])

    choices = all_series_ids

    prompt = 'Szukaj: '

    ans = open_menu(choices=choices, prompt=prompt)
    ans_index = all_series_ids.index(ans)
    ans_details = all_series_json[ans_index]

    m_details(details=ans_details)


def m_details(details):
    choices = [
        "Oglądaj od pierwszego odcinka",
        "Lista odcinków"
    ]

    if details in mylist:
        choices.append("Usuń z mojej listy")
    else:
        choices.append("Dodaj do mojej listy")

    choices.append("Cofnij do wyszukiwarki")
    choices.append("Menu główne")

    prompt = 'Wybierz co chcesz zrobić: '

    genres = "   [ "
    for genre in details['genres']:
        genres += genre + ", "

    genres += "]"

    episode_count = get_episodes_count_for_serie(details['slug'])

    ans = open_menu(choices=choices, prompt=prompt, qmark=f'{details["title"]} / {details["title_en"]} [{episode_count}]', message=genres, height=5, image=details['cover'])

    if ans == choices[0]:
        continue_data[0] = details
        w_first(details['slug'])
    elif ans == choices[1]:
        continue_data[0] = details
        w_list(details['slug'])
    elif ans == choices[2]:
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

    elif ans == choices[3]:
        m_find()
    elif ans == choices[4]:
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

    choices = [player[0] for player in players]

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
        w_players(SLUG, NUMBER, err='Wybrane źródło nie jest dostępne, lub nie jest wspierane! Możesz to złgosić na discordzie.')

    w_default(SLUG, NUMBER, process)


def mpv_play(URL):
    if shutil.which('mpv') is None:
        print(colored("[BŁĄD]", "red"), colored("Aby program działał wymagana jest instalacja", "white"), colored("mpv", "green"), '\n')
        sys.exit()
    if shutil.which('yt-dlp') is None:
        print(colored("[BŁĄD]", "red"), colored("Aby program działał wymagana jest instalacja", "white"), colored("yt-dlp", "green"), '\n')
        sys.exit()
    if "mega" in URL:
        if shutil.which('megatools') is None:
            print(colored("[UWAGA]", "yellow"), colored("Aby oglądać z tego źródła wymagana jest instalacja", "white"), colored("megatools", "green"), '\n')
            sys.exit()


        video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm']
        download_path = '/tmp/'
        files_in_directory = os.listdir(download_path)

        for file in files_in_directory:
            if file.lower().endswith(tuple(video_extensions)):
                file_path = os.path.join(download_path, file)
                os.remove(file_path)

        mega_url = URL.replace('embed', 'file')
        before_files = set(os.listdir(download_path))
        os.system(f'megadl {mega_url} --path {download_path}')
        after_files = set(os.listdir(download_path))
        new_files = after_files - before_files
        video_files = [file for file in new_files if file.lower().endswith(tuple(video_extensions))]

        try:
            process = Popen(args=['mpv' if platform.system() == "Linux" or platform.system() == "Darwin" else WIN_mpv, "--save-position-on-quit", f'/tmp/{video_files[0]}'], shell=False, stdout=DEVNULL, stderr=DEVNULL)
            return process
        except IndexError:
            return


    else:
        process = Popen(args=['mpv' if platform.system() == "Linux" or platform.system() == "Darwin" else WIN_mpv, "--save-position-on-quit", URL], shell=False, stdout=DEVNULL, stderr=DEVNULL)
        return process


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
        process.terminate()
        update_rpc("Menu główne", "Szuka anime do obejrzenia...")
        w_players(SLUG, NUMBER)

    elif ans == choices[1]:
        process.terminate()
        update_rpc("Menu główne", "Szuka anime do obejrzenia...")
        continue_data[1] = NUMBER + 1 if NUMBER < how_many_episodes else NUMBER
        save()
        w_players(SLUG, NUMBER + 1 if NUMBER < how_many_episodes else NUMBER)
    elif ans == choices[2]:
        process.terminate()
        update_rpc("Menu główne", "Szuka anime do obejrzenia...")
        continue_data[1] = NUMBER + 1 if NUMBER < how_many_episodes else NUMBER
        save()
        w_players(SLUG, NUMBER - 1 if NUMBER >= 2 else NUMBER)
    elif ans == choices[3]:
        process.terminate()
        update_rpc("Menu główne", "Szuka anime do obejrzenia...")
        w_list(SLUG)
    elif ans == choices[4]:
        process.terminate()
        update_rpc("Menu główne", "Szuka anime do obejrzenia...")
        m_welcome()


# SAVING SECTION

PATH_home = os.path.expanduser("~")
PATH_config = os.path.join(PATH_home, ".config", "doccli")
PATH_mylist = os.path.join(PATH_config, "mylist.json")
PATH_continue = os.path.join(PATH_config, "continue.json")
PATH_settings = os.path.join(PATH_config, "settings.json")
PATH_history = os.path.join(PATH_config, "history.json")

# Windows MPV location
WIN_home = os.path.expanduser('~')
WIN_mpv = os.path.join(WIN_home, '.config', 'doccli', 'essentials', 'mpv.com')


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
            settings = [True, "Używa doccli!"]
            json.dump(settings, file, indent=4)
    if not os.path.exists(PATH_history):
        with open(PATH_history, 'w') as file:
            file.write('[]')

    # Win install
    if platform.system() == "Windows":
        if not os.path.exists(WIN_mpv):
            print(colored("Wykryto pierwsze uruchomienie programu!", "red"))
            print("Wypakowywanie potrzebnych składników...")

            try:
                with ZipFile('doccli_windows_essentials.zip', 'r') as zfile:
                    zfile.extractall(PATH_config)
                print("Wypakowano!")
                time.sleep(1)
                os.remove('doccli_windows_essentials.zip')
                time.sleep(1)
            except:
                print(colored("Coś poszło nie tak! Upewnij się że wypakowałeś WSZYSTKIE pliki! Nie można znaleźć pliku .zip", "red"))
                time.sleep(5)
                sys.exit()

    with open(PATH_mylist, 'r') as json_file:
        loaded_data = json.load(json_file)
        global mylist
        mylist = loaded_data

    with open(PATH_continue, 'r') as json_file:
        loaded_data = json.load(json_file)
        continue_data = loaded_data

    with open(PATH_settings, 'r') as json_file:
        loaded_data = json.load(json_file)
        settings = loaded_data

    with open(PATH_history, 'r') as json_file:
        loaded_data = json.load(json_file)
        global history
        history = loaded_data


def save():
    with open(PATH_mylist, 'w') as json_file:
        json.dump(mylist, json_file, indent=4)
    with open(PATH_continue, 'w') as json_file:
        json.dump(continue_data, json_file, indent=4)
    with open(PATH_settings, 'w') as json_file:
        json.dump(settings, json_file, indent=4)
    with open(PATH_history, 'w') as json_file:
        json.dump(history, json_file, indent=4)