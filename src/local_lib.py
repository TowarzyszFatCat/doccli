import os
import subprocess
from datetime import datetime

# From pip
from termcolor import colored

# Doccli modules
from storage import ds
from ui_utils import clear, open_menu
from cache import get_cached_series_list
from anilist_connector import get_duration_by_malid
from menus_decor import MOJA_BIBLIOTEKA
from i18n import t


def m_local_library():
    """Zarządza pobranymi plikami i pozwala na ich odtwarzanie offline."""
    from main_module import m_welcome  # Import lokalny
    
    clear()
        
    dl_path = ds.settings.get("download_path", "")
    if dl_path != "":
        downloads_dir = dl_path
    else:
        current_dir = os.getcwd()
        downloads_dir = os.path.join(current_dir, "doccli_downloads")
    
    if not os.path.exists(downloads_dir):
        print(colored(t("lib_err_no_dir").format(downloads_dir), "red"))
        print(colored(t("lib_err_no_anime"), "yellow"))
        print('')
        input(colored(t("lib_enter_to_return"), "yellow"))
        m_welcome()
        return
        
    series_list = [d for d in os.listdir(downloads_dir) if os.path.isdir(os.path.join(downloads_dir, d))]
    
    if not series_list:
        print(colored(t("lib_info_empty"), "yellow"))
        print('')
        input(colored(t("lib_enter_to_return"), "yellow"))
        m_welcome()
        return
        
    series_list.append(t("menu_main"))
    
    selected_series = open_menu(
        choices=series_list, 
        prompt=t("lib_prompt_series"), 
        height=10, 
        message=MOJA_BIBLIOTEKA
    )
    
    if selected_series == t("menu_main"):
        m_welcome()
        return

    while True:
        clear()
        series_path = os.path.join(downloads_dir, selected_series)
        
        episodes_list = [f for f in os.listdir(series_path) if os.path.isfile(os.path.join(series_path, f))]
        episodes_list.sort()
        
        if not episodes_list:
            print(colored(t("lib_err_no_vids").format(selected_series), "red"))
            input(colored(t("lib_enter_to_return"), "yellow"))
            m_welcome()
            return
            
        choices = [t("lib_watch_auto")] + episodes_list + [t("lib_back_to_series")]
        
        selected_ep = open_menu(
            choices=choices, 
            prompt=t("lib_prompt_ep").format(selected_series), 
            height=10, 
            message=MOJA_BIBLIOTEKA
        )
        
        if selected_ep == t("lib_back_to_series"):
            m_local_library()
            return
            
        elif selected_ep == t("lib_watch_auto"):
            for ep in episodes_list:
                file_path = os.path.join(series_path, ep)
                clear()
                print(colored(t("lib_auto_playing").format(ep), "cyan"))
                print(colored(t("lib_mpv_info"), "white"))
                
                all_series = get_cached_series_list()
                mal_id = None
                for s in all_series:
                    if s['title'] == selected_series or s['title_en'] == selected_series:
                        mal_id = s['mal_id']
                        break
                        
                duration = get_duration_by_malid(mal_id) if mal_id else 21

                now = datetime.now()
                entry = {
                    "timestamp": now.timestamp(),
                    "dt_string": now.strftime("%d/%m/%Y %H:%M"),
                    "title": selected_series,
                    "title_en": selected_series,
                    "episode": ep,
                    "source": "Doccli - Offline",
                    "slug": None,
                    "duration": duration
                }
                ds.history.insert(0, entry)
                ds.save()
                
                try:
                    process = subprocess.run(["mpv", file_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    
                    if process.returncode != 0:
                        print(colored(t("lib_auto_interrupted"), "yellow"))
                        input(t("lib_press_enter"))
                        break
                except FileNotFoundError:
                    print(colored(t("lib_err_no_mpv"), "red"))
                    input(t("lib_press_enter"))
                    m_welcome()
                    return
        else:
            file_path = os.path.join(series_path, selected_ep)
            clear()
            print(colored(t("lib_playing_disk").format(selected_ep), "cyan"))
            print(colored(t("lib_mpv_info"), "white"))
            
            all_series = get_cached_series_list()
            mal_id = None
            for s in all_series:
                if s['title'] == selected_series or s['title_en'] == selected_series:
                    mal_id = s['mal_id']
                    break
                    
            duration = get_duration_by_malid(mal_id) if mal_id else 21

            now = datetime.now()
            entry = {
                "timestamp": now.timestamp(),
                "dt_string": now.strftime("%d/%m/%Y %H:%M"),
                "title": selected_series,
                "title_en": selected_series,
                "episode": selected_ep,
                "source": "Doccli - Offline",
                "slug": None,
                "duration": duration 
            }
            ds.history.insert(0, entry)
            ds.save()
            
            try:
                subprocess.run(["mpv", file_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except FileNotFoundError:
                print(colored(t("lib_err_no_mpv"), "red"))
                input(t("lib_press_enter"))
                m_welcome()
                return