import time

# From pip
import pypresence.exceptions
from pypresence import Presence, ActivityType

# Doccli modules
from i18n import t

discord_data = [t("menu_main"), t("rpc_loading")]
start_time = None
running = False
RPC = None

try:
    client_ID = '1206583480771936318'
    RPC = Presence(client_ID)
    RPC.connect()
    start_time = time.time()
except Exception: 
    # Discord jest wyłączony
    RPC = None


def update_rpc(first_line, second_line):
    global discord_data
    discord_data = [first_line, second_line]


def set_running(val):
    global running
    running = val


def start_rpc():
    while running:
        # Aktualizuj tylko, jeśli udało się połączyć przy starcie
        if RPC is not None:
            try:
                RPC.update(
                    activity_type=ActivityType.WATCHING, 
                    state=discord_data[1], 
                    details=discord_data[0], 
                    large_image='icon_1', 
                    large_text=t("rpc_large_text"), 
                    buttons=[
                        {"label": "GitHub", "url": "https://github.com/TowarzyszFatCat/doccli"}, 
                        {"label": t("rpc_discord_btn"), "url": "https://discord.gg/FgfSM7bSEK"}
                    ], 
                    start=start_time
                )
            except Exception:
                # Jeśli ktoś zamknie Discorda w trakcie oglądania
                pass
                
        time.sleep(5)