import subprocess
import time
import requests
import shutil

from termcolor import colored
import os
from utils.ascii import doccli_logo_centered_70p

def run_fzf(header, all_details, choices):

    choices_str = ''
    for choice in choices:
        choices_str += choice + '\n'

    # Pliki dla detali
    doccli_fzf_path = '/tmp/doccli_fzf'
    if not os.path.exists(doccli_fzf_path):
        os.mkdir('/tmp/doccli_fzf')

    for file in os.listdir(path=doccli_fzf_path):
        file_path = os.path.join(doccli_fzf_path, file)
        os.remove(file_path)

    for detail in all_details:
        file_path = os.path.join(doccli_fzf_path, str(all_details.index(detail) + 1) + '.')
        with open(file_path, 'w') as f:
            for index in detail:
                if detail.index(index) == 0:
                    # Handle image
                    response = requests.get(index)
                    image_path = os.path.join(doccli_fzf_path, str(all_details.index(detail) + 1) + '._')
                    with open(image_path, 'wb') as file:
                        file.write(response.content)
                elif detail.index(index) % 2 == 0:
                    f.write(colored(str(index), 'green'))
                else:
                    f.write(colored(str(index) + '\n', 'white'))


    try:
        terminal_size = shutil.get_terminal_size()
        columns, rows = terminal_size.columns, terminal_size.lines
        height = int(rows)
        width = int(columns * 0.35)

        result = subprocess.run(
            [
                "fzf",
                "--info=hidden",
                "--header-first",
                "--height=100%",
                "--no-margin",
                "+m",
                "-i",
                "--exact",
                "--tabstop=1",
                "--layout=reverse",
                "--border",
                f"--header={header}",
                f"--preview=chafa --size={width}x{height} /tmp/doccli_fzf/{{1}}_",
                f"--bind=ctrl-i:preview(batcat -p --color=always /tmp/doccli_fzf/{{1}})",
                f"--bind=ctrl-c:preview(chafa --size={width}x{height} /tmp/doccli_fzf/{{1}}_)",
                "--preview-window=left:40%:wrap",
                "--cycle"
            ],
            text=True,
            input=choices_str,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        if result.returncode == 0:
            return result.stdout.strip()  # Wybrana opcja
        else:
            return None  # Użytkownik anulował wybór

    except FileNotFoundError:
        print("fzf nie jest zainstalowany lub nie znajduje się w PATH.")
        return None
