import os
import pathlib
from datetime import date, datetime

# From pip
from rich.align import Align
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from termcolor import colored

# Doccli modules
from storage import ds
from ui_utils import clear
from anilist_connector import get_anilist_global_stats, get_anilist_advanced_stats

def get_folder_size():
        
    if ds.settings[4] != "":
        folder_path = ds.settings[4]
    else:
        folder_path = os.path.join(os.getcwd(), "doccli_downloads")

    total_size = 0
    if os.path.exists(folder_path):
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
    return total_size

def get_user_rank(hours):
    if hours < 10: return "[#FFFFFF]🌱 Świeżak[/#FFFFFF]"
    elif hours < 25: return "[#E6F2FF]🌸 Widz[/#E6F2FF]"
    elif hours < 50: return "[#CCE6FF]🍙 Nowicjusz[/#CCE6FF]"
    elif hours < 75: return "[#99CCFF]🗡️ Uczeń[/#99CCFF]"
    elif hours < 100: return "[#66B3FF]🛡️ Giermek[/#66B3FF]"
    elif hours < 125: return "[#3399FF]🥷 Genin[/#3399FF]"
    elif hours < 150: return "[#0080FF]📜 Chuunin[/#0080FF]"
    elif hours < 200: return "[#0066CC]🌪️ Jonin[/#0066CC]"
    elif hours < 250: return "[#004C99]⚔️ Samuraj[/#004C99]"
    elif hours < 300: return "[#009999]🍂 Ronin[/#009999]"
    elif hours < 400: return "[#00CC99]🦊 Shinobi[/#00CC99]"
    elif hours < 500: return "[#00FF99]⭐ Otaku[/#00FF99]"
    elif hours < 600: return "[#33FF33]🦅 Zwiadowca[/#33FF33]"
    elif hours < 700: return "[#99FF33]🩸 Łowca[/#99FF33]"
    elif hours < 850: return "[#CCFF33]👁️ Zabójca[/#CCFF33]"
    elif hours < 1000: return "[#FFFF00]🏴‍☠️ Supernova[/#FFFF00]"
    elif hours < 1200: return "[#FFCC00]⚓ Kapitan[/#FFCC00]"
    elif hours < 1400: return "[#FF9900]🔮 Mistrz[/#FF9900]"
    elif hours < 1600: return "[#FF6600]🦸 Bohater[/#FF6600]"
    elif hours < 1800: return "[#FF3300]🧙‍♂️ Arcymag[/#FF3300]"
    elif hours < 2000: return "[#FF0000]👑 Król[/#FF0000]"
    elif hours < 2250: return "[#CC0000]🐉 Cesarz[/#CC0000]"
    elif hours < 2500: return "[#FF0066]🌌 Bóstwo[/#FF0066]"
    elif hours < 3000: return "[#FF00CC]👹 Tytan[/#FF00CC]"
    else: return "[#9900CC]👑 Hikikomori[/#9900CC]"

def m_stats():
    clear()

    ep_doccli = 0
    minutes_doccli = 0
    
    # --- OBLICZANIE NAWYKÓW ---
    maraton_dict = {}
    pora_dict = {"Nocny Marek (22-04)": 0, "Ranny Ptaszek (04-12)": 0, "Popołudniowy Chill (12-17)": 0, "Wieczorny Seans (17-22)": 0}
    online_count = 0
    offline_count = 0
    
    for item in ds.history:
        date_str = None
        is_offline = False
        
        if isinstance(item, dict):
            if item.get("source", "").startswith("Doccli"):
                ep_doccli += 1
                minutes_doccli += item.get("duration", 21)
                date_str = item.get("dt_string", "")
                is_offline = "Offline" in item.get("source", "")
        elif isinstance(item, str):
            ep_doccli += 1
            minutes_doccli += 21
            date_str = item[1:17] if len(item) > 17 else ""
            is_offline = "| Offline" in item
            
        # Zliczanie do maratonu i godzin
        if date_str and len(date_str) >= 16:
            date_only = date_str[:10]
            maraton_dict[date_only] = maraton_dict.get(date_only, 0) + 1
            
            try:
                hour = int(date_str[11:13])
                if 4 <= hour < 12: pora_dict["Ranny Ptaszek (04-12)"] += 1
                elif 12 <= hour < 17: pora_dict["Popołudniowy Chill (12-17)"] += 1
                elif 17 <= hour < 22: pora_dict["Wieczorny Seans (17-22)"] += 1
                else: pora_dict["Nocny Marek (22-04)"] += 1
            except: pass
            
            if is_offline: offline_count += 1
            else: online_count += 1

    max_maraton = max(maraton_dict.values()) if maraton_dict else 0
    max_maraton_date = max(maraton_dict, key=maraton_dict.get) if maraton_dict else "Brak"
    ulubiona_pora = max(pora_dict, key=pora_dict.get) if sum(pora_dict.values()) > 0 else "Brak danych"

    has_token = len(ds.settings) > 3 and ds.settings[3] != ""
    ep_anilist = 0
    minutes_anilist = 0
    adv_stats = None
    
    if has_token:
        ep_anilist, minutes_anilist = get_anilist_global_stats(ds.settings[3])
        adv_stats = get_anilist_advanced_stats(ds.settings[3])

    ep_total = max(ep_doccli, ep_anilist) if has_token else ep_doccli
    minutes_total = max(minutes_doccli, minutes_anilist) if has_token else minutes_doccli
    
    percent_doccli = 0
    if ep_total > 0:
        percent_doccli = round((ep_doccli / ep_total) * 100, 1)

    q_mylist = len(ds.mylist)
    ti_c = pathlib.Path(ds.config_dir).stat().st_mtime
    dt_c = datetime.fromtimestamp(ti_c).strftime("%d/%m/%Y")

    creation_dt = date.fromtimestamp(ti_c)
    now_dt = date.today()
    delta_dt = now_dt - creation_dt

    # Średnia tygodniowa w doccli
    weeks = max(1, delta_dt.days / 7.0)
    weekly_avg = round(ep_doccli / weeks, 1)

    hours = minutes_total // 60
    minutes = minutes_total % 60
    
    doccli_hours = minutes_doccli // 60
    doccli_minutes = minutes_doccli % 60
    
    size_bytes = get_folder_size()
    size_gb = round(size_bytes / (1024 ** 3), 2)

    last_watched = "Brak danych"
    if ds.history:
        first_entry = ds.history[0]
        if isinstance(first_entry, dict): clean_title = first_entry.get("title", "Nieznany")
        else:
            raw_history = str(first_entry) 
            clean_title = raw_history.split("]", 1)[1].strip() if "]" in raw_history else raw_history
        last_watched = clean_title[:32] + "..." if len(clean_title) > 35 else clean_title

    user_rank = get_user_rank(doccli_hours)
    console = Console()

    # --- OBLICZANIE SZEROKOŚCI RESPONSYWNEJ ---
    try:
        term_width = console.size.width
        if term_width < 80: term_width = 80
    except:
        term_width = 110

    max_ui_width = min(term_width - 2, 130)
    left_w = int(max_ui_width * 0.60)
    right_w = max_ui_width - left_w - 4

    # 1. AKTYWNOŚĆ
    table_activity = Table(show_header=False, box=None, padding=(0, 2), expand=True)
    table_activity.add_column("Statystyka", style="cyan")
    table_activity.add_column("Wartość", justify="right")
    table_activity.add_row("Obecna Ranga:", user_rank)
    table_activity.add_row("Obejrzane w doccli:", f"[cyan]{ep_doccli}[/cyan]")
    table_activity.add_row("Czas oglądania w doccli:", f"[cyan]{doccli_hours}h {doccli_minutes}m[/cyan]")
    table_activity.add_row("Odcinki obejrzane ogółem:", f"[red]{ep_total}[/red]")
    table_activity.add_row("Czas oglądania ogółem:", f"[cyan]{hours}h {minutes}m[/cyan]")
    table_activity.add_row("Ostatnio oglądane:", f"[white]{last_watched}[/white]")

    # 2. NAWYKI (Lokalne)
    table_habits = Table(show_header=False, box=None, padding=(0, 2), expand=True)
    table_habits.add_column("Statystyka", style="cyan")
    table_habits.add_column("Wartość", justify="right")
    table_habits.add_row("Życiowy maraton (1 dzień):", f"[red]{max_maraton}[/red] odc. ({max_maraton_date})")
    table_habits.add_row("Średnia tygodniowa:", f"[yellow]{weekly_avg}[/yellow] odc.")
    table_habits.add_row("Główna pora seansów:", f"[cyan]{ulubiona_pora}[/cyan]")
    table_habits.add_row("Sieć vs Dysk:", f"[cyan]{online_count}[/cyan] sieć / [green]{offline_count}[/green] dysk")

    # 3. ANILIST (Zewnętrzne)
    table_al = Table(show_header=False, box=None, padding=(0, 2), expand=True)
    table_al.add_column("Statystyka", style="cyan")
    table_al.add_column("Wartość", justify="right")
    
    if adv_stats:
        oldest_plan = adv_stats['oldest_planning'][:22] + "..." if len(adv_stats['oldest_planning']) > 25 else adv_stats['oldest_planning']
        table_al.add_row("Ukończone vs Reszta:", f"[green]{adv_stats['completed']}[/green] / [red]{adv_stats['not_completed']}[/red]")
        table_al.add_row("Kupka wstydu (Planowane):", f"[yellow]{adv_stats['planning_count']}[/yellow]")
        table_al.add_row("Najdłużej w kolejce:", f"[white]{oldest_plan}[/white]")
        table_al.add_row("Ulubione gatunki (Top 3):", f"[cyan]{adv_stats['genres']}[/cyan]")
        mean_s = f"{adv_stats['mean_score']}/100" if adv_stats['mean_score'] > 0 else "Brak"
        table_al.add_row("Średnia przyznanych ocen:", f"[bright_green]{mean_s}[/bright_green]")
    else:
        table_al.add_row("Status połączenia:", "[red]Brak danych z AniList[/red]")

    # 4. BIBLIOTEKA
    table_app = Table(show_header=False, box=None, padding=(0, 2), expand=True)
    table_app.add_column("Statystyka", style="cyan")
    table_app.add_column("Wartość", justify="right")
    table_app.add_row("Udział doccli w historii:", f"[yellow]{percent_doccli}%[/yellow]")
    table_app.add_row("Zajęte miejsce na dysku:", f"[green]{size_gb} GB[/green]")
    table_app.add_row("Instalacja doccli:", f"[white]{dt_c}[/white]")
    table_app.add_row("Wiek profilu:", f"[white]{delta_dt.days} dni[/white]")

    # RANGI - DUŻA LISTA
    table_legend = Table(show_header=False, box=None, padding=(0, 2), expand=True)
    table_legend.add_column("Ranga", style="white") 
    table_legend.add_column("Wymaganie", justify="right", style="white")
    table_legend.add_row("[#FFFFFF]🌱 Świeżak[/#FFFFFF]", "0 - 9 godz.")
    table_legend.add_row("[#E6F2FF]🌸 Widz[/#E6F2FF]", "10 - 24 godz.")
    table_legend.add_row("[#CCE6FF]🍙 Nowicjusz[/#CCE6FF]", "25 - 49 godz.")
    table_legend.add_row("[#99CCFF]🗡️ Uczeń[/#99CCFF]", "50 - 74 godz.")
    table_legend.add_row("[#66B3FF]🛡️ Giermek[/#66B3FF]", "75 - 99 godz.")
    table_legend.add_row("[#3399FF]🥷 Genin[/#3399FF]", "100 - 124 godz.")
    table_legend.add_row("[#0080FF]📜 Chuunin[/#0080FF]", "125 - 149 godz.")
    table_legend.add_row("[#0066CC]🌪️ Jonin[/#0066CC]", "150 - 199 godz.")
    table_legend.add_row("[#004C99]⚔️ Samuraj[/#004C99]", "200 - 249 godz.")
    table_legend.add_row("[#009999]🍂 Ronin[/#009999]", "250 - 299 godz.")
    table_legend.add_row("[#00CC99]🦊 Shinobi[/#00CC99]", "300 - 399 godz.")
    table_legend.add_row("[#00FF99]⭐ Otaku[/#00FF99]", "400 - 499 godz.")
    table_legend.add_row("[#33FF33]🦅 Zwiadowca[/#33FF33]", "500 - 599 godz.")
    table_legend.add_row("[#99FF33]🩸 Łowca[/#99FF33]", "600 - 699 godz.")
    table_legend.add_row("[#CCFF33]👁️ Zabójca[/#CCFF33]", "700 - 849 godz.")
    table_legend.add_row("[#FFFF00]🏴‍☠️ Supernova[/#FFFF00]", "850 - 999 godz.")
    table_legend.add_row("[#FFCC00]⚓ Kapitan[/#FFCC00]", "1000 - 1199 godz.")
    table_legend.add_row("[#FF9900]🔮 Mistrz[/#FF9900]", "1200 - 1399 godz.")
    table_legend.add_row("[#FF6600]🦸 Bohater[/#FF6600]", "1400 - 1599 godz.")
    table_legend.add_row("[#FF3300]🧙‍♂️ Arcymag[/#FF3300]", "1600 - 1799 godz.")
    table_legend.add_row("[#FF0000]👑 Król[/#FF0000]", "1800 - 1999 godz.")
    table_legend.add_row("[#CC0000]🐉 Cesarz[/#CC0000]", "2000 - 2249 godz.")
    table_legend.add_row("[#FF0066]🌌 Bóstwo[/#FF0066]", "2250 - 2499 godz.")
    table_legend.add_row("[#FF00CC]👹 Tytan[/#FF00CC]", "2500 - 2999 godz.")
    table_legend.add_row("[#9900CC]👑 Hikikomori[/#9900CC]", "3000+ godz.")

    # PANELE O DYNAMICZNEJ SZEROKOŚCI
    panel_activity = Panel(table_activity, title="[yellow]🎬 Twój Profil[/yellow]", border_style="cyan", width=left_w)
    panel_habits = Panel(table_habits, title="[yellow]🧠 Twoje Nawyki (Doccli)[/yellow]", border_style="cyan", width=left_w)
    panel_al = Panel(table_al, title="[yellow]☁️ Statystyki Konta (AniList)[/yellow]", border_style="cyan", width=left_w)
    panel_app = Panel(table_app, title="[yellow]📁 Biblioteka i Dane[/yellow]", border_style="cyan", width=left_w)
    
    panel_legend = Panel(table_legend, title="[yellow]🏆 Legenda Rang[/yellow]", border_style="cyan", width=right_w)

    left_column = Group(
        panel_activity,
        panel_habits,
        panel_al,
        panel_app
    )

    dashboard_grid = Table.grid(padding=(0, 4))
    dashboard_grid.add_column(justify="left")
    dashboard_grid.add_column(justify="left")
    
    dashboard_grid.add_row(left_column, panel_legend)

    # WYŚWIETLANIE
    console.print(Align.center(dashboard_grid))
    
    print('\n')
    input(colored("Naciśnij enter aby wrócić do menu głównego...", "yellow"))
    return