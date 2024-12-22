from apis import anilist
from utils import trending_logo_centered_60p, fuzzy_menu, gen_rating, clear_terminal, run_fzf
from time import sleep

def trending_menu():
    trending_anime = anilist.get_trending_anime()
    
    mal_ids = []    # MalID wszystkich pozycji.
    choices = []    # Wybory jako tablica
    all_details = []
    i = 0
    
    for anime in trending_anime:
        i += 1
        mal_ids.append(anime['idMal'])
        item = str(i) + '. ' + str(anime['title']['romaji'])
        choices.append(item)

        anime_details = []
        anime_details.append(anime['coverImage']['large'])
        anime_details.append(' ')
        anime_details.append("MalID: ")
        anime_details.append(str(anime['idMal']))
        anime_details.append("Tytuł (JP): ")
        anime_details.append(str(anime['title']['romaji']))
        anime_details.append("Tytuł (EN): ")
        anime_details.append(str(anime['title']['english']))
        anime_details.append("Odcinki: ")
        anime_details.append(str(anime['episodes']))
        anime_details.append("Popularność: ")
        anime_details.append(str(anime['popularity']))
        anime_details.append("Opinie: ")
        anime_details.append(gen_rating(anime['averageScore']))
        anime_details.append("Status: ")
        anime_details.append(str(anime['status']))

        genres = ''
        for genre in anime['genres']:
            genres += genre + ", "

        anime_details.append("Gatunki: ")
        anime_details.append(genres)


        all_details.append(anime_details)


    ans = run_fzf(header=trending_logo_centered_60p(), all_details=all_details,choices=choices)
    choosed_mal_id = mal_ids[choices.index(ans)]    # MalId wybranej przez użytkownika pozycji.

    print(choosed_mal_id)


clear_terminal()
trending_menu()
