import tcod

from components.spell import Spell, spells, cast_lightning

# There may be 'errors' highlighted in areas with the code "self.owner". This is OK because these elements all have owners at runtime the IDE just doesn't 
# realize it. This is what happens when you use composition instead of inheritance.

class BasicEnemy:
    def take_turn(self, target, fov_map, game_map, entities):
        results = []

        monster = self.owner        
        if tcod.map_is_in_fov(fov_map, monster.x, monster.y):

            if monster.distance_to_target(target) >= 2:
                monster.move_astar(target, entities, game_map)

            elif target.combat_entity.hp > 0:
                attack_results = monster.combat_entity.attack(target)
                results.extend(attack_results)
        
        return results

class MagicEnemy:
    def take_turn(self, target, fov_map, game_map, entities):
        results = []

        monster = self.owner
        if tcod.map_is_in_fov(fov_map, monster.x, monster.y):

            if monster.distance_to_target(target) >= 4:
                monster.move_astar(target, entities, game_map)
            
            elif target.combat_entity.hp > 0:
                if self.owner.combat_entity.mana >= 35:
                    spell = cast_lightning
                    attack_results = monster.book.cast_spell(spell, entities=entities, fov_map=fov_map, game_map=game_map)
                    results.extend(attack_results)
                else:
                    if monster.distance_to_target(target) >= 2:
                        monster.move_astar(target, entities, game_map)
                    else:
                        attack_results = monster.combat_entity.attack(target)
                        results.extend(attack_results)
        
        return results

# Can add different enemy types that do different things here. The default is above, but we can change how monsters move and react to the player. We can even add ai's that help the player potentially in the future.

