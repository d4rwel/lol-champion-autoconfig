import re

class Champion:
    def __init__(self, name, spells, startitems, items, perks, skill_order):
        self.name = name
        self.name_stripped = self.strip_name(name)
        self.spells = spells
        self.place_flash_on_key_f()
        self.items = items
        self.startitems = startitems
        self.perks = perks
        self.skill_order = skill_order

    # Strips apostrophes, dots and whitespaces off of the name
    @staticmethod
    def strip_name(name):
        return re.sub("[\s\.']", '', name)

    # Place Flash spell on key F
    def place_flash_on_key_f(self):
        if self.spells[0] == 4:
            self.spells = list(reversed(self.spells))

    def __str__(self):
        return 'Name:{}\nSpells:{}\nItems:{}\nStartitems:{}\nSkillorder:{},\nPerks:{}'.format(self.name, \
                self.spells, self.items, self.startitems, self.skill_order, self.perks)

