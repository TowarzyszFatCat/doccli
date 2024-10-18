from requests import get


### DOCCHI API

# Get list of players for episode
def get_players_list(SLUG, NUMBER):
    request = get(f"https://api.docchi.pl/v1/episodes/find/{SLUG}/{NUMBER}")
    if request.status_code == 200:
        return request.json()
    else:
        return request.status_code


# Get list of how much episodes series contains
def get_episodes_count_for_serie(SLUG):
    request = get(f"https://api.docchi.pl/v1/episodes/count/{SLUG}")
    if request.status_code == 200:
        return len(request.json())
    else:
        return request.status_code


# Get all hentais list
def get_hentai_list():  # XD
    request = get(f"https://api.docchi.pl/v1/series/hentai")
    if request.status_code == 200:
        return request.json()
    else:
        return request.status_code


# Get all series list
def get_series_list():
    request = get(f"https://api.docchi.pl/v1/series/list")
    if request.status_code == 200:
        return request.json()
    else:
        return request.status_code


# Get detail info about the Series
def get_details_for_serie(SLUG):
    request = get(f"https://api.docchi.pl/v1/series/find/{SLUG}")
    if request.status_code == 200:
        return request.json()
    else:
        return request.status_code


### AniSkip API
def get_skip_times(MALID, EP):
    #            OPS OPE ENS ENE
    skip_times = [-1, -1, -1, -1]

    request = get(f'https://api.aniskip.com/v2/skip-times/{MALID}/{EP}?types=op&types=ed&types=mixed-op&types=mixed-ed&types=recap&episodeLength=0')
    if request.status_code == 200:
        ans = request.json()

        if ans['found'] == True:
            for i in ans['results']:
                # Handle openings
                if i['skipType'] == 'op':
                    times = i['interval']
                    skip_times[0] = times['startTime']
                    skip_times[1] = times['endTime']
                # Handle endings
                if i['skipType'] == 'ed':
                    times = i['interval']
                    skip_times[2] = times['startTime']
                    skip_times[3] = times['endTime']

    return skip_times