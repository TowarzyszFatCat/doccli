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

TRENDING_LOGO_ASCII="""
.___________________________________________________.
| _   _    _       ____ _____   _    ____ ___ _____ |
|| \ | |  / \     / ___|__  /  / \  / ___|_ _| ____||
||  \| | / _ \   | |     / /  / _ \ \___ \| ||  _|  |
|| |\  |/ ___ \  | |___ / /_ / ___ \ ___) | || |___ |
||_| \_/_/   \_\  \____/____/_/   \_\____/___|_____||
'---------------------------------------------------'
"""


def doccli_logo_centered():
    terminal_width = os.get_terminal_size().columns
    art_lines = DOCCLI_LOGO_ASCII.splitlines()
    return "\n".join(line.center(terminal_width) for line in art_lines)

def doccli_logo_centered_70p():
    terminal_width = os.get_terminal_size().columns
    usable_width = int(terminal_width * 0.65)
    art_lines = DOCCLI_LOGO_ASCII.splitlines()
    return "\n".join(line.center(usable_width) for line in art_lines)

def trending_logo_centered_70p():
    terminal_width = os.get_terminal_size().columns
    usable_width = int(terminal_width * 0.65)
    art_lines = TRENDING_LOGO_ASCII.splitlines()
    return "\n".join(line.center(usable_width) for line in art_lines)
