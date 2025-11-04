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

def get_stars_by_mal_id(mal_id):
    query = '''
    query ($malId: Int) {
      Media(idMal: $malId, type: ANIME) {
        averageScore
      }
    }
    '''

    variables = {"malId": mal_id}
    response = post(url, json={'query': query, 'variables': variables})

    if response.status_code == 200:
        data = response.json()
        media = data.get('data', {}).get('Media')

        if not media or media['averageScore'] is None:
            return "✩✩✩✩✩"

        avg = media['averageScore']
        stars = avg / 20  # 0–5
        full_stars = int(stars)
        half_star = stars - full_stars >= 0.5

        full = "\U0001F315" * full_stars
        if half_star and full_stars < 5:
            full += "\U0001F317"
        full += "\U0001F311" * (5 - len(full))
        return full
    else:
        return "\U0001F311\U0001F311\U0001F311\U0001F311\U0001F311"