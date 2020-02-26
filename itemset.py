import json

path = "C:\Riot Games\League of Legends\Config\Champions"


def create_itemset(champion):
    data = {}
    data['title'] = 'ARAM: {}'.format(champion.name)
    data['type'] = 'custom'
    data['map'] = 'any'
    data['mode'] = 'any'
    data['priority'] = True
    data['sortrank'] = 0
    blocks = [add_items_to_block(champion.startitems, 'Starting Items'),
              add_items_to_block(champion.items, champion.skill_order)]
    data['blocks'] = blocks
    write_item_file(data, champion.name_stripped)


def add_items_to_block(items, block_name):
    block = {}
    block['recMath'] = False
    block['minSummonerLevel'] = -1
    block['showIfSummonerSpell'] = ''
    block['hideIfSummonerSpell'] = ''
    block['type'] = block_name
    block['items'] = []
    for item in items:
        data = {}
        data['id'] = '{}'.format(item)
        data['count'] = 1
        block['items'].append(data)
    return block


def write_item_file(data, stripped_champion_name):
    filename = 'ARAM_{}.json'.format(stripped_champion_name)
    with open('{}\{}\Recommended\{}'.format(path, stripped_champion_name, filename), 'w') as outfile:
        json.dump(data, outfile)
