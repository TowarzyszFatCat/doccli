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
from i18n import t

VERSION = "v2.33.1"

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
    print(colored(t("run_env_check"), "cyan"))
    
    # 1. Wymagane: yt-dlp
    if shutil.which("yt-dlp"):
        local_yt = get_cmd_version("yt-dlp")
        latest_yt = get_latest_ytdlp_version()
        
        if latest_yt:
            norm_local = ".".join([str(int(x)) if x.isdigit() else x for x in local_yt.split('.')])
            norm_latest = ".".join([str(int(x)) if x.isdigit() else x for x in latest_yt.split('.')])
            
            if norm_local != norm_latest:
                print(colored("[+] yt-dlp:    ", "green") + t("run_yt_installed_old").format(local_yt, latest_yt))
                
                # --- WERSJA KOMENDY ZALEŻNA OD SYSTEMU ---
                if os.name == "nt":
                    update_cmd = "yt-dlp -U"
                else:
                    update_cmd = "sudo yt-dlp -U"
                
                print(colored(t("run_yt_update_rec").format(update_cmd), "red"))
            else:
                print(colored("[+] yt-dlp:    ", "green") + t("run_yt_installed_ok").format(local_yt))
        else:
            print(colored("[+] yt-dlp:    ", "green") + t("run_yt_installed").format(local_yt))
    else:
        print(colored("[-] yt-dlp:    ", "red") + t("run_yt_missing"))
        requires_action = True

    # 2. Wymagane: mpv
    if shutil.which("mpv"):
        mpv_v = get_cmd_version("mpv")
        print(colored("[+] mpv:       ", "green") + t("run_mpv_installed").format(mpv_v))
    else:
        print(colored("[-] mpv:       ", "red") + t("run_mpv_missing"))
        requires_action = True

    # 3. Opcjonalne: chafa
    if shutil.which("chafa"):
        timg_v = get_cmd_version("chafa")
        print(colored("[+] chafa:     ", "green") + t("run_chafa_installed").format(timg_v))
    else:
        print(colored("[!] chafa:     ", "yellow") + t("run_chafa_missing"))
        requires_action = True

    # 4. Opcjonalne: megatools
    if shutil.which("megatools"):
        mega_v = get_cmd_version("megatools")
        print(colored("[+] megatools: ", "green") + t("run_mega_installed").format(mega_v))
    else:
        print(colored("[!] megatools: ", "yellow") + t("run_mega_missing"))

    print("")
    return requires_action

def check_update() -> bool:
    try:
        response = get(
            "https://api.github.com/repos/TowarzyszFatCat/doccli/releases/latest",
            timeout=5
        )
        response.raise_for_status()
        
        data = response.json()
        latest_version = data.get("name")

        if latest_version and latest_version != VERSION:
            print(colored(t("run_upd_current"), "white"), colored(VERSION, "red"))
            print(colored(t("run_upd_latest"), "white"), colored(latest_version, "green"))
            print("")
            print(colored(t("run_upd_avail"), "white"))
            
            # DLA WINDOWSA
            if os.name == "nt":
                download_url = None
                for asset in data.get("assets", []):
                    if asset["name"].endswith(".exe"):
                        download_url = asset["browser_download_url"]
                        break
                
                if download_url:
                    from InquirerPy import prompt
                    questions = [{
                        "type": "confirm",
                        "message": t("run_upd_prompt"),
                        "name": "update",
                        "default": True
                    }]
                    ans = prompt(questions)
                    
                    if ans["update"]:
                        perform_update_windows(download_url)
                        return True
                else:
                    print(colored(t("run_upd_manual"), "white"))
                    print(colored("https://github.com/TowarzyszFatCat/doccli", "cyan"))
                    print("")
                    return True
                    
            # DLA LINUX / MACOS ---
            else:
                print(colored(t("run_upd_manual"), "white"))
                print(colored("https://github.com/TowarzyszFatCat/doccli", "cyan"))
                print("")
                return True
            
    except exceptions.RequestException:
        pass
        
    return False


def perform_update_windows(download_url):
    import tempfile
    print(colored(t("run_upd_dl"), "cyan"))
    
    try:
        req = get(download_url, stream=True)
        exe_path = os.path.join(tempfile.gettempdir(), "Doccli_Update.exe")
        
        with open(exe_path, 'wb') as f:
            for chunk in req.iter_content(chunk_size=8192):
                f.write(chunk)
                
        print(colored(t("run_upd_dl_ok"), "green"))
        
        subprocess.Popen([exe_path, "/SILENT", "/SUPPRESSMSGBOXES", "/FORCECLOSEAPPLICATIONS"])
        sys.exit()
        
    except Exception as e:
        print(colored(t("run_upd_err").format(e), "red"))
        time.sleep(3)


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    
    has_dep_warnings = check_dependencies()
    has_app_update = check_update()
    
    if has_dep_warnings or has_app_update:
        input(colored(t("run_enter_cont"), "yellow"))
    else:
        time.sleep(2)
    
    set_running(True)
    thread = threading.Thread(target=start_rpc)
    thread.start()
    
    m_welcome()