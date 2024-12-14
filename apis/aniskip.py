import requests
from termcolor import colored


def check_service_availability() -> str:
    try:
        req = requests.head(f"https://api.aniskip.com/v2/skip-times/44511/1?types=op&episodeLength=0")
        if req.status_code == 200:
            return colored("ONLINE", color="green")
        else:
            return colored("OFFLINE", color="red")
    except:
        return colored("OFFLINE",color="red")

# Funkcja poniżej wymaga poprawek
def get_skip_times(malid, ep):
    #            OPS OPE ENS ENE
    skip_times = [-1, -1, -1, -1]

    req = get(f'https://api.aniskip.com/v2/skip-times/{malid}/{ep}?types=op&types=ed&types=mixed-op&types=mixed-ed&types=recap&episodeLength=0')
    ans = req.json()

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
