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
        print(colored(f"[BŁĄD] Twój folder pobierania jeszcze nie istnieje ({downloads_dir}).", "red"))
        print(colored("Najpierw musisz pobrać jakieś anime!", "yellow"))
        print('')
        input(colored("Naciśnij Enter, aby wrócić do menu...", "yellow"))
        m_welcome()
        return
        
    series_list = [d for d in os.listdir(downloads_dir) if os.path.isdir(os.path.join(downloads_dir, d))]
    
    if not series_list:
        print(colored("[INFO] Twój folder doccli_downloads jest pusty.", "yellow"))
        print('')
        input(colored("Naciśnij Enter, aby wrócić do menu...", "yellow"))
        m_welcome()
        return
        
    series_list.append("Wróć do menu głównego")
    
    selected_series = open_menu(
        choices=series_list, 
        prompt='Wybierz serię z dysku: ', 
        height=10, 
        message=MOJA_BIBLIOTEKA
    )
    
    if selected_series == "Wróć do menu głównego":
        m_welcome()
        return

    while True:
        clear()
        series_path = os.path.join(downloads_dir, selected_series)
        
        episodes_list = [f for f in os.listdir(series_path) if os.path.isfile(os.path.join(series_path, f))]
        episodes_list.sort()
        
        if not episodes_list:
            print(colored(f"Brak plików wideo w folderze {selected_series}.", "red"))
            input(colored("Naciśnij Enter, aby wrócić do menu...", "yellow"))
            m_welcome()
            return
            
        choices = ["Oglądaj automatycznie"] + episodes_list + ["Wróć do wyboru serii"]
        
        selected_ep = open_menu(
            choices=choices, 
            prompt=f'Wybierz odcinek ({selected_series}): ', 
            height=10, 
            message=MOJA_BIBLIOTEKA
        )
        
        if selected_ep == "Wróć do wyboru serii":
            m_local_library()
            return
            
        elif selected_ep == "Oglądaj automatycznie":
            for ep in episodes_list:
                file_path = os.path.join(series_path, ep)
                clear()
                print(colored(f"Oglądanie automatyczne: {ep}", "cyan"))
                print(colored("Wciśnij 'Q' w obrębie okna MPV, lub zamknij je aby przerwać seans i wrócić do menu.", "white"))
                
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
                        print(colored("\n[INFO] Przerwano oglądanie automatyczne.", "yellow"))
                        input("Naciśnij Enter...")
                        break
                except FileNotFoundError:
                    print(colored("[BŁĄD] Nie znaleziono odtwarzacza mpv!", "red"))
                    input("Naciśnij Enter...")
                    m_welcome()
                    return
        else:
            file_path = os.path.join(series_path, selected_ep)
            clear()
            print(colored(f"Odtwarzam z dysku: {selected_ep}", "cyan"))
            print(colored("Wciśnij 'Q' w obrębie okna MPV, lub zamknij je aby przerwać seans i wrócić do menu.", "white"))
            
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
                print(colored("[BŁĄD] Nie znaleziono odtwarzacza mpv!", "red"))
                input("Naciśnij Enter...")
                m_welcome()
                return