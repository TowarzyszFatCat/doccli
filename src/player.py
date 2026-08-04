import os
import shutil
import subprocess
import tempfile
import time
from datetime import datetime
from subprocess import Popen, DEVNULL
from termcolor import colored

# Doccli modules
from storage import ds
from docchi_api_connector import extract_lycoris_direct_link
from anilist_connector import get_duration_by_malid, update_anilist_progress, generate_aniskip_chapters


def kill_process(process):
    """Bezpiecznie zamyka proces odtwarzacza wideo."""
    if not process:
        return
    
    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/F", "/T", "/PID", str(process.pid)], 
            capture_output=True
        )
    else:
        process.terminate()


def mpv_play(URL, quality="best", mal_id=None, ep_number=None):
    """Uruchamia odtwarzacz mpv z odpowiednimi parametrami."""
    mpv_exec = "mpv.exe" if os.name == "nt" else "mpv"

    if shutil.which('mpv') is None:
        print(colored("[BŁĄD]", "red"), colored("Aby program działał wymagana jest instalacja", "white"), colored("mpv", "green"), '\n')
        sys.exit()
    if shutil.which('yt-dlp') is None:
        print(colored("[BŁĄD]", "red"), colored("Aby program działał wymagana jest instalacja", "white"), colored("yt-dlp", "green"), '\n')
        sys.exit()
        
    temp_dir = tempfile.gettempdir()
    chapters_file = os.path.join(temp_dir, "doccli_chapters")

    generate_aniskip_chapters(mal_id, ep_number, chapters_file)

    if "lycoris" in URL.lower():
        direct_url = extract_lycoris_direct_link(URL)
        if direct_url:
            URL = direct_url
            print(colored("[+] Sukces! Znaleziono bezpośredni link wideo.", "green"))
        else:
            print(colored("[-] Nie udało się zdekodować linku. Próbuję odtworzyć domyślnie...", "yellow"))

    ytdl_format_arg = "bestvideo+bestaudio/best"
    if quality != "best":
        height = quality.replace('p', '')
        ytdl_format_arg = f"bestvideo[height<=?{height}]+bestaudio/best"

    details = ds.continue_data[0]
    anime_title = details.get('title', 'Nieznane Anime') if details else 'Nieznane Anime'
    media_title = f"{anime_title} - Odcinek {ep_number}"

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
                    pass 

        mega_url = URL.replace('embed', 'file')
        before_files = set(os.listdir(temp_dir))
        
        os.system(f'megadl {mega_url} --path {temp_dir}')
        
        after_files = set(os.listdir(temp_dir))
        new_files = after_files - before_files
        video_files = [file for file in new_files if file.lower().endswith(tuple(video_extensions))]

        try:
            process = Popen(args=[mpv_exec,
                                  "--save-position-on-quit",
                                  "--input-terminal=no",
                                  f"--force-media-title={media_title}",
                                  f"--chapters-file={chapters_file}",
                                  os.path.join(temp_dir, video_files[0])],
                            shell=False,
                            stdout=DEVNULL,
                            stderr=DEVNULL,)
            return process
        except IndexError:
            return None

    else:
        process = Popen(args=[mpv_exec,
                              "--save-position-on-quit",
                              "--input-terminal=no",
                              f"--force-media-title={media_title}",
                              f"--ytdl-format={ytdl_format_arg}",
                              f"--chapters-file={chapters_file}",
                              URL],
                        shell=False,
                        stdout=DEVNULL,
                        stderr=DEVNULL)
        return process


def delayed_tracker(details, number, process, total_episodes):
    """Zapisuje postęp oglądania po upływie odpowiedniego czasu."""
    for _ in range(100):
        if process is None or process.poll() is not None:
            return  
        time.sleep(1)
        
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    
    duration = get_duration_by_malid(details['mal_id'])
    
    entry = {
        "timestamp": now.timestamp(),
        "dt_string": dt_string,
        "title": details['title'],
        "title_en": details['title_en'],
        "episode": str(number),
        "source": "Doccli - Online",
        "slug": details['slug'],
        "duration": duration
    }
    
    ds.history.insert(0, entry)
    ds.save()
    
    token = ds.settings.get("anilist_token", "")
    
    if token != "":
        is_completed = (number == total_episodes)
        update_anilist_progress(details['mal_id'], number, token, is_completed)