from urllib3.exceptions import InsecureRequestWarning
import requests, json, ddragon, champion


def initialize():
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    lockfile = open('c:\Riot Games\League of Legends\lockfile', 'r')
    values = lockfile.readline().split(':')
    lockfile.close()
    return values[2], values[3]


def request(endpoint, method='get', payload={}):
    path = 'https://127.0.0.1:{}/{}'.format(port, endpoint)
    if method == 'get':
        r = requests.get(path, auth=('riot', auth_token), verify=False)
    elif method == 'post':
        r = requests.post(path, data=json.dumps(payload), auth=('riot', auth_token), verify=False)
    elif method == 'put':
        r = requests.put(path, data=json.dumps(payload), auth=('riot', auth_token), verify=False)
    elif method == 'delete':
        r = requests.delete(path, auth=('riot', auth_token), verify=False)
    elif method == 'patch':
        r = requests.patch(path, data=json.dumps(payload), auth=('riot', auth_token), verify=False)
    return r.json() if method == 'get' else r.text


def get_map():
    response = request('lol-lobby/v2/lobby')
    summoner_rift_ids = {1, 2, 11}
    aram_ids = {12, 14}
    map_id = response['gameConfig']['mapId']
    if map_id in summoner_rift_ids:
        return "Summoner's Rift"
    elif map_id in aram_ids:
        return 'ARAM'
    else:
        return 'Unknown'

def get_summoner():
    response = request('lol-summoner/v1/current-summoner')
    return response


def get_current_champion():
    # return the name of the champion assigned in matchmaking
    champion_id = request('lol-champ-select/v1/current-champion')
    return ddragon.get_champion_name(champion_id)


def set_perks(champion):
    delete_perks()
    data = {'current': True,
            'isDeletable': True,
            'isEditable': True,
            'name': 'ARAM: {}'.format(champion.name),
            'primaryStyleId': champion.perks[0],
            'selectedPerkIds': champion.perks[1:5] + champion.perks[6:],
            'subStyleId': champion.perks[5]
            }
    request('lol-perks/v1/pages', 'post', data)


def delete_perks():
    # deletes all(!) perk sets with the name "ARAM: <champion_name>"
    perk_sets = request('lol-perks/v1/pages')
    for perk_set in perk_sets:
        if 'ARAM' in perk_set['name']:
            request('lol-perks/v1/pages/{}'.format(perk_set['id']), method='delete')


def set_spells(champion):
    data = {'spell1Id': champion.spells[0],
            'spell2Id': champion.spells[1]}
    request('lol-champ-select/v1/session/my-selection', 'patch', data)


port, auth_token = initialize()


if __name__ == '__main__':
    print(get_map())
