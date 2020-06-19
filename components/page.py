class Page:
    def __init__(self, slot, spell_list=[], power_bonus=0, defense_bonus=0, max_hp_bonus=0, max_mana_bonus=0):
        self.slot = slot
        self.spell_list = spell_list
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.max_hp_bonus = max_hp_bonus
        self.max_mana_bonus = max_mana_bonus
        