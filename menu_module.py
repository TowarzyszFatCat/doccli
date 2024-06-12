import sys
import time
import json
from InquirerPy import inquirer
import os
from os import system
from docchi_api_connector import get_series_list, get_episodes_count_for_serie, get_players_list
from subprocess import Popen, DEVNULL
from termcolor import colored

def clear():
    system("clear")


def open_menu(choices, prompt='Prompt', border=True, qmark='', message='', pointer='>', cycle=True, height=10):
    clear()

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

    choices = [
        "Wyszukaj",
    ]

    if continue_data[0] is None:
        choices.append("Nie masz nic do wznowienia")
    else:
        choices.append(f"Wznów {continue_data[0]['title']} / {continue_data[0]['title_en']}, Odc: {continue_data[1]}")

    choices.append("Moja lista")
    choices.append("Dołącz do discorda")
    choices.append("Zamknij")

    prompt = 'Wybierz co chcesz zrobić: '

    ans = open_menu(choices=choices, prompt=prompt)

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
        m_discord()
    elif ans == choices[4]:
        sys.exit()


def m_discord():
    print(colored('Zaproszenie:', "white"), colored('discord.gg/Y4RcwbE5CJ', "green"))
    print('')
    input(colored("Naciśnij enter by pominąć...", "yellow"))

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

def m_find():
    choices = [
        "Po tytule",
        "Po tytule EN",
        "Mal ID",
        "Cofnij"
    ]

    prompt = 'Wybierz jak chcesz wyszukać: '

    ans = open_menu(choices=choices, prompt=prompt)

    if ans == choices[0]:
        f_title()
    elif ans == choices[1]:
        f_title_EN()
    elif ans == choices[2]:
        f_malid()
    elif ans == choices[3]:
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

    choices.append("Cofnij")

    prompt = 'Wybierz co chcesz zrobić: '

    genres = "   [ "
    for genre in details['genres']:
        genres += genre + ", "

    genres += "]"

    episode_count = get_episodes_count_for_serie(details['slug'])

    ans = open_menu(choices=choices, prompt=prompt, qmark=f'{details["title"]} / {details["title_en"]} [{episode_count}]', message=genres)

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


def w_first(SLUG):
    continue_data[1] = 1
    save()
    w_players(SLUG, 1)

def w_list(SLUG):
    last_episode = get_episodes_count_for_serie(SLUG)

    choices = list(range(1, last_episode + 1))

    prompt = 'Wybierz odcinek: '

    ans = open_menu(choices=choices, prompt=prompt)
    continue_data[1] = ans
    save()

    w_players(SLUG, ans)


def w_players(SLUG, NUMBER, err=''):
    players = []

    for player in get_players_list(SLUG, NUMBER):
        player_info = [player['player_hosting'], player['player']]

        players.append(player_info)

    choices = [player[0] for player in players]

    prompt = 'Wybierz źródło: '

    ans = open_menu(choices=choices, prompt=prompt, qmark=err)
    ans_index_in_choices = choices.index(ans)

    ans_index = players[ans_index_in_choices]

    process = mpv_play(ans_index[1])



    # Wait 10 sec and check if started playing
    print("Rozpoczynanie odtwarzania...")
    time.sleep(3)                                      # CZAS ZALEZNY OD PREDKOSCI LACZA
    if process.poll() is not None:
        w_players(SLUG, NUMBER, err='Wybrane źródło nie jest dostępne, lub nie jest wspierane! Możesz to złgosić na discordzie.')

    w_default(SLUG, NUMBER, process)

def mpv_play(URL):
    process = Popen(args=['mpv', URL], shell=False, stdout=DEVNULL, stderr=DEVNULL)
    return process

def w_default(SLUG, NUMBER, process):

    how_many_episodes = get_episodes_count_for_serie(SLUG)

    choices = [
        "Następny odcinek",
        "Poprzedni odcinek",
        "Lista odcinków",
        "Menu główne"
    ]

    prompt = 'Co chcesz zrobić? '

    ans = open_menu(choices=choices, prompt=prompt,qmark=f'Odcinek: {NUMBER}/{how_many_episodes}')

    if ans == choices[0]:
        process.kill()
        continue_data[1] = NUMBER + 1 if NUMBER < how_many_episodes else NUMBER
        save()
        w_players(SLUG, NUMBER + 1 if NUMBER < how_many_episodes else NUMBER)
    elif ans == choices[1]:
        process.kill()
        continue_data[1] = NUMBER + 1 if NUMBER < how_many_episodes else NUMBER
        save()
        w_players(SLUG, NUMBER - 1 if NUMBER >= 2 else NUMBER)
    elif ans == choices[2]:
        process.kill()
        w_list(SLUG)
    elif ans == choices[3]:
        process.kill()
        m_welcome()



# SAVING SECTION

PATH_home = os.path.expanduser("~")
PATH_config = os.path.join(PATH_home, ".config", "doccli")
PATH_mylist = os.path.join(PATH_config, "mylist.json")
PATH_continue = os.path.join(PATH_config, "continue.json")


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

    with open(PATH_mylist, 'r') as json_file:
        loaded_data = json.load(json_file)
        global mylist
        mylist = loaded_data

    with open(PATH_continue, 'r') as json_file:
        loaded_data = json.load(json_file)
        continue_data = loaded_data


def save():
    with open(PATH_mylist, 'w') as json_file:
        json.dump(mylist, json_file, indent=4)
    with open(PATH_continue, 'w') as json_file:
        json.dump(continue_data, json_file, indent=4)