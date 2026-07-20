from requests import post
import time
from deep_translator import GoogleTranslator

url = "https://graphql.anilist.co"

def get_trending_anime_malids():
    query = '''
    query {
      Page(page: 1, perPage: 100) {
        media(sort: TRENDING_DESC, type: ANIME) {
          idMal
        }
      }
    }
    '''

    request = post(url, json={'query': query})

    if request.status_code == 200:
        ans = request.json()
        ids = []

        for elm in ans['data']['Page']['media']:
            ids.append(elm['idMal'])

        return ids
    else:
        return request.status_code


def get_details_from_anilist(mal_id):
    query = '''
    query ($malId: Int) {
      Media(idMal: $malId, type: ANIME) {
        averageScore
        description(asHtml: false)
      }
    }
    '''
    
    variables = {"malId": mal_id}
    
    # Domyślne wartości
    stars = "\U0001F311\U0001F311\U0001F311\U0001F311\U0001F311"
    description = "Brak opisu."

    try:
        response = post(url, json={'query': query, 'variables': variables}, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            media = data.get('data', {}).get('Media')

            if media:
                # Obsługa gwiazdek
                if media.get('averageScore'):
                    avg = media['averageScore']
                    stars_val = avg / 20 
                    full_stars = int(stars_val)
                    half_star = stars_val - full_stars >= 0.5
                    full = "\U0001F315" * full_stars
                    if half_star and full_stars < 5:
                        full += "\U0001F317"
                    full += "\U0001F311" * (5 - len(full))
                    stars = full
                
                # Obsługa opisu i tłumaczenie na polski
                if media.get('description'):
                    raw_desc = media['description']
                    # Szybkie przeczyszczenie z ewentualnych dziwnych tagów HTML, które lubi dawać AniList
                    clean_desc = raw_desc.replace('<br>', '\n').replace('<i>', '').replace('</i>', '')
                    
                    try:
                        translated = GoogleTranslator(source='auto', target='pl').translate(clean_desc)
                        description = translated
                    except Exception:
                        description = clean_desc

    except Exception:
        pass

    return stars, description