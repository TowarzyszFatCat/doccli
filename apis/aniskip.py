from requests import get


def check_service_availability() -> str:
    try:
        req = get(f"https://api.aniskip.com/v2/")
        if req.status_code == 200:
            return "ONLINE"
    except:
        return "OFFLINE"

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