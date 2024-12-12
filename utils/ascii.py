import os

DOCCLI_LOGO_ASCII="""
.----------------------------------.
| ____   ___   ____ ____ _     ___ |
||  _ \ / _ \ / ___/ ___| |   |_ _||
|| | | | | | | |  | |   | |    | | |
|| |_| | |_| | |__| |___| |___ | | |
||____/ \___/ \____\____|_____|___||
|               v3.0               |
'----------------------------------'
"""

def doccli_logo_centered():
    terminal_width = os.get_terminal_size().columns
    art_lines = DOCCLI_LOGO_ASCII.splitlines()
    return "\n".join(line.center(terminal_width) for line in art_lines)