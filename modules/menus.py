from apis import anilist
from utils import trending_logo_centered, fuzzy_menu, gen_rating, clear_terminal

def trending_menu():
    trending_anime = anilist.get_trending_anime()
    
    mal_ids = []
    choices = []
    index = 0
    
    for anime in trending_anime:
        index += 1
        mal_ids.append(anime['idMal'])
        choices.append(str(index) + '. ' + anime['title']['english'] + ' | ' + gen_rating(anime['averageScore']))


    fuzzy_menu(message=trending_logo_centered(),
                instruction="Wybierz anime: ",
                long_instruction="Lista top 25 najbardziej popularnych anime na dzień dzisiejszy",
                choices=choices
               )


clear_terminal()
trending_menu()
