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

def get_folder_size(folder_path="doccli_downloads"):
    total_size = 0
    if os.path.exists(folder_path):
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
    return total_size

def get_user_rank(hours):
    if hours < 10:
        return "[cyan]🌱 Niedzielny Widz[/cyan]"
    elif hours < 25:
        return "[green]🌸 Nowicjusz[/green]"
    elif hours < 50:
        return "[orange]🗡️ Uczeń Shounenów[/orange]"
    elif hours < 100:
        return "[blue]🥷 Genin[/blue]"
    elif hours < 250:
        return "[violet]⭐ Otaku[/violet]"
    elif hours < 500:
        return "[magenta]⚔️ Łowca Demonów[/magenta]"
    elif hours < 1000:
        return "[red]🔥 Weteran [/red]"
    else:
        return "[yellow]👑 Hikikomori[yellow]"

def m_stats():
    clear()

    ep_played = len(ds.history)
    q_mylist = len(ds.mylist)

    ti_c = pathlib.Path(ds.config_dir).stat().st_mtime
    dt_c = datetime.fromtimestamp(ti_c).strftime("%d/%m/%Y")

    creation_dt = date.fromtimestamp(ti_c)
    now_dt = date.today()
    delta_dt = now_dt - creation_dt

    total_minutes = ep_played * 21
    hours = total_minutes // 60
    minutes = total_minutes % 60
    
    size_bytes = get_folder_size()
    size_gb = round(size_bytes / (1024 ** 3), 2)

    last_watched = "Brak danych"
    if ds.history:
        raw_history = str(ds.history[0]) 
        if "]" in raw_history:
            clean_title = raw_history.split("]", 1)[1].strip()
        else:
            clean_title = raw_history
            
        if len(clean_title) > 35:
            last_watched = clean_title[:32] + "..."
        else:
            last_watched = clean_title

    user_rank = get_user_rank(hours)

    console = Console()

    # AKTYWNOŚĆ
    table_activity = Table(show_header=False, box=None, padding=(0, 2))
    table_activity.add_column("Statystyka", style="cyan", width=25)
    table_activity.add_column("Wartość", justify="right", style="bold")
    table_activity.add_row("Obecna Ranga:", user_rank)
    table_activity.add_row("Odtworzone odcinki:", f"[bold red]{ep_played}[/bold red]")
    table_activity.add_row("Czas oglądania (21m/odc):", f"[yellow]{hours}h {minutes}m[/yellow]")
    table_activity.add_row("Ostatnio oglądane:", f"[magenta]{last_watched}[/magenta]")

    # BIBLIOTEKA
    table_app = Table(show_header=False, box=None, padding=(0, 2))
    table_app.add_column("Statystyka", style="cyan", width=25)
    table_app.add_column("Wartość", justify="right", style="bold")
    table_app.add_row("Zapisane na liście:", f"[bold red]{q_mylist}[/bold red]")
    table_app.add_row("Zajęte miejsce na dysku:", f"[green]{size_gb} GB[/green]")
    table_app.add_row("Pierwsza instalacja doccli:", f"[white]{dt_c}[/white]")
    table_app.add_row("Wiek profilu:", f"[white]{delta_dt.days} dni[/white]")

    # RANGI
    table_legend = Table(show_header=False, box=None, padding=(0, 2))
    table_legend.add_column("Ranga", style="bold", width=30) 
    table_legend.add_column("Wymaganie", justify="right", style="dim white")
    table_legend.add_row("[cyan]🌱 Niedzielny Widz[/cyan]", "0 - 9 godz.")
    table_legend.add_row("[green]🌸 Nowicjusz[/green]", "10 - 24 godz.")
    table_legend.add_row("[yellow]🗡️ Uczeń Shounenów[/yellow]", "25 - 49 godz.")
    table_legend.add_row("[blue]🥷 Genin[/blue]", "50 - 99 godz.")
    table_legend.add_row("[violet]⭐ Otaku[/violet]", "100 - 249 godz.")
    table_legend.add_row("[magenta]⚔️ Łowca Demonów[/magenta]", "250 - 499 godz.")
    table_legend.add_row("[red]🔥 Weteran [/red]", "500 - 999 godz.")
    table_legend.add_row("[yellow]👑 Hikikomori[yellow]", "1000+ godz.")


    panel_activity = Panel(table_activity, title="[bold yellow]🎬 Twój Profil[/bold yellow]", border_style="cyan", expand=False)
    panel_app = Panel(table_app, title="[bold yellow]📁 Biblioteka i Dane[/bold yellow]", border_style="cyan", expand=False)
    panel_legend = Panel(table_legend, title="[bold yellow]🏆 Legenda Rang[/bold yellow]", border_style="cyan", expand=False)


    dashboard = Group(
        Align.center(panel_activity),
        Align.center(panel_app),
        Align.center(panel_legend)
    )

    main_panel = Panel(
        dashboard, 
        title="[bold magenta]📊 STATYSTYKI DOCCLI[/bold magenta]", 
        border_style="blue", 
        expand=False,
        padding=(1, 4)
    )

    console.print(Align.center(main_panel))
    
    print('\n')
    input(colored("Naciśnij enter aby wrócić do menu głównego...", "yellow"))
    return