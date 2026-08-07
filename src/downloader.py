import os
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor

# From pip
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskProgressColumn, TextColumn, TimeRemainingColumn
from termcolor import colored

# Doccli modules
from docchi_api_connector import extract_lycoris_direct_link, get_players_list, get_english_players
from ui_utils import clear, open_menu
from anilist_connector import get_quick_episode_count
from i18n import t
from storage import ds

def w_download_season(details, episodes_list=None, base_download_dir=""):
    SLUG = details['slug']
    TITLE = details.get('title_en') if ds.settings.get('language') == 'en' and details.get('title_en') else details['title']
    MAL_ID = details.get('mal_id')
    
    how_many_episodes = get_quick_episode_count(MAL_ID)

    if how_many_episodes <= 0:
        clear()
        print(colored(t("dl_err_ep_count"), "red"))
        time.sleep(3)
        return

    if episodes_list is None:
        episodes_list = list(range(1, how_many_episodes + 1))

    current_lang = ds.settings.get("language", "pl")
    lang_choices = []
    
    if current_lang == "pl":
        lang_choices.append(t("dl_lang_pl_sub"))
        
    # Zawsze pokazuj angielskie
    lang_choices.extend([
        t("dl_lang_en_sub"),
        t("dl_lang_en_dub"),
        t("cancel")
    ])
    
    chosen_lang = open_menu(
        choices=lang_choices,
        prompt=t("dl_prompt_lang"),
        height=6
    )

    if chosen_lang == t("cancel"):
        return

    quality_choices = [
        t("dl_qual_best"),
        "1080p",
        "720p",
        "480p",
        "360p",
        t("cancel")
    ]
    
    chosen_quality = open_menu(
        choices=quality_choices,
        prompt=t("dl_prompt_qual"),
        height=6
    )

    if chosen_quality == t("cancel"):
        return

    quality_args = []
    if chosen_quality != t("dl_qual_best"):
        res = chosen_quality.replace('p', '')
        quality_args = ["-S", f"res:{res}"]

    if not base_download_dir:
        base_download_dir = os.path.join(os.getcwd(), "doccli_downloads")
        
    safe_title = re.sub(r'[\\/*?:"<>|]', "", TITLE).strip()
    
    if chosen_lang == t("dl_lang_pl_sub"):
        folder_name = f"{t('dl_folder_pl')} {safe_title}"
    elif chosen_lang == t("dl_lang_en_sub"):
        folder_name = f"{t('dl_folder_en_sub')} {safe_title}"
    elif chosen_lang == t("dl_lang_en_dub"):
        folder_name = f"{t('dl_folder_en_dub')} {safe_title}"
        
    series_dir = os.path.join(base_download_dir, folder_name)
    os.makedirs(series_dir, exist_ok=True)

    clear()
    print(colored(t("dl_info_prep").format(TITLE, len(episodes_list)), "cyan"))
    print(colored(t("dl_info_ver").format(chosen_lang), "cyan"))
    print(colored(t("dl_info_qual").format(chosen_quality), "cyan"))
    print(colored(t("dl_info_loc").format(series_dir), "yellow"))
    
    for ep_number in episodes_list:
        players = []
        
        if chosen_lang == t("dl_lang_pl_sub"):
            pl_sources = get_players_list(SLUG, ep_number)
            if isinstance(pl_sources, list):
                players = pl_sources
        else:
            en_sources = get_english_players(details, ep_number)
            if isinstance(en_sources, list):
                for p in en_sources:
                    hosting_label = p['player_hosting'].lower()
                    # Sprawdzamy używając słów ze słownika (napisy/sub, dubbing/dub)
                    if chosen_lang == t("dl_lang_en_sub") and t("anidb_sub").lower() in hosting_label:
                        players.append(p)
                    elif chosen_lang == t("dl_lang_en_dub") and t("anidb_dub").lower() in hosting_label:
                        players.append(p)
        
        if not players:
            print(colored(t("dl_err_no_src").format(ep_number), "red"))
            continue
        
        file_name_template = os.path.join(series_dir, f"{safe_title}{t('dl_ep_file_prefix')} {ep_number:02d}.%(ext)s")
        downloaded = False
        
        print(f"\r\033[K" + colored(t("dl_scan").format(ep_number), "cyan"), end="", flush=True)

        def check_dl_link(player):
            hosting_name, url = player['player_hosting'], player['player']
            url_lower = url.lower()
            
            if "lycoris" in url_lower:
                direct = extract_lycoris_direct_link(url)
                return (player, "ok", "Auto", direct if direct else url)
            elif "mega" in url_lower:
                return (player, "mega", "MEGA", url)
            else:
                try:
                    res = subprocess.run(
                        ["yt-dlp", "--print", "%(resolution)s", "--no-warnings", url],
                        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, timeout=15 
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
                            return (player, "ok", resolved_res, url)
                            
                    res_fallback = subprocess.run(
                        ["yt-dlp", "-q", "--simulate", "--no-warnings", url],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15 
                    )
                    if res_fallback.returncode == 0:
                        return (player, "ok", t("pl_unknown"), url)
                    return (player, "error", "", url)
                except:
                    return (player, "error", "", url)

        with ThreadPoolExecutor(max_workers=15) as executor:
            scanned_sources = list(executor.map(check_dl_link, players))

        valid_sources = [s for s in scanned_sources if s[1] in ("ok", "mega")]

        if not valid_sources:
            print(colored(t("dl_err_all_dead").format(ep_number), "red"))
            continue

        def sort_key(source_tuple):
            _, _, res_text, _ = source_tuple
            if chosen_quality != t("dl_qual_best"):
                if res_text == chosen_quality: return 0  
                if res_text == "Auto": return 1          
                return 2                                 
            else:
                if res_text == "Auto": return 0
                return 1

        valid_sources.sort(key=sort_key)
        print() 

        for index, source_data in enumerate(valid_sources, 1):
            player, status, res_text, target_url = source_data
            
            print(colored(t("dl_try_dl").format(player['player_hosting'], res_text, index, len(valid_sources)), "yellow"))
            
            command = ["yt-dlp", "--newline", "--no-warnings", "--merge-output-format", "mp4"]
            
            if quality_args:
                command.extend(quality_args)
                
            command.extend([target_url, "-o", file_name_template])
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold cyan]{task.description}"),
                BarColumn(bar_width=40, complete_style="green", finished_style="bold green"),
                TaskProgressColumn(),
                TimeRemainingColumn(),
            ) as progress:                
                task_id = progress.add_task(description=t("dl_prog_vid").format(ep_number), total=100)
                
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                current_percent = 0.0
                
                error_msgs = []

                for line in process.stdout:
                    if "ERROR:" in line or "Error" in line:
                        error_msgs.append(line.strip())
                        
                    match = re.search(r'\[download\]\s+([\d\.]+)%', line)
                    if match:
                        try:
                            percent = float(match.group(1))
                            if percent < current_percent - 50:
                                progress.update(task_id, description=t("dl_prog_aud").format(ep_number))
                            current_percent = percent
                            progress.update(task_id, completed=percent)
                        except ValueError:
                            pass
                            
                process.wait()
                
                if process.returncode == 0:
                    downloaded = True
                    progress.update(task_id, completed=100, description=t("dl_prog_done").format(ep_number))
                    break 
                else:
                    progress.update(task_id, description=t("dl_prog_err").format(ep_number))
                    if error_msgs:
                        print(colored(t("dl_ytdlp_err").format(error_msgs[-1]), "red"))

        if not downloaded:
            print(colored(t("dl_err_failed_all").format(ep_number), "red"))
        
    print(colored(t("dl_finished_all").format(TITLE), "green"))
    input(colored(t("dl_enter_to_return"), "yellow"))