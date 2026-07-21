import os
import re
import subprocess
import time

# From pip
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskProgressColumn, TextColumn, TimeRemainingColumn
from termcolor import colored

# Doccli modules
from docchi_api_connector import extract_lycoris_direct_link, get_episodes_count_for_serie, get_players_list
from ui_utils import clear

def w_download_season(SLUG, TITLE):
    how_many_episodes = get_episodes_count_for_serie(SLUG)

    if how_many_episodes == 404:
        clear()
        print(colored("Nie znaleziono strony [Błąd 404]", "red"))
        time.sleep(3)
        return

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
    
    return