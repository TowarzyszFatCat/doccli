import requests

# Można tu potem dodać config żeby wyświetlało się tyle wyników ile chce użytkownik. 
def get_trending_anime():

    url = "https://graphql.anilist.co"

    query = """
    query ($page: Int, $perPage: Int) {
      Page(page: $page, perPage: $perPage) {
        media(sort: TRENDING_DESC, type: ANIME) {
          idMal
          title {
            romaji
            english
          }
          coverImage {
            large
          }
          genres
          averageScore
          popularity
        }
      }
    }
    """

    variables = {
        "page": 1,
        "perPage": 25
    }

    response = requests.post(url, json={"query": query, "variables": variables})

    if response.status_code == 200:
        data = response.json()
        trending_anime = data['data']['Page']['media']
        return trending_anime
    else:
        return "err"
