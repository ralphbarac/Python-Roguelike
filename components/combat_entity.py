import tcod

import components.status_effects

from game_messages import Message



# There may be 'errors' highlighted in areas with the code "self.owner". This is OK because these elements all have owners at runtime the IDE just doesn't 
# realize it. This is what happens when you use composition instead of inheritance.

class CombatEntity:
    def __init__(self, hp, power, defense, mana=0, xp=0, effects=[]):
        self.base_max_hp = hp
        self.hp = hp
        self.base_max_mana = mana
        self.mana = mana
        self.base_power = power
        self.base_defense = defense
        self.xp = xp

    def add_status_effect(self, effect):
        self.owner.effects.append(effect)

    def apply_status_effects(self):
        results = []
        for effect in self.owner.effects:
            if effect.owner == self.owner:
                if effect.turns_left == 0:
                    self.owner.effects.remove(effect)
                else:
                    results.extend(effect.function(effect.total_turns, effect.turns_left, effect.amount, effect.owner))
                    effect.turns_left -= 1
            
        return results

    @property
    def max_hp(self):
        if self.owner and self.owner.book:
            bonus = self.owner.book.max_hp_bonus
        else:
            bonus = 0
        
        return self.base_max_hp + bonus
    
    @property 
    def max_mana(self):
        if self.owner and self.owner.book:
            bonus = self.owner.book.max_mana_bonus
        else:
            bonus = 0
        
        return self.base_max_mana + bonus
    
    @property
    def power(self):
        if self.owner and self.owner.book:
            bonus = self.owner.book.power_bonus
        else:
            bonus = 0
        
        return self.base_power + bonus
    
    @property
    def defense(self):
        if self.owner and self.owner.book:
            bonus = self.owner.book.defense_bonus
        else:
            bonus = 0
        
        return self.base_defense + bonus
    
    
    def take_damage(self, amount):
        results = []
        
        self.hp -= amount
    
        if self.hp <= 0:
            results.append({'dead': self.owner, 'xp': self.xp})
        
        return results
    
    def update_defense(self, amount):
        results = []
        self.base_defense = self.base_defense + amount

        if amount > 0:
            results.append({'message': Message('{0} defense increases by {1}!'.format(self.owner.name, amount), tcod.lighter_violet)})
        else:
            results.append({'message': Message('{0} defense decreases by {1}!'.format(self.owner.name, amount*(-1)), tcod.lighter_violet)})
        
        return results
    
    def update_power(self, amount):
        results = []
        self.base_power = self.base_power + amount

        if amount > 0:
            results.append({'message': Message('{0} power increases by {1}!'.format(self.owner.name, amount), tcod.lighter_violet)})
        else:
            results.append({'message': Message('{0} power decreases by {1}!'.format(self.owner.name, amount*(-1)), tcod.lighter_violet)})
        
        return results
    
    def heal(self, amount):
        results = []
        heal_amount = amount

        self.hp += amount
        if self.hp > self.max_hp:
            difference = self.hp - self.max_hp
            self.hp = self.max_hp
            heal_amount = amount - difference
        
        results.append({'message': Message('{0} heals for {1} hitpoints.'.format(self.owner.name, heal_amount), tcod.green)})

        return results
    
    def restore_mana(self, amount):
        results = []
        restore_amount = amount

        self.mana += amount
        if self.mana > self.max_mana:
            difference = self.mana - self.max_mana
            self.mana = self.max_mana
            restore_amount = amount - difference
        
        results.append({'message': Message('{0} restores {1} mana.'.format(self.owner.name, restore_amount), tcod.green)})

        return results
    
    def mana_cost(self, amount):
        if self.mana - amount < 0:
            return False
        else:
            self.mana = self.mana - amount
            return True

    def attack(self, target):
        results = []

        damage = self.power - target.combat_entity.defense

        if damage > 0:
            results.append({'message': Message('{0} attacks {1} for {2} hitpoints.'.format(self.owner.name.capitalize(), target.name, str(damage)), tcod.white)})
            # The extend function keeps our results list flat. Instead of [{'message': 'example'}, [{'message': 'example}]]
            # we get [{'message': 'example}, {'message': 'example}] which is easier to loop through.
            results.extend(target.combat_entity.take_damage(damage))
        else:
            results.append({'message': Message('{0} attacks {1} but does no damage.'.format(self.owner.name.capitalize(), target.name), tcod.white)})

        return results  
