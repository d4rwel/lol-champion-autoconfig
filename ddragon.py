import json, requests, re
from pathlib import Path

filename = 'ddragon.json'
url = 'http://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/'


def open_ddragon():
    if not Path(filename).is_file():
        return create_ddragon()
    else:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
        if not is_latest_version(data):
            data = create_ddragon()
        return data


def create_ddragon():
    data = {}
    data['version'] = get_latest_version()
    data['champions'] = get_data('champion-summary')
    data['perks'] = get_data('perks')
    data['items'] = get_data('items')
    data['spells'] = get_data('summoner-spells')
    data['perks'].update(get_perkstyles())
    with open(filename, 'w') as json_file:
        json.dump(data, json_file)
    return data


def get_perkstyles():
    data = {}
    r = requests.get('{}perkstyles.json'.format(url))
    r_json = r.json()
    for style in r_json['styles']:
        data[style['name']] = style['id']
    return data


def get_data(file_name):
    data = {}
    r = requests.get('{}{}.json'.format(url, file_name))
    r_json = r.json()
    for date in r_json:
        data[date['name']] = date['id']
    return data


def get_latest_version():
    r = requests.get('https://ddragon.leagueoflegends.com/api/versions.json')
    version = re.findall("(?<=\[\")(.*?)(?=\"\,)", r.text)[0]
    return version


def is_latest_version(json_data):
    latest_version = get_latest_version()
    return latest_version == json_data['version']


def get_champion_id(name):
    return data['champions'].get(name)


def get_perk_id(name):
    return data['perks'].get(name)


def get_spell_id(name):
    return data['spells'].get(name)


def get_item_id(name):
    return data['items'].get(name)


def get_id(name):
    if get_champion_id(name):
        return get_champion_id(name)
    elif get_perk_id(name):
        return get_perk_id(name)
    elif get_spell_id(name):
        return get_spell_id(name)
    elif get_item_id(name):
        return get_item_id(name)
    else:
        return None


def get_champion_name(champion_id):
    key_list = list(data['champions'].keys())
    value_list = list(data['champions'].values())
    name = key_list[value_list.index(champion_id)]
    return name


data = open_ddragon()  # json data


if __name__ == "__main__":
    print(get_id('Summon Aery'))
    pass
