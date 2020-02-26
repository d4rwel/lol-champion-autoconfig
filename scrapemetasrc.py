import requests, bs4, json, re, ddragon
from champion import Champion


def get_champion(name):
    name_stripped = Champion.strip_name(name)
    res = requests.get('https://www.metasrc.com/euw/aram/champion/{}'.format(name_stripped))
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'lxml')

    spells = get_items(soup, 'Best Spells')
    startitems = get_items(soup, 'Best Starting Items')
    items = get_items(soup, 'Best Item Build Order')
    perks = get_perks(soup)
    skill_order = get_skill_order(soup)
        
    return Champion(name, spells, startitems, items, perks, skill_order)


def get_perks(soup):
    perks = []
    perk_images = soup.find_all('image')
    for idx, perk_image in enumerate(perk_images):
        perk_name = perk_image.parent.parent['title']
        perk_name = re.search('>(.*)</div><', perk_name).group(1).split('>',1)[1]
        perks.append(ddragon.get_perk_id(perk_name))
    return perks


def get_items(soup, div_name):
    data = []
    imgs = soup.find_all('div', string=div_name)[0].next_sibling.find_all('img')
    for img in imgs:
        data.append(ddragon.get_id(img['alt']))
    return data


def get_skill_order(soup):
    skills = soup.find_all('div', string='Best Skill Order')[0].next_sibling.find_all('td')
    skill_order = ''
    for i in range(1,19):
        skill_order += skills[i].string if skills[i].string is not None else ''
        skill_order += skills[i + 19].string if skills[i + 19].string is not None else ''
        skill_order += skills[i + 38].string if skills[i + 38].string is not None else ''
    return skill_order 


if __name__ == '__main__':
    champ = get_champion('leona')
    print(champ)
