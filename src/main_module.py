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
from menus_decor import MAIN_MENU, SZUKAJ, NA_CZASIE, MOJA_LISTA, HISTORIA, MOJA_BIBLIOTEKA, KALENDARZ
from discord_integration import update_rpc, set_running
from docchi_api_connector import get_episodes_count_for_serie, get_players_list, get_details_for_serie, extract_lycoris_direct_link, get_english_players
from anilist_connector import get_details_from_anilist, update_anilist_progress, get_anilist_plan_to_watch, sync_anilist_list_status, get_anilist_history, get_duration_by_malid, sync_history_with_anilist, get_quick_episode_count
from player import mpv_play, kill_process, delayed_tracker
from local_lib import m_local_library
from i18n import t

LAST_CHECK_TIME = 0

def get_notifications():
    tracked_mal_ids = set()
    
    for item in ds.mylist:
        if item.get('mal_id'): tracked_mal_ids.add(int(item['mal_id']))
        
    seen_slugs = set()
    for item in ds.history:
        if isinstance(item, dict) and item.get('source', '').startswith('Doccli - Online'):
            slug = item.get('slug')
            if slug and slug not in seen_slugs:
                ep_str = str(item.get('episode', '1'))
                if ep_str not in ["Ukończono", "Completed", t("al_completed")]:
                    seen_slugs.add(slug)
    
    if seen_slugs:
        for s in get_cached_series_list():
            if s.get('slug') in seen_slugs and s.get('mal_id'):
                tracked_mal_ids.add(int(s['mal_id']))
                
    if not tracked_mal_ids:
        return
        
    from anilist_connector import check_new_episodes
    current_eps = {}
    mal_list = list(tracked_mal_ids)
    for i in range(0, len(mal_list), 50):
        current_eps.update(check_new_episodes(mal_list[i:i+50]))
    
    known_eps = ds.settings.get("known_eps", {})
    unread = ds.settings.get("unread_notifications", [])
    history = ds.settings.get("notification_history", [])
    
    all_s_dict = {str(s.get('mal_id')): s for s in get_cached_series_list()}
    
    for mal_id_str, ep_count in current_eps.items():
        known = known_eps.get(mal_id_str, 0)
        if known > 0 and ep_count > known:
            s = all_s_dict.get(mal_id_str)
            if s:
                title = s.get('title_en') if ds.settings.get('language') == 'en' and s.get('title_en') else s.get('title', 'Anime')
                msg = t("notif_new_ep").format(title, ep_count)
                if msg not in unread and msg not in history:
                    unread.append(msg)
                    history.insert(0, msg)
        known_eps[mal_id_str] = ep_count
        
    ds.settings["known_eps"] = known_eps
    ds.settings["unread_notifications"] = unread
    ds.settings["notification_history"] = history[:50]
    ds.save()

def m_notifications():
    clear()
    ds.settings["unread_notifications"] = []
    ds.save()
    
    history = ds.settings.get("notification_history", [])
    
    if not history:
        print(colored(t("notif_empty"), "yellow"))
        print('')
        input(colored(t("lib_enter_to_return"), "yellow"))
        m_welcome()
        return
        
    choices = [t("notif_clear")] + history + [t("back")]
    
    ans = open_menu(choices=choices, prompt=t("hist_prompt"), message=t("notif_title"), height=10)
    
    if ans == t("back") or ans == choices[-1]:
        m_welcome()
    elif ans == t("notif_clear"):
        ds.settings["notification_history"] = []
        ds.save()
        m_notifications()
    else:
        m_notifications()

def m_welcome():
    global LAST_CHECK_TIME
    
    preload_series_cache()
    update_rpc(t("menu_main"), t("rpc_searching"))

    if time.time() - LAST_CHECK_TIME > 600:
        get_notifications()
        LAST_CHECK_TIME = time.time()

    unread_count = len(ds.settings.get("unread_notifications", []))
    notif_label = t("menu_notifications").format(unread_count)

    choices = [
        t("menu_search"),
        t("menu_resume"),
        notif_label,
        t("menu_mylist"),
        t("menu_trending"),
        t("menu_calendar"),
        t("menu_library"),
        t("menu_history"),
        t("menu_stats"),
        t("menu_settings"),
        t("menu_discord"),
        t("menu_exit")
    ]

    prompt_txt = t("welcome_prompt")

    has_token = ds.settings.get("anilist_token", "") != ""
    if has_token:
        status_txt = t("status_connected")
    else:
        status_txt = t("status_disconnected")

    dynamic_menu_art = MAIN_MENU + "\n" + status_txt + "\n"
    
    unread = ds.settings.get("unread_notifications", [])
    if unread:
        dynamic_menu_art += "\n" + colored(unread[-1], "green") + "\n"

    ans = open_menu(choices=choices, prompt=prompt_txt, height=12, message=dynamic_menu_art)

    if ans == choices[0]: m_find()                          # 0: Search
    elif ans == choices[1]: m_resume()                      # 1: Continue watching
    elif ans == choices[2]: m_notifications()               # 2: Notifications (X)
    elif ans == choices[3]: m_mylist()                      # 3: My List
    elif ans == choices[4]: m_trending()                    # 4: Trending Anime
    elif ans == choices[5]: m_calendar()                    # 5: Release Calendar
    elif ans == choices[6]: m_local_library()               # 6: My Library (Offline)
    elif ans == choices[7]: m_history()                     # 7: Watch History
    elif ans == choices[8]: m_stats(); m_welcome()          # 8: Doccli Statistics
    elif ans == choices[9]: m_settings()                    # 9: Settings
    elif ans == choices[10]: m_discord()                    # 10: Join our Discord
    elif ans == choices[11]: set_running(False); sys.exit() # 11: Exit


def m_settings():
    def_dl = ds.settings.get("download_path", "")
    current_dl_path = def_dl if def_dl != "" else t("dl_def_path")
    current_quality = ds.settings.get("player_quality", "best")
    current_lang = ds.settings.get("language", "pl")

    choices = [
        t("set_rpc"),
        t("set_anilist"),
        f"{t('set_dl_path')} ({t('currently')}: {current_dl_path})",
        f"{t('set_quality')} ({t('currently')}: {current_quality})",
        f"{t('set_lang')} ({t('currently')}: {current_lang.upper()})",
        t("menu_main")
    ]
    
    prompt_text = t("set_prompt")
    ans = open_menu(choices=choices, prompt=prompt_text, height=8)
    
    if ans == choices[0]:
        rpc_choices = [{
                "type": "list",
                "message": t("rpc_q"),
                "choices": [t("yes"), t("no")],
            }]
        res = prompt(questions=rpc_choices)

        if res[0] == t("no"):
            ds.settings["rpc_enabled"] = False
            ds.save()
            m_welcome()
        if res[0] == t("yes"):
            clear()
            ds.settings["rpc_enabled"] = True
            choices2 = [{"type": "input", "message": t("rpc_input"), "name": "status_dc"}]
            res2 = prompt(questions=choices2)

            if not res2['status_dc'] == "" and len(res2['status_dc']) > 1:
                ds.settings["rpc_status"] = res2['status_dc']
                ds.save()
                m_welcome()
            else:
                ds.settings["rpc_status"] = t("rpc_def_status")
                ds.save()
                m_welcome()
                
    elif ans == choices[1]:
        clear()
        CLIENT_ID = "16904"
        print(colored(t("al_info1"), "cyan"))
        print(colored(t("al_info2"), "cyan"))
        
        auth_url = f"https://anilist.co/api/v2/oauth/authorize?client_id={CLIENT_ID}&response_type=token"
        try:
            webbrowser.open(auth_url)
        except:
            print(colored(t("al_err").format(auth_url), "yellow"))
            
        questions = [{"type": "input", "message": t("al_input"), "name": "token"}]
        res = prompt(questions)
        
        if res['token']:
            ds.settings["anilist_token"] = res['token'].strip()
            ds.save()
            print(colored(t("al_success"), "green"))
            time.sleep(3)
        m_settings()

    elif ans == choices[2]:
        clear()
        print(colored(t("dl_info").format(current_dl_path), "cyan"))
        print(colored(t("dl_help1"), "yellow"))
        print(colored(t("dl_help2"), "yellow"))
        
        questions = [{"type": "input", "message": t("dl_input"), "name": "new_path"}]
        res = prompt(questions)
        new_input = res['new_path'].strip()
        
        if new_input == "":
            ds.settings["download_path"] = ""
            ds.save()
            print(colored(t("dl_reset"), "green"))
        else:
            try:
                os.makedirs(new_input, exist_ok=True)
                ds.settings["download_path"] = new_input
                ds.save()
                print(colored(t("dl_success").format(new_input), "green"))
            except Exception as e:
                print(colored(t("dl_err").format(e), "red"))
        
        time.sleep(3)
        m_settings()
        
    elif ans == choices[3]:
        quality_choices = [t("qual_source"), "1080p", "720p", "480p", "360p", t("back")]
        chosen = open_menu(choices=quality_choices, prompt=t("qual_prompt"), height=7)
        
        if chosen != t("back"):
            if chosen == t("qual_source") or chosen.startswith("best"):
                ds.settings["player_quality"] = "best"
            else:
                ds.settings["player_quality"] = chosen
            ds.save()
            print(colored(t("qual_success").format(ds.settings['player_quality']), "green"))
            time.sleep(2)
        m_settings()

    elif ans == choices[4]:
        lang_choices = ["Polski (pl)", "English (en)", t("back")]
        chosen = open_menu(choices=lang_choices, prompt=t("lang_prompt"), height=5)
        
        if chosen == "Polski (pl)":
            ds.settings["language"] = "pl"
            ds.save()
            print(colored(t("lang_success"), "green"))
            time.sleep(2)
        elif chosen == "English (en)":
            ds.settings["language"] = "en"
            ds.save()
            print(colored(t("lang_success"), "green"))
            time.sleep(2)
            
        m_settings()

    elif ans == choices[5]:
        m_welcome()


def m_discord():
    webbrowser.open('https://discord.gg/Y4RcwbE5CJ')
    m_welcome()


def m_mylist():
    has_token = ds.settings.get("anilist_token") != ""
    
    if has_token:
        clear()
        print(colored(t("mylist_sync"), "cyan"))
        
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

    choices = [t("back")]
    display_map = {}
    
    if ds.mylist:
        choices.append(t("mylist_random"))
    
    display_list = list(reversed(ds.mylist))
    
    for element in display_list:
        display_text = f"{element['title']} | {element['title_en']}"
        choices.append(display_text)
        display_map[display_text] = element

    prompt_txt = t("mylist_prompt")
    ans = open_menu(choices=choices, prompt=prompt_txt, message=MOJA_LISTA)
    
    if ans == t("back"):
        m_welcome()
        
    elif ans == t("mylist_random"):
        import random
        random_anime = random.choice(ds.mylist)
        m_details(random_anime)
        
    else:
        selected_anime = display_map[ans]
        m_details(selected_anime)


def m_history():
    choices = [t("back")]
    display_map = {}
    
    for item in ds.history[:50]:  
        display_text = f"[{item['dt_string']}] [{item['source']}] {item['title']} [{t('def_qmark').format(item['episode'], '')[:-1]}]"
        choices.append(display_text)
        display_map[display_text] = item

    prompt = t("hist_prompt")
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
                print(colored(t("hist_err_server"), "red"))
                time.sleep(2)
                m_history()
        else:
            print(colored(t("hist_err_profile"), "yellow"))
            time.sleep(3)
            m_history()


def m_find():
    choices = [
        t("find_title"),
        t("find_title_en"),
        t("find_mal"),
        t("find_genre"),
        t("back")
    ]

    prompt = t("find_prompt")
    ans = open_menu(choices=choices, prompt=prompt, height=5, message=SZUKAJ)

    if ans == choices[0]:
        perform_search('title')
    elif ans == choices[1]:
        perform_search('title_en')
    elif ans == choices[2]:
        perform_search('mal_id')
    elif ans == choices[3]:
        perform_genre_search()
    elif ans == choices[4]:
        m_welcome()


def perform_search(search_key):
    all_series_json = get_cached_series_list()
    
    choices = [serie[search_key] for serie in all_series_json]
    choices.append(t("back"))
    
    prompt = t("find_search")
    ans = open_menu(choices=choices, prompt=prompt, message=SZUKAJ)
    
    if ans == t("back"):
        m_find()
        return
        
    ans_index = choices.index(ans)
    ans_details = all_series_json[ans_index]

    m_details(details=ans_details)


def perform_genre_search():
    import random
    
    all_series_json = get_cached_series_list()
    
    unique_genres = set()
    for serie in all_series_json:
        if 'genres' in serie and isinstance(serie['genres'], list):
            for genre in serie['genres']:
                unique_genres.add(genre.strip())
                
    if not unique_genres:
        print(colored(t("genre_err"), "red"))
        time.sleep(2)
        m_find()
        return

    genres_list = sorted(list(unique_genres))
    genres_list.append(t("back"))

    ans_genre = open_menu(
        choices=genres_list, 
        prompt=t("genre_prompt"), 
        message=SZUKAJ, 
        height=10
    )
    
    if ans_genre == t("back"):
        m_find()
        return

    filtered_series = []
    for serie in all_series_json:
        if 'genres' in serie and ans_genre in serie['genres']:
            filtered_series.append(serie)

    sort_choices = [t("sort_trending"), t("sort_alpha"), t("sort_surprise"), t("back")]
    ans_sort = open_menu(choices=sort_choices, prompt=t("sort_prompt"), message=SZUKAJ, height=6)
    
    if ans_sort == t("back"):
        perform_genre_search()
        return
        
    if ans_sort == t("sort_surprise"):
        ans_details = random.choice(filtered_series)
        m_details(details=ans_details)
        return
        
    trending_list = get_cached_trending_list()
    
    if ans_sort == t("sort_trending"):
        def sort_key(serie):
            mal_id = serie.get('mal_id')
            if mal_id in trending_list:
                return (trending_list.index(mal_id), serie.get('title', '').lower())
            return (999999, serie.get('title', '').lower())
            
        filtered_series.sort(key=sort_key)
    else:
        filtered_series.sort(key=lambda x: x.get('title', '').lower())

    choices_titles = []
    for serie in filtered_series:
        prefix = "⭐ " if ans_sort == t("sort_trending") and serie.get('mal_id') in trending_list else ""
        choices_titles.append(f"{prefix}{serie.get('title', t('al_none'))} / {serie.get('title_en', t('al_none'))}")
        
    choices_titles.append(t("back"))

    ans_anime = open_menu(
        choices=choices_titles, 
        prompt=t("genre_res_prompt").format(ans_genre, len(filtered_series)), 
        message=SZUKAJ, 
        height=10
    )

    if ans_anime == t("back"):
        perform_genre_search()
        return

    ans_index = choices_titles.index(ans_anime)
    ans_details = filtered_series[ans_index]

    m_details(details=ans_details)


def m_trending():
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

    top_anime.sort(key=lambda x: x[0])
    
    choices = [t("back")]
    for anime in top_anime:
        choices.append(f"{anime[0] + 1}. {anime[2]} / {anime[3]}")

    prompt = t("trend_prompt")

    ans = open_menu(choices=choices, prompt=prompt, message=NA_CZASIE)
    
    if ans == choices[0]:
        m_welcome()
    else:
        ans_index = choices.index(ans)
        ans_slug = top_anime[ans_index - 1][1]
        m_details(get_details_for_serie(SLUG=ans_slug))


def m_details(details):
    last_watched_ep = 0
    for item in ds.history:
        if isinstance(item, dict) and item.get('slug') == details['slug']:
            try:
                last_watched_ep = int(item.get('episode', 0))
                break
            except ValueError:
                pass
                
    next_ep = last_watched_ep + 1 if last_watched_ep > 0 else 1

    score_bar, description, episode_count, trailer_url = get_details_from_anilist(str(details["mal_id"]))

    watch_opt = f"{t('det_cont')} {next_ep}" if last_watched_ep > 0 else t("det_first")
    
    choices = [watch_opt, t("det_list")]
    
    if trailer_url:
        choices.append(t("det_trailer"))

    choices.extend([t("det_dl_season"), t("det_dl_eps")])

    if details in ds.mylist:
        choices.append(t("det_rm_list"))
    else:
        choices.append(t("det_add_list"))

    choices.extend([t("det_search"), t("menu_main")])

    prompt_txt = t("det_prompt")

    genres = "[ "
    for genre in details['genres']:
        genres += genre + ","
    genres += " ]"

    max_ep = episode_count if isinstance(episode_count, int) else 9999

    ans = open_menu(
        choices=choices,
        prompt=prompt_txt,
        qmark=f'{details["title"]} / {details["title_en"]} \n [{t("det_ep_count")}: {episode_count}] [{t("det_score")}: {score_bar}]',
        message=genres,
        height=8,
        image=details['cover'],
        description=description 
    )

    if ans == watch_opt:
        ds.continue_data[0] = details
        ds.continue_data[1] = next_ep
        ds.save()
        w_players(details['slug'], next_ep)
        
    elif ans == t("det_list"):
        ds.continue_data[0] = details
        w_list(details['slug'])
        
    elif ans == t("det_trailer"):
        clear()
        print(colored(t("trailer_loading"), "cyan"))
        mpv_cmd = "mpv.exe" if os.name == "nt" else "mpv"
        try:
            subprocess.run([mpv_cmd, trailer_url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass
        m_details(details)
        
    elif ans == t("det_dl_season"): 
        w_download_season(details, base_download_dir=ds.settings["download_path"])
        m_details(details)
        
    elif ans == t("det_dl_eps"): 
        questions = [{
            "type": "input", 
            "message": t("det_dl_input").format(episode_count), 
            "name": "episodes_input"
        }]
        res = prompt(questions)
        
        if res['episodes_input']:
            episodes_to_download = set()
            for part in res['episodes_input'].split(','):
                part = part.strip()
                if not part: continue
                if '-' in part:
                    try:
                        start, end = map(int, part.split('-'))
                        start, end = min(start, end), max(start, end)
                        episodes_to_download.update(range(max(1, start), min(max_ep, end) + 1))
                    except ValueError: pass 
                else:
                    try:
                        ep = int(part)
                        if 1 <= ep <= max_ep: episodes_to_download.add(ep)
                    except ValueError: pass 

            ep_list = sorted(list(episodes_to_download))
            if not ep_list:
                print(colored(t("det_dl_err"), "red"))
                time.sleep(2)
            else:
                w_download_season(details, ep_list, base_download_dir=ds.settings["download_path"])
        m_details(details)
        
    elif ans in [t("det_rm_list"), t("det_add_list")]:
        has_token = ds.settings.get("anilist_token") != ""
        token = ds.settings["anilist_token"] if has_token else ""
        
        if details in ds.mylist:
            ds.mylist.remove(details)
            if has_token: threading.Thread(target=sync_anilist_list_status, args=(details['mal_id'], token, False), daemon=True).start()
        else:
            ds.mylist.append(details)
            if has_token: threading.Thread(target=sync_anilist_list_status, args=(details['mal_id'], token, True), daemon=True).start()
            
        ds.save()
        m_details(details)
            
    elif ans == t("det_search"):
        m_find()
        
    elif ans == t("menu_main"):
        m_welcome()


def w_list(SLUG):
    details = ds.continue_data[0]
    
    if not details or details.get('slug') != SLUG:
        details = get_details_for_serie(SLUG)
        ds.continue_data[0] = details
        
    last_episode = get_quick_episode_count(details.get('mal_id'))

    if last_episode <= 0:
        clear()
        print(colored(t("list_err"), "red"))
        time.sleep(3)
        m_details(details)
        return

    choices = list(range(1, last_episode + 1))
    choices.append(t("back"))

    prompt = t("list_prompt")
    ans = open_menu(choices=choices, prompt=prompt)
    
    if ans == t("back"):
        m_details(details)
    else:
        ds.continue_data[1] = ans
        ds.save()
        w_players(SLUG, ans)


def w_players(SLUG, NUMBER, err=''):
    from docchi_api_connector import get_players_list, extract_lycoris_direct_link, get_english_players
    import shutil
    import subprocess
    from concurrent.futures import ThreadPoolExecutor

    players = []
    details = ds.continue_data[0]
    current_lang = ds.settings.get("language", "pl")

    clear()
    print(colored(t("pl_load").format(NUMBER), "cyan"))
    
    if current_lang == "pl":
        print(colored(t("pl_pl_src"), "yellow"))
        pl_players_list = get_players_list(SLUG, NUMBER)
        if pl_players_list != 404 and isinstance(pl_players_list, list):
            for player in pl_players_list:
                players.append(["[PL]", player['player_hosting'], player['player']])

    print(colored(t("pl_en_src"), "yellow"))
    if details:
        en_players_list = get_english_players(details, NUMBER)
        if en_players_list:
            for player in en_players_list:
                players.append(["[EN]", player['player_hosting'], player['player']])

    if not players:
        clear()
        print(colored(t("pl_404"), "red"))
        time.sleep(3)
        if details:
            m_details(details)
        else:
            m_details(get_details_for_serie(SLUG))
        return

    print(colored(t("pl_analyzing"), "cyan"))
    
    def check_link(player):
        hosting_name, url = player[1], player[2]
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
                        if "x" in raw_res:
                            resolved_res = f"{raw_res.split('x')[-1]}p"
                        elif raw_res.isdigit():
                            resolved_res = f"{raw_res}p"
                        else:
                            resolved_res = raw_res
                    else:
                        resolved_res = t("pl_unknown")
                        
                    return ("ok", resolved_res)
                    
                res_fallback = subprocess.run(
                    ["yt-dlp", "-q", "--simulate", "--no-warnings", url],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=15 
                )
                
                if res_fallback.returncode == 0:
                    return ("ok", t("pl_unknown"))
                    
                return ("error", "")
            except:
                return ("error", "")

    with ThreadPoolExecutor(max_workers=15) as executor:
        results = list(executor.map(check_link, players))

    choices = []
    
    for player, result in zip(players, results):
        status, res_text = result
        lang_tag = player[0]
        hosting_name = player[1]
        source_link = player[2]

        if status == "ok":
            prefix = f"✅ {lang_tag} [{res_text}] "
        elif status == "mega":
            prefix = f"🟡 {lang_tag} [MEGA] "
        else:
            prefix = f"❌ {lang_tag} [{t('pl_none')}] "
            
        display_line = (prefix + hosting_name).ljust(45) + f" | {t('pl_link')}: " + source_link
        choices.append(display_line)

    current_quality = ds.settings.get("player_quality", "best")
    choices.append(f"{t('pl_chg_qual')} ({t('currently')}: {current_quality})")
    choices.append(t("menu_main"))

    prompt = t("pl_prompt")
    ans = open_menu(choices=choices, prompt=prompt, qmark=err)

    if ans == choices[-1]:
        m_welcome()
        return
        
    if ans == choices[-2]: 
        quality_choices = [t("qual_source"), "1080p", "720p", "480p", "360p"]
        chosen = open_menu(choices=quality_choices, prompt=t("qual_prompt"), height=6)
        
        if chosen == t("qual_source") or chosen.startswith("best"):
            ds.settings["player_quality"] = "best"
        else:
            ds.settings["player_quality"] = chosen
            
        ds.save()
        w_players(SLUG, NUMBER, err=t("pl_qual_chg").format(ds.settings["player_quality"]))
        return

    ans_index_in_choices = choices.index(ans)
    selected_player_url = players[ans_index_in_choices][2]

    mal_id = ds.continue_data[0].get('mal_id') if ds.continue_data[0] else None

    process = mpv_play(
        URL=selected_player_url, 
        quality=ds.settings.get("player_quality", "best"),
        mal_id=mal_id,
        ep_number=NUMBER
    )

    print(t("pl_start"))
    time.sleep(3)                                      
    if process == None or process.poll() is not None:
        w_players(SLUG, NUMBER, err=t("pl_err_src"))

    w_default(SLUG, NUMBER, process)


def w_default(SLUG, NUMBER, process):
    details = ds.continue_data[0]
    if not details or details.get('slug') != SLUG:
        details = get_details_for_serie(SLUG)
        
    how_many_episodes = get_quick_episode_count(details.get('mal_id'))

    if how_many_episodes <= 0:
        how_many_episodes = NUMBER

    if ds.settings.get("rpc_enabled", True):
        update_rpc(t("def_rpc_watch").format(details.get('title', 'Anime'), NUMBER, how_many_episodes), ds.settings.get("rpc_status", t("rpc_def_status")))
    else:
        update_rpc(t("def_rpc_def"), ds.settings.get("rpc_status", t("rpc_def_status")))

    threading.Thread(target=delayed_tracker, args=(details, NUMBER, process, how_many_episodes), daemon=True).start()

    choices = [t("def_chg_src")]
    token = ds.settings.get("anilist_token", "")

    if NUMBER < how_many_episodes:
        choices.append(t("def_next"))
    else:
        if token != "":
            choices.append(t("def_rate"))

    choices.extend([
        t("def_prev"),
        t("def_list"),
        t("menu_main")
    ])

    prompt = t("def_prompt")
    ans = open_menu(choices=choices, prompt=prompt, qmark=t("def_qmark").format(NUMBER, how_many_episodes), height=7)

    if ans == choices[0]:
        kill_process(process)
        update_rpc(t("menu_main"), t("rpc_searching"))
        w_players(SLUG, NUMBER)

    elif ans == t("def_next"):
        kill_process(process)
        update_rpc(t("menu_main"), t("rpc_searching"))
        next_ep = NUMBER + 1
        ds.continue_data[1] = next_ep
        ds.save()
        w_players(SLUG, next_ep)
        
    elif ans == t("def_rate"):
        kill_process(process) 
        if token != "":
            clear()
            
            from anilist_connector import rate_anilist_anime, get_anilist_score_format
            
            print(colored(t("rate_info"), "cyan"))
            score_format = get_anilist_score_format(token)
            
            rate_choices = []
            
            if score_format == "POINT_100":
                rate_choices = [str(i) for i in range(100, 0, -1)]
            elif score_format == "POINT_10_DECIMAL":
                rate_choices = [f"{i/10:.1f}" for i in range(100, 0, -1)]
            elif score_format == "POINT_5":
                rate_choices = ["5 ⭐", "4 ⭐", "3 ⭐", "2 ⭐", "1 ⭐"]
            elif score_format == "POINT_3":
                rate_choices = [f"🙂 {t('rate_good')}", f"😐 {t('rate_avg')}", f"🙁 {t('rate_bad')}"]
            else: 
                rate_choices = [str(i) for i in range(10, 0, -1)]
                
            rate_choices.append(t("rate_no"))
            
            ans_rate = open_menu(
                choices=rate_choices,
                prompt=t("rate_prompt"),
                height=12
            )
            
            if ans_rate != t("rate_no"):
                score_raw = 0
                
                if score_format == "POINT_100":
                    score_raw = int(ans_rate)
                elif score_format == "POINT_10_DECIMAL":
                    score_raw = int(float(ans_rate) * 10)
                elif score_format == "POINT_5":
                    score_raw = int(ans_rate.split()[0]) * 20  
                elif score_format == "POINT_3":
                    if ":)" in ans_rate: score_raw = 100
                    elif ":|" in ans_rate: score_raw = 67
                    else: score_raw = 33
                else:
                    score_raw = int(ans_rate) * 10
                
                print(colored(t("rate_send"), "cyan"))
                if rate_anilist_anime(details.get('mal_id'), score_raw, token):
                    print(colored(t("rate_ok"), "green"))
                else:
                    print(colored(t("rate_err"), "red"))
                time.sleep(2)
                
        update_rpc(t("menu_main"), t("rpc_searching"))
        m_welcome()

    elif ans == t("def_finish"):
        kill_process(process)
        clear()
        print(colored(t("finish_msg").format(details.get('title', t("player_unknown_anime"))), "green"))
        time.sleep(2)
        update_rpc(t("menu_main"), t("rpc_searching"))
        m_welcome()

    elif ans == t("def_prev"):
        kill_process(process)
        update_rpc(t("menu_main"), t("rpc_searching"))
        prev_ep = NUMBER - 1 if NUMBER >= 2 else NUMBER
        ds.continue_data[1] = prev_ep
        ds.save()
        w_players(SLUG, prev_ep)
        
    elif ans == t("def_list"):
        kill_process(process)
        update_rpc(t("menu_main"), t("rpc_searching"))
        w_list(SLUG)
        
    elif ans == t("menu_main"):
        kill_process(process)
        update_rpc(t("menu_main"), t("rpc_searching"))
        m_welcome()


def m_resume():
    resume_list = []
    seen_slugs = set()

    for item in ds.history:
        if isinstance(item, dict) and item.get('source', '').startswith('Doccli - Online'):
            slug = item.get('slug')
            if slug and slug not in seen_slugs:
                ep_str = str(item.get('episode', '1'))
                
                if ep_str in ["Ukończono", "Completed", t("al_completed")]:
                    seen_slugs.add(slug)
                    continue
                    
                try:
                    last_ep = int(ep_str)
                    next_ep = last_ep + 1
                except ValueError:
                    last_ep = 0
                    next_ep = 1

                seen_slugs.add(slug)
                
                resume_list.append({
                    'slug': slug,
                    'title': item.get('title'),
                    'last_ep': last_ep,
                    'next_ep': next_ep,
                    'mal_id': None
                })

    if not resume_list:
        print(colored(t("res_empty"), "yellow"))
        time.sleep(2)
        m_welcome()
        return

    resume_list = resume_list[:15]
    all_series = get_cached_series_list()
    
    for res_item in resume_list:
        for s in all_series:
            if s.get('slug') == res_item['slug']:
                res_item['mal_id'] = s.get('mal_id')
                break

    clear()
    print(colored(t("res_load"), "cyan"))
    
    def fetch_total(item):
        total = get_quick_episode_count(item['mal_id']) if item['mal_id'] else 0
        return item, total

    with ThreadPoolExecutor(max_workers=15) as executor:
        results = list(executor.map(fetch_total, resume_list))

    choices = [t("back")]
    display_map = {}
    
    for item, total_eps in results:
        bar_len = 10
        if total_eps > 0:
            ratio = min(1.0, item['last_ep'] / total_eps)
            filled = int(bar_len * ratio)
            bar = "█" * filled + "░" * (bar_len - filled)
            ep_info = f"[{item['last_ep']}/{total_eps}]"
        else:
            bar = "░" * bar_len
            ep_info = f"[{item['last_ep']}/?]"
            
        short_title = item['title'][:25] + "..." if len(item['title']) > 25 else item['title']
        base_text = t("res_resume").format(short_title, item['next_ep'])
        
        display_text = f"{base_text.ljust(45)} {ep_info.rjust(8)} {bar}"
        
        choices.append(display_text)
        display_map[display_text] = item

    ans = open_menu(choices=choices, prompt=t("res_prompt"), height=10)
    
    if ans == t("back"):
        m_welcome()
    else:
        selected = display_map[ans]
        slug = selected['slug']
        next_ep = selected['next_ep']
        
        clear()
        print(colored(t("res_load"), "cyan"))
        details = get_details_for_serie(slug)
        
        ds.continue_data[0] = details
        ds.continue_data[1] = next_ep
        ds.save()
        
        w_players(slug, next_ep)

def m_calendar():
    from anilist_connector import get_anilist_schedule
    from datetime import datetime
    
    clear()
    print(colored(t("cal_info"), "cyan"))
    
    schedule = get_anilist_schedule(days=7) 
    
    if not schedule:
        print(colored(t("cal_err1"), "red"))
        time.sleep(2)
        m_welcome()
        return

    all_series = get_cached_series_list()
    local_db = {str(s.get('mal_id')): s for s in all_series if s.get('mal_id')}

    choices_map = {}
    choices = []

    days_names = t("cal_days")

    for item in schedule:
        if not item.get('media') or not item['media'].get('idMal'):
            continue
            
        mal_id = str(item['media']['idMal'])
        
        if mal_id in local_db:
            local_anime = local_db[mal_id]
            air_time = int(item['airingAt'])
            ep_num = item['episode']

            dt = datetime.fromtimestamp(air_time)
            day_name = days_names[dt.weekday()]
            time_str = dt.strftime("%H:%M")
            date_str = dt.strftime("%d.%m")

            display_str = f"[{day_name} {date_str} | {time_str}] {local_anime.get('title', t('cal_none'))} (Odc. {ep_num})"
            choices.append(display_str)
            choices_map[display_str] = local_anime

    if not choices:
        print(colored(t("cal_err2"), "yellow"))
        time.sleep(3)
        m_welcome()
        return

    choices.append(t("back"))

    ans = open_menu(
        choices=choices, 
        prompt=t("cal_prompt"), 
        height=12,
        message=KALENDARZ
    )

    if ans == t("back"):
        m_welcome()
    else:
        selected_anime = choices_map[ans]
        m_details(selected_anime)