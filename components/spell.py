import spell_functions

import components.status_effects as effect

from game_messages import Message


import tcod

class Spell:
    def __init__(self, name, mana_cost, spell_function=None, targeting=False, targeting_message=None, **kwargs):
        self.name = name
        self.mana_cost = mana_cost
        self.spell_function = spell_function
        self.function_kwargs=kwargs
        self.targeting = targeting
        self.targeting_message = targeting_message



# WATER
cast_minor_heal = Spell('Minor Heal', 20, spell_function=spell_functions.cast_minor_heal, amount=30)

water_spells = [cast_minor_heal]

#FIRE
cast_fireball = Spell('Fireball', 20, spell_functions.cast_fireball, targeting=True, targeting_message=Message('Left click a target tile to cast the fireball, or right click to cancel.', tcod.light_red), damage=12, radius=3)

cast_pillar_of_fire = Spell('Pillar of Fire', 20, spell_function=spell_functions.cast_pillar_of_fire, targeting=True, targeting_message=Message('Left click a target tile to cast the pillar, or right click to cancel.', tcod.light_red))

fire_spells = [cast_fireball, cast_pillar_of_fire]

# EARTH
cast_stoneskin = Spell('Stoneskin', 15, spell_function=spell_functions.cast_stoneskin)

earth_spells = [cast_stoneskin]

# =================================================================== #

# LIGHTNING
cast_lightning = Spell('Lightning', 35, spell_function=spell_functions.cast_lightning, damage=20, maximum_range=5)
cast_lightning_rune = Spell('Lightning Rune', 10, spell_function=spell_functions.cast_lightning_rune)

lightning_spells = [cast_lightning, cast_lightning_rune]

# AIR
cast_haste = Spell('Haste', 10, spell_function=spell_functions.caste_haste)
cast_gust = Spell('Gust', 15, spell_function=spell_functions.cast_gust, damage=10, maximum_range=3)

air_spells = [cast_haste, cast_gust]

# NATURE
cast_drain = Spell('Drain', 60, spell_function=spell_functions.cast_drain, damage=10, maximum_range=5)
cast_vines = Spell('Vines', 30, spell_function=spell_functions.cast_vines, targeting=True, targeting_message=Message('Left click a target tile to cast vines, or right click to cancel.', tcod.darker_green), damage=5)

nature_spells = [cast_drain, cast_vines]

# =================================================================== #


# PSYCHIC

cast_weaken = Spell('Weaken', 20, spell_function=spell_functions.cast_weaken, amount=10, maximum_range=7)

psychic_spells = [cast_weaken]





spells = [water_spells, fire_spells, earth_spells, lightning_spells, air_spells, nature_spells, psychic_spells]
