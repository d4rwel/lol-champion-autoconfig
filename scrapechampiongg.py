import requests, bs4, json, re, ddragon
from champion import Champion

def get_champion(name):
    name_stripped = Champion.strip_name(name)
    res = requests.get('https://champion.gg/champion/{}'.format(name_stripped))
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'lxml')

    spells = get_spells(soup, '% Summoners')
    startitems = get_items(soup, '% Starters')
    items = get_items(soup, '% Completed Build')
    perks = get_perks(soup)
    skill_order = get_skill_order(soup)
        
    return Champion(name, spells, startitems, items, perks, skill_order)


def get_perks(soup):
    perks = []
    divs = soup.find(string=re.compile("% Runes")).parent.parent.find_all(class_=re.compile('Description__Title'))
    for div in divs:
        perks.append(ddragon.get_id(div.string))
    return perks


def get_items(soup, indicator):
    data = []
    imgs = soup.find(string=re.compile(indicator)).parent.next_sibling.next_sibling.find_all('img')
    for img in imgs:
        data.append(img['data-id'])
    return data

    
def get_spells(soup, indicator):
    data = []
    imgs = soup.find(string=re.compile(indicator)).parent.next_sibling.next_sibling.find_all('img')
    for img in imgs:
        data.append(ddragon.get_id(img['tooltip']))
    return data


def get_skill_order(soup):
    divs = soup.find(string=re.compile("% Skill Order")).parent.next_sibling
    divs = divs.next_sibling.find_all(class_="skill-selections")[1:]
    table = []
    for div in divs:
        table.append(div.find_all("div"))
    skill_order = ''
    for i in range(0,18):
        if table[0][i]['class']:
            skill_order += 'Q'
        elif table[1][i]['class']:
            skill_order += 'W'
        elif table[2][i]['class']:
            skill_order += 'E'
        else:
            skill_order += 'R'
    return skill_order 


if __name__ == '__main__':
    champ = get_champion('Soraka')
    champ = get_champion('Lulu')
    print(champ)
