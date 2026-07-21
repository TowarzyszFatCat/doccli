import time

# From pip
from deep_translator import GoogleTranslator
from requests import post

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


def update_anilist_progress(mal_id, episode_number, token):
    if not token or token == "":
        return False
        
    query_id = '''
    query ($malId: Int) {
      Media(idMal: $malId, type: ANIME) {
        id
      }
    }
    '''
    try:
        req = post("https://graphql.anilist.co", json={'query': query_id, 'variables': {'malId': mal_id}}, timeout=5)
        if req.status_code != 200:
            return False
        anilist_id = req.json()['data']['Media']['id']
    except:
        return False

    mutation = '''
    mutation ($mediaId: Int, $progress: Int) {
      SaveMediaListEntry(mediaId: $mediaId, progress: $progress) {
        id
        progress
      }
    }
    '''
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    variables = {
        'mediaId': anilist_id,
        'progress': episode_number
    }
    
    try:
        req_mut = post("https://graphql.anilist.co", json={'query': mutation, 'variables': variables}, headers=headers, timeout=5)
        return req_mut.status_code == 200
    except:
        return False
    

def get_anilist_plan_to_watch(token):
    if not token or token == "":
        return None
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    
    query_user = '''
    query {
      Viewer {
        id
      }
    }
    '''
    try:
        req1 = post("https://graphql.anilist.co", json={'query': query_user}, headers=headers, timeout=5)
        if req1.status_code != 200:
            return None
        user_id = req1.json()['data']['Viewer']['id']
    except:
        return None

    query_list = '''
    query ($userId: Int) {
      MediaListCollection(userId: $userId, type: ANIME, status: PLANNING) {
        lists {
          entries {
            media {
              idMal
            }
          }
        }
      }
    }
    '''
    try:
        req2 = post("https://graphql.anilist.co", json={'query': query_list, 'variables': {'userId': user_id}}, headers=headers, timeout=5)
        if req2.status_code != 200:
            return None
            
        mal_ids = []
        lists = req2.json()['data'].get('MediaListCollection', {}).get('lists', [])
        
        if lists:
            for entry in lists[0]['entries']:
                if entry['media']['idMal']:
                    mal_ids.append(entry['media']['idMal'])
                    
        return mal_ids
    except:
        return None


def sync_anilist_list_status(mal_id, token, status_add=True):
    if not token or token == "":
        return False

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    query_id = '''
    query ($malId: Int) {
      Media(idMal: $malId, type: ANIME) {
        id
      }
    }
    '''
    try:
        req = post("https://graphql.anilist.co", json={'query': query_id, 'variables': {'malId': mal_id}}, timeout=5)
        if req.status_code != 200: return False
        anilist_id = req.json()['data']['Media']['id']
    except:
        return False

    if status_add:
        mutation = '''
        mutation ($mediaId: Int, $status: MediaListStatus) {
          SaveMediaListEntry(mediaId: $mediaId, status: $status) {
            id
          }
        }
        '''
        try:
            post("https://graphql.anilist.co", json={'query': mutation, 'variables': {'mediaId': anilist_id, 'status': 'PLANNING'}}, headers=headers, timeout=5)
            return True
        except:
            return False
    else:
        try:
            query_user = '''
            query {
              Viewer {
                id
              }
            }
            '''
            req_user = post("https://graphql.anilist.co", json={'query': query_user}, headers=headers, timeout=5)
            if req_user.status_code != 200: return False
            user_id = req_user.json()['data']['Viewer']['id']

            query_entry = '''
            query ($mediaId: Int, $userId: Int) {
              MediaList(mediaId: $mediaId, userId: $userId) {
                id
              }
            }
            '''
            req_entry = post("https://graphql.anilist.co", json={'query': query_entry, 'variables': {'mediaId': anilist_id, 'userId': user_id}}, headers=headers, timeout=5)
            if req_entry.status_code != 200: return False
            
            entry_data = req_entry.json().get('data', {}).get('MediaList')
            if not entry_data: 
                return False # Nie ma tego na liście, więc nie ma co usuwać
                
            entry_id = entry_data['id']
            
            mutation_del = '''
            mutation ($id: Int) {
              DeleteMediaListEntry(id: $id) {
                deleted
              }
            }
            '''
            post("https://graphql.anilist.co", json={'query': mutation_del, 'variables': {'id': entry_id}}, headers=headers, timeout=5)
            return True
        except:
            return False