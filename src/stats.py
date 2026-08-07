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
from i18n import t

def get_folder_size():
        
    if ds.settings.get("download_path") != "":
        folder_path = ds.settings["download_path"]
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
    if hours < 10: return f"[#FFFFFF]🌱 {t('rank_freshman')}[/#FFFFFF]"
    elif hours < 25: return f"[#E6F2FF]🌸 {t('rank_viewer')}[/#E6F2FF]"
    elif hours < 50: return f"[#CCE6FF]🍙 {t('rank_novice')}[/#CCE6FF]"
    elif hours < 75: return f"[#99CCFF]🗡️ {t('rank_disciple')}[/#99CCFF]"
    elif hours < 100: return f"[#66B3FF]🛡️ {t('rank_squire')}[/#66B3FF]"
    elif hours < 125: return f"[#3399FF]🥷 {t('rank_genin')}[/#3399FF]"
    elif hours < 150: return f"[#0080FF]📜 {t('rank_chuunin')}[/#0080FF]"
    elif hours < 200: return f"[#0066CC]🌪️ {t('rank_jonin')}[/#0066CC]"
    elif hours < 250: return f"[#004C99]⚔️ {t('rank_samurai')}[/#004C99]"
    elif hours < 300: return f"[#009999]🍂 {t('rank_ronin')}[/#009999]"
    elif hours < 400: return f"[#00CC99]🦊 {t('rank_shinobi')}[/#00CC99]"
    elif hours < 500: return f"[#00FF99]⭐ {t('rank_otaku')}[/#00FF99]"
    elif hours < 600: return f"[#33FF33]🦅 {t('rank_scout')}[/#33FF33]"
    elif hours < 700: return f"[#99FF33]🩸 {t('rank_hunter')}[/#99FF33]"
    elif hours < 850: return f"[#CCFF33]👁️ {t('rank_assassin')}[/#CCFF33]"
    elif hours < 1000: return f"[#FFFF00]🏴‍☠️ {t('rank_supernova')}[/#FFFF00]"
    elif hours < 1200: return f"[#FFCC00]⚓ {t('rank_captain')}[/#FFCC00]"
    elif hours < 1400: return f"[#FF9900]🔮 {t('rank_master')}[/#FF9900]"
    elif hours < 1600: return f"[#FF6600]🦸 {t('rank_hero')}[/#FF6600]"
    elif hours < 1800: return f"[#FF3300]🧙‍♂️ {t('rank_archmage')}[/#FF3300]"
    elif hours < 2000: return f"[#FF0000]👑 {t('rank_king')}[/#FF0000]"
    elif hours < 2250: return f"[#CC0000]🐉 {t('rank_emperor')}[/#CC0000]"
    elif hours < 2500: return f"[#FF0066]🌌 {t('rank_deity')}[/#FF0066]"
    elif hours < 3000: return f"[#FF00CC]👹 {t('rank_titan')}[/#FF00CC]"
    else: return f"[#9900CC]👑 {t('rank_hikikomori')}[/#99CCFF]"

def m_stats():
    clear()

    ep_doccli = 0
    minutes_doccli = 0
    
    # --- OBLICZANIE NAWYKÓW ---
    maraton_dict = {}
    pora_dict = {
        t("stat_night"): 0, 
        t("stat_early"): 0, 
        t("stat_chill"): 0, 
        t("stat_evening"): 0
    }
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
                if 4 <= hour < 12: pora_dict[t("stat_early")] += 1
                elif 12 <= hour < 17: pora_dict[t("stat_chill")] += 1
                elif 17 <= hour < 22: pora_dict[t("stat_evening")] += 1
                else: pora_dict[t("stat_night")] += 1
            except: pass
            
            if is_offline: offline_count += 1
            else: online_count += 1

    max_maraton = max(maraton_dict.values()) if maraton_dict else 0
    max_maraton_date = max(maraton_dict, key=maraton_dict.get) if maraton_dict else t("stat_none")
    ulubiona_pora = max(pora_dict, key=pora_dict.get) if sum(pora_dict.values()) > 0 else t("stat_no_data")

    has_token = ds.settings.get("anilist_token") != ""
    ep_anilist = 0
    minutes_anilist = 0
    adv_stats = None
    
    if has_token:
        ep_anilist, minutes_anilist = get_anilist_global_stats(ds.settings["anilist_token"])
        adv_stats = get_anilist_advanced_stats(ds.settings["anilist_token"])

    ep_total = max(ep_doccli, ep_anilist) if has_token else ep_doccli
    minutes_total = max(minutes_doccli, minutes_anilist) if has_token else minutes_doccli
    
    percent_doccli = 0
    if ep_total > 0:
        percent_doccli = round((ep_doccli / ep_total) * 100, 1)

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

    last_watched = t("stat_no_data")
    if ds.history:
        first_entry = ds.history[0]
        if isinstance(first_entry, dict): clean_title = first_entry.get("title", t("player_unknown_anime"))
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
    table_activity.add_row(t("stat_lbl_rank"), user_rank)
    table_activity.add_row(t("stat_lbl_doccli_eps"), f"[cyan]{ep_doccli}[/cyan]")
    table_activity.add_row(t("stat_lbl_doccli_time"), f"[cyan]{doccli_hours}h {doccli_minutes}m[/cyan]")
    table_activity.add_row(t("stat_lbl_total_eps"), f"[red]{ep_total}[/red]")
    table_activity.add_row(t("stat_lbl_total_time"), f"[cyan]{hours}h {minutes}m[/cyan]")
    table_activity.add_row(t("stat_lbl_last"), f"[white]{last_watched}[/white]")

    # 2. NAWYKI (Lokalne)
    table_habits = Table(show_header=False, box=None, padding=(0, 2), expand=True)
    table_habits.add_column("Statystyka", style="cyan")
    table_habits.add_column("Wartość", justify="right")
    table_habits.add_row(t("stat_lbl_marathon"), f"[red]{max_maraton}[/red] odc. ({max_maraton_date})")
    table_habits.add_row(t("stat_lbl_weekly"), f"[yellow]{weekly_avg}[/yellow] odc.")
    table_habits.add_row(t("stat_lbl_prime_time"), f"[cyan]{ulubiona_pora}[/cyan]")
    table_habits.add_row(t("stat_lbl_net_disk"), f"[cyan]{online_count}[/cyan] {t('stat_net_str')} / [green]{offline_count}[/green] {t('stat_disk_str')}")

    # 3. ANILIST (Zewnętrzne)
    table_al = Table(show_header=False, box=None, padding=(0, 2), expand=True)
    table_al.add_column("Statystyka", style="cyan")
    table_al.add_column("Wartość", justify="right")
    
    if adv_stats:
        oldest_plan = adv_stats['oldest_planning'][:22] + "..." if len(adv_stats['oldest_planning']) > 25 else adv_stats['oldest_planning']
        table_al.add_row(t("stat_lbl_completed_rest"), f"[green]{adv_stats['completed']}[/green] / [red]{adv_stats['not_completed']}[/red]")
        table_al.add_row(t("stat_lbl_planning"), f"[yellow]{adv_stats['planning_count']}[/yellow]")
        table_al.add_row(t("stat_lbl_oldest_queue"), f"[white]{oldest_plan}[/white]")
        table_al.add_row(t("stat_lbl_top_genres"), f"[cyan]{adv_stats['genres']}[/cyan]")
        mean_s = f"{adv_stats['mean_score']}/100" if adv_stats['mean_score'] > 0 else t("stat_none")
        table_al.add_row(t("stat_lbl_mean_score"), f"[bright_green]{mean_s}[/bright_green]")
    else:
        table_al.add_row(t("stat_lbl_al_status"), f"[red]{t('stat_al_no_data')}[/red]")

    # 4. BIBLIOTEKA
    table_app = Table(show_header=False, box=None, padding=(0, 2), expand=True)
    table_app.add_column("Statystyka", style="cyan")
    table_app.add_column("Wartość", justify="right")
    table_app.add_row(t("stat_lbl_share"), f"[yellow]{percent_doccli}%[/yellow]")
    table_app.add_row(t("stat_lbl_size"), f"[green]{size_gb} GB[/green]")
    table_app.add_row(t("stat_lbl_install"), f"[white]{dt_c}[/white]")
    table_app.add_row(t("stat_lbl_age"), f"[white]{delta_dt.days} {t('stat_days')}[/white]")

    # RANGI - DUŻA LISTA
    req_h = t("stat_req_hours")
    table_legend = Table(show_header=False, box=None, padding=(0, 2), expand=True)
    table_legend.add_column("Ranga", style="white") 
    table_legend.add_column("Wymaganie", justify="right", style="white")
    table_legend.add_row(f"[#FFFFFF]🌱 {t('rank_freshman')}[/#FFFFFF]", f"0 - 9 {req_h}")
    table_legend.add_row(f"[#E6F2FF]🌸 {t('rank_viewer')}[/#E6F2FF]", f"10 - 24 {req_h}")
    table_legend.add_row(f"[#CCE6FF]🍙 {t('rank_novice')}[/#CCE6FF]", f"25 - 49 {req_h}")
    table_legend.add_row(f"[#99CCFF]🗡️ {t('rank_disciple')}[/#99CCFF]", f"50 - 74 {req_h}")
    table_legend.add_row(f"[#66B3FF]🛡️ {t('rank_squire')}[/#66B3FF]", f"75 - 99 {req_h}")
    table_legend.add_row(f"[#3399FF]🥷 {t('rank_genin')}[/#3399FF]", f"100 - 124 {req_h}")
    table_legend.add_row(f"[#0080FF]📜 {t('rank_chuunin')}[/#0080FF]", f"125 - 149 {req_h}")
    table_legend.add_row(f"[#0066CC]🌪️ {t('rank_jonin')}[/#0066CC]", f"150 - 199 {req_h}")
    table_legend.add_row(f"[#004C99]⚔️ {t('rank_samurai')}[/#004C99]", f"200 - 249 {req_h}")
    table_legend.add_row(f"[#009999]🍂 {t('rank_ronin')}[/#009999]", f"250 - 299 {req_h}")
    table_legend.add_row(f"[#00CC99]🦊 {t('rank_shinobi')}[/#00CC99]", f"300 - 399 {req_h}")
    table_legend.add_row(f"[#00FF99]⭐ {t('rank_otaku')}[/#00FF99]", f"400 - 499 {req_h}")
    table_legend.add_row(f"[#33FF33]🦅 {t('rank_scout')}[/#33FF33]", f"500 - 599 {req_h}")
    table_legend.add_row(f"[#99FF33]🩸 {t('rank_hunter')}[/#99FF33]", f"600 - 699 {req_h}")
    table_legend.add_row(f"[#CCFF33]👁️ {t('rank_assassin')}[/#CCFF33]", f"700 - 849 {req_h}")
    table_legend.add_row(f"[#FFFF00]🏴‍☠️ {t('rank_supernova')}[/#FFFF00]", f"850 - 999 {req_h}")
    table_legend.add_row(f"[#FFCC00]⚓ {t('rank_captain')}[/#FFCC00]", f"1000 - 1199 {req_h}")
    table_legend.add_row(f"[#FF9900]🔮 {t('rank_master')}[/#FF9900]", f"1200 - 1399 {req_h}")
    table_legend.add_row(f"[#FF6600]🦸 {t('rank_hero')}[/#FF6600]", f"1400 - 1599 {req_h}")
    table_legend.add_row(f"[#FF3300]🧙‍♂️ {t('rank_archmage')}[/#FF3300]", f"1600 - 1799 {req_h}")
    table_legend.add_row(f"[#FF0000]👑 {t('rank_king')}[/#FF0000]", f"1800 - 1999 {req_h}")
    table_legend.add_row(f"[#CC0000]🐉 {t('rank_emperor')}[/#CC0000]", f"2000 - 2249 {req_h}")
    table_legend.add_row(f"[#FF0066]🌌 {t('rank_deity')}[/#FF0066]", f"2250 - 2499 {req_h}")
    table_legend.add_row(f"[#FF00CC]👹 {t('rank_titan')}[/#FF00CC]", f"2500 - 2999 {req_h}")
    table_legend.add_row(f"[#9900CC]👑 {t('rank_hikikomori')}[/#9900CC]", f"3000+ {req_h}")

    # PANELE O DYNAMICZNEJ SZEROKOŚCI
    panel_activity = Panel(table_activity, title=f"[yellow]{t('stat_panel_profile')}[/yellow]", border_style="cyan", width=left_w)
    panel_habits = Panel(table_habits, title=f"[yellow]{t('stat_panel_habits')}[/yellow]", border_style="cyan", width=left_w)
    panel_al = Panel(table_al, title=f"[yellow]{t('stat_panel_anilist')}[/yellow]", border_style="cyan", width=left_w)
    panel_app = Panel(table_app, title=f"[yellow]{t('stat_panel_library')}[/yellow]", border_style="cyan", width=left_w)
    
    panel_legend = Panel(table_legend, title=f"[yellow]{t('stat_panel_legend')}[/yellow]", border_style="cyan", width=right_w)

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
    input(colored(t("stat_return_prompt"), "yellow"))
    return