import tcod

from book_slots import BookSlots

from game_messages import Message

class Book:
    def __init__(self, ele_1=None, ele_2=None, life=None, vision=None, alt=None):
        self.ele_1 = ele_1
        self.ele_2 = ele_2
        self.life = life
        self.vision = vision
        self.alt = alt
        self.spell_list = []

    @property
    def max_hp_bonus(self):
        bonus = 0

        if self.ele_1 and self.ele_1.page:
            bonus += self.ele_1.page.max_hp_bonus
        if self.ele_2 and self.ele_2.page:
            bonus += self.ele_2.page.max_hp_bonus
        if self.life and self.life.page:
            bonus += self.life.page.max_hp_bonus
        if self.vision and self.vision.page:
            bonus += self.vision.page.max_hp_bonus
        if self.alt and self.alt.page:
            bonus += self.alt.page.max_hp_bonus
        
        return bonus
    
    @property
    def max_mana_bonus(self):
        bonus = 0

        if self.ele_1 and self.ele_1.page:
            bonus += self.ele_1.page.max_mana_bonus
        if self.ele_2 and self.ele_2.page:
            bonus += self.ele_2.page.max_mana_bonus
        if self.life and self.life.page:
            bonus += self.life.page.max_mana_bonus
        if self.vision and self.vision.page:
            bonus += self.vision.page.max_mana_bonus
        if self.alt and self.alt.page:
            bonus += self.alt.page.max_mana_bonus
        
        return bonus
    
    @property 
    def power_bonus(self):
        bonus = 0

        if self.ele_1 and self.ele_1.page:
            bonus += self.ele_1.page.power_bonus
        if self.ele_2 and self.ele_2.page:
            bonus += self.ele_2.page.power_bonus
        if self.life and self.life.page:
            bonus += self.life.page.power_bonus
        if self.vision and self.vision.page:
            bonus += self.vision.page.power_bonus
        if self.alt and self.alt.page:
            bonus += self.alt.page.power_bonus
        
        return bonus

    @property
    def defense_bonus(self):
        bonus = 0
        
        if self.ele_1 and self.ele_1.page:
            bonus += self.ele_1.page.defense_bonus
        if self.ele_2 and self.ele_2.page:
            bonus += self.ele_2.page.defense_bonus
        if self.life and self.life.page:
            bonus += self.life.page.defense_bonus
        if self.vision and self.vision.page:
            bonus += self.vision.page.defense_bonus
        if self.alt and self.alt.page:
            bonus += self.alt.page.defense_bonus
        
        return bonus
    
    def get_book_spell_list(self):
        spell_list = []

        if self.ele_1 is not None:
            spell_list.extend(self.ele_1.page.spell_list)
        if self.ele_2 is not None:
            spell_list.extend(self.ele_2.page.spell_list)
        if self.life is not None:
            spell_list.extend(self.life.page.spell_list)
        if self.vision is not None:
            spell_list.extend(self.vision.page.spell_list)
        if self.alt is not None:
            spell_list.extend(self.alt.page.spell_list)
            
        self.spell_list = spell_list
        return self.spell_list
    
    def cast_spell(self, spell, **kwargs):
        results = []

        if self.owner.combat_entity.mana_cost(spell.mana_cost) is not True:
            results.append({'message': Message('You do not have enough mana to cast this spell.', tcod.light_flame)})

            return results

        if spell.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
            results.append({'targeting': spell})
        else:
            kwargs = {**spell.function_kwargs, **kwargs}
            spell_results = spell.spell_function(self.owner, **kwargs)

            results.extend(spell_results)

        return results

    
    def toggle_page(self, page_to_toggle):
        results = []

        slot =  page_to_toggle.page.slot

        if slot == BookSlots.ELEMENTAL_1:
            if self.ele_1 == page_to_toggle:
                self.ele_1 = None
                results.append({'dequipped': page_to_toggle})
            else:
                if self.ele_1:
                    results.append({'dequipped': self.ele_1})
                
                self.ele_1 = page_to_toggle
                results.append({'equipped': page_to_toggle})
        
        elif slot == BookSlots.ELEMENTAL_2:
            if self.ele_2 == page_to_toggle:
                self.ele_2 = None
                results.append({'dequipped': page_to_toggle})
            else:
                if self.ele_2:
                    results.append({'dequipped': self.ele_2})
                
                self.ele_2 = page_to_toggle
                results.append({'equipped': page_to_toggle})

        elif slot == BookSlots.LIFE:
            if self.life == page_to_toggle:
                self.life = None
                results.append({'dequipped': page_to_toggle})
            else:
                if self.life:
                    results.append({'dequipped': self.life})
                
                self.life = page_to_toggle
                results.append({'equipped': page_to_toggle})

        elif slot == BookSlots.VISION:
            if self.vision == page_to_toggle:
                self.vision = None
                results.append({'dequipped': page_to_toggle})
            else:
                if self.vision:
                    results.append({'dequipped': self.vision})
                
                self.vision = page_to_toggle
                results.append({'equipped': page_to_toggle})

        elif slot == BookSlots.ALT:
            if self.alt == page_to_toggle:
                self.alt = None
                results.append({'dequipped': page_to_toggle})
            else:
                if self.alt:
                    results.append({'dequipped': self.alt})
                
                self.alt = page_to_toggle
                results.append({'equipped': page_to_toggle})

        return results
