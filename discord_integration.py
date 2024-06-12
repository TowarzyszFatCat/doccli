import time

import pypresence.exceptions
from pypresence import Presence

discord_data = ["Menu główne", "Ładowanie..."]
start_time = None


try:
    client_ID = '1206583480771936318'
    RPC = Presence(client_ID)
    RPC.connect()
    start_time = time.time()
except: # ojojoj niebezpiecznie
    pass


def update_rpc(first_line, second_line):
    global discord_data
    discord_data = [first_line, second_line]


def start_rpc():
    while True:
        RPC.update(state=discord_data[1], details=discord_data[0], large_image='icon_1', large_text="Doccli - oglądaj anime bezpośrednio ze swojego terminalu!", buttons=[{"label": "GitHub", "url": "https://github.com/TowarzyszFatCat/doccli"}, {"label": "Discord Projektu", "url": "https://discord.gg/FgfSM7bSEK"}], start=start_time)
        time.sleep(5)