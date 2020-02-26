import ddragon, lcu, itemset, scrapechampiongg, scrapemetasrc

champion_name = lcu.get_current_champion()
print('Current champion: {}'.format(champion_name))

champion = None
if (lcu.get_map() == 'ARAM'):
    champion = scrapemetasrc.get_champion(champion_name)
else:
    champion = scrapechampiongg.get_champion(champion_name)

print(champion)
lcu.set_perks(champion)
print('Perks set ...')
lcu.set_spells(champion)
print('Spells set ...')
itemset.create_itemset(champion)
print('Itemset created ...')
exit()
