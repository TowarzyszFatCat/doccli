import time
from datetime import datetime
from termcolor import colored
import os
import requests

# From pip
from deep_translator import GoogleTranslator
from requests import post
from termcolor import colored

# Doccli modules
from storage import ds

SYNC_DONE = False
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
        episodes
        nextAiringEpisode {
          episode
        }
      }
    }
    '''
    
    variables = {"malId": mal_id}
    
    stars = "\U0001F311\U0001F311\U0001F311\U0001F311\U0001F311"
    description = "Brak opisu."
    episode_count = "?" 

    try:
        response = post(url, json={'query': query, 'variables': variables}, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            media = data.get('data', {}).get('Media')

            if media:
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
                
                if media.get('description'):
                    raw_desc = media['description']
                    clean_desc = raw_desc.replace('<br>', '\n').replace('<i>', '').replace('</i>', '')
                    
                    try:
                        translated = GoogleTranslator(source='auto', target='pl').translate(clean_desc)
                        description = translated
                    except Exception:
                        description = clean_desc

                episodes_total = media.get('episodes')
                if not episodes_total:
                    next_airing = media.get('nextAiringEpisode')
                    if next_airing and next_airing.get('episode'):
                        aired = next_airing['episode'] - 1
                        episode_count = f"Trwa emisja (Wydano: {aired})"
                    else:
                        episode_count = "Trwa emisja"
                else:
                    episode_count = episodes_total

    except Exception:
        pass

    return stars, description, episode_count


def update_anilist_progress(mal_id, episode_number, token, is_completed=False):
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
        mediaListEntry {
          progress
        }
      }
    }
    '''
    try:
        req = post("https://graphql.anilist.co", json={'query': query_id, 'variables': {'malId': mal_id}}, headers=headers, timeout=5)
        if req.status_code != 200:
            return False
            
        media_data = req.json()['data']['Media']
        anilist_id = media_data['id']
        
        current_progress = 0
        if media_data.get('mediaListEntry'):
            current_progress = media_data['mediaListEntry'].get('progress', 0)
            
        # Zabezpieczenie przed cofaniem postępu
        if episode_number <= current_progress:
            return True
            
    except:
        return False

    mutation = '''
    mutation ($mediaId: Int, $progress: Int, $status: MediaListStatus) {
      SaveMediaListEntry(mediaId: $mediaId, progress: $progress, status: $status) {
        id
        progress
        status
      }
    }
    '''

    variables = {
        'mediaId': anilist_id,
        'progress': episode_number
    }
    
    # Jeśli to ostatni odcinek status na COMPLETED jak nie to na CURRENT
    if is_completed:
        variables['status'] = 'COMPLETED'
    else:
        variables['status'] = 'CURRENT'
    
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
      MediaListCollection(userId: $userId, type: ANIME, status_in: [PLANNING, CURRENT]) {
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
            for lst in lists:
                for entry in lst['entries']:
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

def get_anilist_history(token):
    if not token or token == "":
        return []

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
            return []
        user_id = req1.json()['data']['Viewer']['id']
    except:
        return []

    query_activity = '''
    query ($userId: Int) {
      Page(page: 1, perPage: 100) {
        activities(userId: $userId, type: ANIME_LIST, sort: ID_DESC) {
          ... on ListActivity {
            progress
            createdAt
            status
            media {
              title {
                romaji
                english
              }
            }
          }
        }
      }
    }
    '''
    try:
        req2 = post("https://graphql.anilist.co", json={'query': query_activity, 'variables': {'userId': user_id}}, headers=headers, timeout=5)
        if req2.status_code != 200:
            return []
            
        activities = req2.json()['data'].get('Page', {}).get('activities', [])
        history_list = []
        
        for act in activities:
            status = act.get('status')
            progress = act.get('progress')
            
            if status not in ['watched episode', 'completed']:
                continue
                
            created_at = act.get('createdAt')
            title_romaji = act.get('media', {}).get('title', {}).get('romaji', 'Nieznany')
            title_eng = act.get('media', {}).get('title', {}).get('english', 'Nieznany')
            
            if not title_eng:
                title_eng = title_romaji
                
            history_list.append({
                'timestamp': created_at,
                'title': title_romaji,
                'title_en': title_eng,
                'progress': progress,
                'status': status
            })
            
        return history_list
    except:
        return []

def get_anilist_global_stats(token):
    if not token or token == "":
        return 0, 0
        
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    
    query_stats = '''
    query {
      Viewer {
        statistics {
          anime {
            episodesWatched
            minutesWatched
          }
        }
      }
    }
    '''
    try:
        req = post("https://graphql.anilist.co", json={'query': query_stats}, headers=headers, timeout=5)
        if req.status_code == 200:
            data = req.json()['data']['Viewer']['statistics']['anime']
            return data['episodesWatched'], data['minutesWatched']
    except:
        pass
    return 0, 0


def get_duration_by_malid(mal_id):
    if not mal_id: return 21
    query = '''query ($malId: Int) { Media(idMal: $malId, type: ANIME) { duration } }'''
    try:
        req = post("https://graphql.anilist.co", json={'query': query, 'variables': {'malId': int(mal_id)}}, timeout=5)
        if req.status_code == 200:
            dur = req.json()['data']['Media']['duration']
            return dur if dur else 21
    except:
        pass
    return 21

def get_anilist_advanced_stats(token):
    if not token or token == "":
        return None
        
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    
    query_stats = '''
    query {
      Viewer {
        id
        statistics {
          anime {
            meanScore
            statuses { count status }
            genres(limit: 3) { genre }
          }
        }
      }
    }
    '''
    
    try:
        req = post("https://graphql.anilist.co", json={'query': query_stats}, headers=headers, timeout=5)
        if req.status_code != 200:
            return None
            
        data = req.json()['data']['Viewer']
        user_id = data['id']
        anime_stats = data['statistics']['anime']
        
        mean_score = anime_stats.get('meanScore', 0)
        genres = [g['genre'] for g in anime_stats.get('genres', [])]
        
        completed = 0
        not_completed = 0
        planning_count = 0
        
        for s in anime_stats.get('statuses', []):
            if s['status'] == 'COMPLETED':
                completed += s['count']
            elif s['status'] in ['CURRENT', 'PAUSED', 'DROPPED']:
                not_completed += s['count']
            elif s['status'] == 'PLANNING':
                planning_count += s['count']
                
        query_plan = '''
        query($userId: Int) {
          MediaListCollection(userId: $userId, type: ANIME, status: PLANNING, sort: ADDED_TIME) {
            lists {
              entries {
                media { title { romaji english } }
              }
            }
          }
        }
        '''
        req_plan = post("https://graphql.anilist.co", json={'query': query_plan, 'variables': {'userId': user_id}}, headers=headers, timeout=5)
        
        oldest_title = "Brak"
        
        if req_plan.status_code == 200:
            lists = req_plan.json()['data'].get('MediaListCollection', {}).get('lists', [])
            if lists and len(lists) > 0:
                entries = lists[0].get('entries', [])
                if len(entries) > 0:
                    t = entries[0]['media']['title']
                    oldest_title = t.get('romaji') or t.get('english') or "Nieznany"
                    
        return {
            'completed': completed,
            'not_completed': not_completed,
            'mean_score': mean_score,
            'genres': ", ".join(genres) if genres else "Brak",
            'planning_count': planning_count,
            'oldest_planning': oldest_title
        }
    except:
        return None


def sync_history_with_anilist():
    global SYNC_DONE
    if SYNC_DONE:
        return
    SYNC_DONE = True
    
    from cache import get_cached_series_list # Import wewnątrz, aby uniknąć pętli
    all_series = get_cached_series_list()
    
    migrated_history = []
    for item in ds.history:
        if isinstance(item, str):
            try:
                date_str = item[1:17]
                dt_object = datetime.strptime(date_str, "%d/%m/%Y %H:%M")
                source = "Doccli - Offline" if "| Offline" in item else "Doccli - Online"
                ep_str, title, slug = "?", item, None
                
                if "[Odc: " in item:
                    ep_str = item.split("[Odc: ")[1].split("]")[0].strip()
                    title = item.split("] ", 1)[1].split(" [Odc:")[0].split(" / ")[0].strip()
                elif " | Offline [" in item:
                    ep_str = item.split(" | Offline [")[1].split("]")[0].strip()
                    title = item.split("] ", 1)[1].split(" | Offline")[0].strip()
                    
                for s in all_series:
                    if s['title'] == title or s['title_en'] == title:
                        slug = s['slug']
                        break
                        
                migrated_history.append({
                    "timestamp": dt_object.timestamp(), 
                    "dt_string": date_str, 
                    "title": title, 
                    "title_en": title, 
                    "episode": ep_str, 
                    "source": source, 
                    "slug": slug,
                    "duration": 21
                })
            except: pass
        elif isinstance(item, dict):
            if "duration" not in item:
                item["duration"] = 21
            migrated_history.append(item)
            
    ds.history = migrated_history
    ds.save()

    has_token = ds.settings.get("anilist_token") != ""
    if not has_token:
        return
        
    print(colored("[INFO] Trwa synchronizacja historii z AniList (To zajmie tylko chwilę)...", "cyan"))
    token = ds.settings["anilist_token"]
    
    try:
        al_history = get_anilist_history(token)
        for al_item in al_history:
            is_duplicate = False
            al_progress = str(al_item['progress']) if al_item['progress'] else ("Ukończono" if al_item['status'] == 'completed' else "?")
            
            for local_item in ds.history:
                if local_item.get('episode') == al_progress:
                    lt_lower = local_item.get('title', '').lower()
                    le_lower = local_item.get('title_en', '').lower()
                    at_lower = al_item['title'].lower() if al_item['title'] else ""
                    ae_lower = al_item['title_en'].lower() if al_item['title_en'] else ""
                    
                    if (at_lower and at_lower in lt_lower) or (ae_lower and ae_lower in le_lower) or (lt_lower and lt_lower in at_lower):
                        is_duplicate = True
                        break
                        
            if not is_duplicate:
                slug = None
                for s in all_series:
                    if s['title'].lower() == (al_item['title'] or "").lower() or (al_item['title_en'] and s['title_en'].lower() == al_item['title_en'].lower()):
                        slug = s['slug']
                        break
                dt_object = datetime.fromtimestamp(al_item['timestamp'])
                ds.history.append({
                    "timestamp": al_item['timestamp'], 
                    "dt_string": dt_object.strftime("%d/%m/%Y %H:%M"), 
                    "title": al_item['title'], 
                    "title_en": al_item['title_en'], 
                    "episode": al_progress, 
                    "source": "AniList", 
                    "slug": slug,
                    "duration": 21
                })
    except: pass

    ds.history.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
    ds.save()


def generate_aniskip_chapters(mal_id, ep_number, filepath):
    """
    Pobiera czasy pomijania z AniSkip i generuje plik FFMETADATA, który MPV natywnie rozumie.
    """
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
        except Exception:
            pass
            
    if not mal_id or not ep_number:
        print(colored("[-] AniSkip: Brak MAL ID lub numeru odcinka. Markery wyłączone.", "dark_grey"))
        return
        
    try:
        url = f"https://api.aniskip.com/v2/skip-times/{mal_id}/{ep_number}?types=op&types=ed&types=mixed-op&types=mixed-ed&types=recap&episodeLength=0"
        req = requests.get(url, timeout=3)
        
        if req.status_code == 200:
            data = req.json()
            if data.get("found"):
                results = data.get("results", [])
                results.sort(key=lambda x: x['interval']['startTime'])
                
                content = ";FFMETADATA1\n"
                current_time = 0.0
                
                for res in results:
                    start_time = float(res['interval']['startTime'])
                    end_time = float(res['interval']['endTime'])
                    skip_type = res['skipType']
                    
                    if start_time > current_time:
                        content += "\n[CHAPTER]\nTIMEBASE=1/1000\n"
                        content += f"START={int(current_time * 1000)}\n"
                        content += f"END={int(start_time * 1000)}\n"
                        content += "title=Odcinek\n"
                        
                    title = "Opening" if "op" in skip_type else "Ending" if "ed" in skip_type else skip_type.capitalize()
                    content += "\n[CHAPTER]\nTIMEBASE=1/1000\n"
                    content += f"START={int(start_time * 1000)}\n"
                    content += f"END={int(end_time * 1000)}\n"
                    content += f"title={title}\n"
                    
                    current_time = end_time
                    
                content += "\n[CHAPTER]\nTIMEBASE=1/1000\n"
                content += f"START={int(current_time * 1000)}\n"
                content += "END=99999999\n"
                content += "title=Odcinek\n"
                
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                
                print(colored(f"[+] Znaleziono markery AniSkip! Wygenerowano {len(results)} przedziałów.", "green"))
            else:
                print(colored("[-] Baza AniSkip nie posiada jeszcze markerów dla tego odcinka.", "yellow"))
        else:
            print(colored(f"[-] Odrzucenie z serwera AniSkip (Błąd {req.status_code})", "red"))
            
    except Exception as e:
        print(colored(f"[BŁĄD] AniSkip awaria pobierania: {e}", "red"))