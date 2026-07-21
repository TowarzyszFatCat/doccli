import os
import sys
import re
import shutil
import subprocess
import threading
import time

# From pip
from requests import exceptions, get
from termcolor import colored

# Doccli modules
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")) # Drurne obejście
from discord_integration import set_running, start_rpc
from main_module import m_welcome

VERSION = "v2.30.2"

def get_cmd_version(cmd, args=["--version"]):
    try:
        result = subprocess.run([cmd] + args, capture_output=True, text=True, timeout=2)
        out = result.stdout.strip() or result.stderr.strip()
        match = re.search(r'(\d+\.\d+(?:\.\d+)*[a-zA-Z0-9\-]*)', out)
        if match:
            return match.group(1)
        return "Nieznana"
    except Exception:
        return "Nieznana"

def get_latest_ytdlp_version():
    try:
        res = get("https://pypi.org/pypi/yt-dlp/json", timeout=3)
        res.raise_for_status()
        return res.json()["info"]["version"]
    except exceptions.RequestException:
        return None

def check_dependencies() -> bool:
    requires_action = False
    
    print(colored(f"--- Doccli {VERSION} ---", "yellow"))
    print(colored("[INFO] Sprawdzanie środowiska i zależności...", "cyan"))
    
    # 1. Wymagane: yt-dlp
    if shutil.which("yt-dlp"):
        local_yt = get_cmd_version("yt-dlp")
        latest_yt = get_latest_ytdlp_version()
        
        if latest_yt:
            norm_local = ".".join([str(int(x)) if x.isdigit() else x for x in local_yt.split('.')])
            norm_latest = ".".join([str(int(x)) if x.isdigit() else x for x in latest_yt.split('.')])
            
            if norm_local != norm_latest:
                print(colored("[+] yt-dlp:    ", "green") + f"Zainstalowano (Twoja: {local_yt} | Najnowsza: {latest_yt})")
                
                # --- WERSJA KOMENDY ZALEŻNA OD SYSTEMU ---
                if os.name == "nt":
                    update_cmd = "yt-dlp -U"
                else:
                    update_cmd = "sudo yt-dlp -U"
                
                print(colored(f"    [!] Zalecam aktualizację komendą: ({update_cmd}), bo niektóre źródła mogą nie działać!", "red"))
            else:
                print(colored("[+] yt-dlp:    ", "green") + f"Zainstalowano (Wersja: {local_yt} - Aktualna!)")
        else:
            print(colored("[+] yt-dlp:    ", "green") + f"Zainstalowano (Wersja: {local_yt})")
    else:
        print(colored("[-] yt-dlp:    ", "red") + "BRAK! Odtwarzanie i pobieranie nie będzie działać.")
        requires_action = True

    # 2. Wymagane: mpv
    if shutil.which("mpv"):
        mpv_v = get_cmd_version("mpv")
        print(colored("[+] mpv:       ", "green") + f"Zainstalowano (Wersja: {mpv_v})")
    else:
        print(colored("[-] mpv:       ", "red") + "BRAK! Odtwarzanie wideo nie będzie działać.")
        requires_action = True

    # 3. Opcjonalne: chafa
    if shutil.which("chafa"):
        timg_v = get_cmd_version("chafa")
        print(colored("[+] chafa:     ", "green") + f"Zainstalowano (Wersja: {timg_v} | Wyświetlanie okładek)")
    else:
        print(colored("[!] chafa:     ", "yellow") + "Brak [Wyświetlanie okładek]")
        requires_action = True

    # 4. Opcjonalne: megatools
    if shutil.which("megatools"):
        mega_v = get_cmd_version("megatools")
        print(colored("[+] megatools: ", "green") + f"Zainstalowano (Wersja: {mega_v})")
    else:
        print(colored("[!] megatools: ", "yellow") + "Brak (Odtwarzanie ze źródeł Mega.nz)")

    print("")
    return requires_action

def check_update() -> bool:
    try:
        response = get(
            "https://api.github.com/repos/TowarzyszFatCat/doccli/releases/latest",
            timeout=5
        )
        response.raise_for_status()
        
        latest_version = response.json().get("name")

        if latest_version and latest_version != VERSION:
            print(colored("Wersja programu: ", "white"), colored(VERSION, "red"))
            print(colored("Najnowsza wersja:", "white"), colored(latest_version, "green"))
            print("")
            print(colored("Dostępna jest nowa wersja doccli!", "white"))
            print(colored("Szczegóły aktualizacji oraz instrukcję aktualizacji znajdziesz tutaj:", "white"))
            print(colored("https://github.com/TowarzyszFatCat/doccli", "cyan"))
            print("")
            return True
            
    except exceptions.RequestException:
        pass
        
    return False

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    
    has_dep_warnings = check_dependencies()
    has_app_update = check_update()
    
    if has_dep_warnings or has_app_update:
        input(colored("Naciśnij Enter, aby kontynuować...", "yellow"))
    else:
        time.sleep(2)
    
    set_running(True)
    thread = threading.Thread(target=start_rpc)
    thread.start()
    
    m_welcome()