import os
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor

# From pip
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskProgressColumn, TextColumn, TimeRemainingColumn
from termcolor import colored

# Doccli modules
from docchi_api_connector import extract_lycoris_direct_link, get_episodes_count_for_serie, get_players_list, get_english_players
from ui_utils import clear, open_menu

def w_download_season(details, episodes_list=None, base_download_dir=""):
    SLUG = details['slug']
    TITLE = details['title']
    
    how_many_episodes = get_episodes_count_for_serie(SLUG)

    if how_many_episodes == 404:
        clear()
        print(colored("Nie znaleziono strony [Błąd 404]", "red"))
        time.sleep(3)
        return

    if episodes_list is None:
        episodes_list = list(range(1, how_many_episodes + 1))

    lang_choices = [
        "Polski (Napisy PL)",
        "Angielski (Napisy EN)",
        "Angielski (Dubbing EN)",
        "Anuluj"
    ]
    
    chosen_lang = open_menu(
        choices=lang_choices,
        prompt="Wybierz preferowaną wersję językową dla pobieranych plików: ",
        height=6
    )

    if chosen_lang == "Anuluj":
        return

    quality_choices = [
        "Najlepsza dostępna (Domyślna)",
        "1080p",
        "720p",
        "480p",
        "360p",
        "Anuluj"
    ]
    
    chosen_quality = open_menu(
        choices=quality_choices,
        prompt="Wybierz preferowaną jakość obrazu do pobrania: ",
        height=6
    )

    if chosen_quality == "Anuluj":
        return

    quality_args = []
    if chosen_quality != "Najlepsza dostępna (Domyślna)":
        res = chosen_quality.replace('p', '')
        quality_args = ["-S", f"res:{res}"]

    if not base_download_dir:
        base_download_dir = os.path.join(os.getcwd(), "doccli_downloads")
        
    safe_title = re.sub(r'[\\/*?:"<>|]', "", TITLE).strip()
    
    if chosen_lang == "Polski (Napisy PL)":
        folder_name = f"[PL] {safe_title}"
    elif chosen_lang == "Angielski (Napisy EN)":
        folder_name = f"[EN Napisy] {safe_title}"
    elif chosen_lang == "Angielski (Dubbing EN)":
        folder_name = f"[EN Dubbing] {safe_title}"
        
    series_dir = os.path.join(base_download_dir, folder_name)
    os.makedirs(series_dir, exist_ok=True)

    clear()
    print(colored(f"[INFO] Przygotowywanie do pobrania {TITLE} (Wybrano {len(episodes_list)} odc.)...", "cyan"))
    print(colored(f"[INFO] Ustawiona wersja: {chosen_lang}", "cyan"))
    print(colored(f"[INFO] Ustawiona jakość: {chosen_quality}", "cyan"))
    print(colored(f"[INFO] Lokalizacja zapisu: {series_dir}", "yellow"))
    
    for ep_number in episodes_list:
        players = []
        
        if chosen_lang == "Polski (Napisy PL)":
            pl_sources = get_players_list(SLUG, ep_number)
            if isinstance(pl_sources, list):
                players = pl_sources
        else:
            en_sources = get_english_players(details, ep_number)
            if isinstance(en_sources, list):
                for p in en_sources:
                    hosting_label = p['player_hosting'].lower()
                    if chosen_lang == "Angielski (Napisy EN)" and "napisy" in hosting_label:
                        players.append(p)
                    elif chosen_lang == "Angielski (Dubbing EN)" and "dubbing" in hosting_label:
                        players.append(p)
        
        if not players:
            print(colored(f"\n[BŁĄD] Nie znaleziono źródeł w wybranym języku dla odcinka {ep_number}. Pomijam...", "red"))
            continue
        
        file_name_template = os.path.join(series_dir, f"{safe_title} - Odcinek {ep_number:02d}.%(ext)s")
        downloaded = False
        
        print(f"\r\033[K" + colored(f"[*] Skanowanie jakości źródeł dla odcinka {ep_number}...", "cyan"), end="", flush=True)

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
                        return (player, "ok", "Nieznana", url)
                    return (player, "error", "", url)
                except:
                    return (player, "error", "", url)

        with ThreadPoolExecutor(max_workers=15) as executor:
            scanned_sources = list(executor.map(check_dl_link, players))

        valid_sources = [s for s in scanned_sources if s[1] in ("ok", "mega")]

        if not valid_sources:
            print(colored(f"\n[BŁĄD] Żadne ze źródeł dla odcinka {ep_number} nie działa.", "red"))
            continue

        def sort_key(source_tuple):
            _, _, res_text, _ = source_tuple
            if chosen_quality != "Najlepsza dostępna (Domyślna)":
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
            
            print(colored(f"[*] Próbuję pobrać z: {player['player_hosting']} [{res_text}] (Źródło {index}/{len(valid_sources)})...", "yellow"))
            
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
                task_id = progress.add_task(description=f"Pobieranie odc. {ep_number} [bold yellow](Ścieżka VIDEO)", total=100)
                
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
                else:
                    progress.update(task_id, description=f"[bold red]Błąd pobierania odc. {ep_number}!")
                    if error_msgs:
                        print(colored(f"\n   [Szczegóły błędu yt-dlp]: {error_msgs[-1]}", "red"))

        if not downloaded:
            print(colored(f"[BŁĄD] Żadne ze źródeł dla odcinka {ep_number} nie zadziałało.", "red"))
        
    print(colored(f"\n[ZAKOŃCZONO] Proces pobierania serii {TITLE} dobiegł końca!", "green"))
    input(colored("Naciśnij Enter, aby wrócić...", "yellow"))