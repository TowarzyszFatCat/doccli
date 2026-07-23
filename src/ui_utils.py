import os
import shutil
import sys
import tempfile
import textwrap
import html
import re

# From pip
from InquirerPy import inquirer
from PIL import Image
from termcolor import colored
import requests

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def get_terminal_size():
    columns, rows = os.get_terminal_size()
    return columns, rows

def center_text(text: str) -> str:
    # Odejmujemy 1 od szerokości terminala
    terminal_width = os.get_terminal_size().columns - 1
    art_lines = text.splitlines()
    
    # Zostawiamy oryginalne .center() bez rstrip()
    return "\n".join(line.center(terminal_width) for line in art_lines)

def open_menu(choices, prompt='Prompt', border=True, qmark='', message='', pointer='>', cycle=True, height=10, image=None, description=None):
    clear()

    if image:
        try:
            response = requests.get(image)
            image_path = os.path.join(tempfile.gettempdir(), "cover.png")
            with open(image_path, 'wb') as file:
                file.write(response.content)

            term_width, term_height = get_terminal_size()
            
            avail_height = max(5, term_height - height - 7) 
            chafa_height = max(3, avail_height)

            img_ratio = 0.7
            margin_ratio = 0.0

            try:
                img = Image.open(image_path).convert("RGBA")
                img_w, img_h = img.size
                
                pad_pixels = int(img_w * 0.15) 
                new_w = pad_pixels + img_w
                
                padded_img = Image.new("RGBA", (new_w, img_h), (0, 0, 0, 0))
                padded_img.paste(img, (pad_pixels, 0))
                padded_img.save(image_path, "PNG")
                
                img_ratio = new_w / img_h
                margin_ratio = pad_pixels / img_h
            except Exception:
                pass

            if shutil.which('chafa') is not None:
                char_aspect = 2.0 
                chafa_units_h = chafa_height * char_aspect
                
                rendered_cols = int(chafa_units_h * img_ratio)
                margin_cols = int(chafa_units_h * margin_ratio)
                
                text_start_col = rendered_cols + margin_cols + 4
                
                if text_start_col >= term_width - 15:
                    text_start_col = int(term_width * 0.4)
                    
                text_width = term_width - text_start_col - 2

                print("\0337", end="")
                sys.stdout.flush()

                os.system(f"chafa -s {term_width}x{chafa_height} {image_path}")
                
                if description:
                    # 1. Odkodowanie znaków specjalnych
                    clean_desc = html.unescape(description)
                    
                    # 2. Zamiana tagów HTML na pojedynczą spację
                    clean_desc = re.sub(r'<[^>]+>', ' ', clean_desc)
                    
                    # 3. Zgniecenie wszystkich spacji i enterów w jedną spację
                    clean_desc = re.sub(r'\s+', ' ', clean_desc).strip()
                    
                    wrapped_desc = textwrap.wrap(clean_desc, width=text_width)
                    
                    header_text = "Opis z AniList:"
                    colored_header = colored(header_text, "cyan") 
                    
                    wrapped_desc.insert(0, colored_header)
                    wrapped_desc.insert(1, "") 
                else:
                    wrapped_desc = []

                for i, line in enumerate(wrapped_desc[:avail_height]):
                    row = i + 2 
                    print(f"\033[{row};{text_start_col}H{line}", end="")

                menu_row = avail_height + 2
                print(f"\033[{menu_row};1H", end="")
                sys.stdout.flush()
                    
            else:
                print(center_text("Brak narzędzia 'chafa' do wyświetlania okładek."))
                
        except Exception as e:
            pass

    try:
        action = inquirer.fuzzy(
            message=message if message.startswith('[') else center_text(message),
            choices=choices,
            border=border,
            qmark=qmark,
            prompt=prompt,
            long_instruction="Ctrl+C = Cofnij / Menu główne",
            pointer=pointer,
            cycle=cycle,
            height=height,
        ).execute()
    except KeyboardInterrupt:
        clear()
        back_keywords = ["cofnij", "wróć", "menu główne", "zamknij", "anuluj"]
        for choice in choices:
            if any(kw in str(choice).lower() for kw in back_keywords):
                return choice
        return choices[0]

    clear() 

    try:
        return choices[choices.index(action)]
    except ValueError:
        return open_menu(choices=choices, prompt=prompt, border=border, qmark="Nie znaleziono na liście, wyszukaj ponownie", message=message, pointer=pointer, cycle=cycle, height=height)