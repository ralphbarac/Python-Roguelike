import tcod 

import components.status_effects as effects

from game_messages import Message

from map_objects.trap import Trap

from render_functions import RenderOrder

import status_effect_functions as sfn
import trap_functions as tf


# FIRE SPELLS

def cast_fireball(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not tcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'spell_success': False, 'message': Message('You cannot target a tile outside your field of view.', tcod.yellow)})
        return results
    
    results.append({'spell_success': True, 'message': Message('The fireball explodes, burning everything within {0} tiles!'.format(radius), tcod.orange)})

    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.combat_entity and entity.combat_entity.hp > 0:
            new_damage = damage - entity.combat_entity.defense
            results.append({'message': Message('The {0} gets burned for {1} hit points'.format(entity.name, new_damage), tcod.orange)})
            results.extend(entity.combat_entity.take_damage(new_damage))
    
    return results

def cast_pillar_of_fire(*args, **kwargs):
    caster = args[0]
    fov_map = kwargs.get('fov_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')
    game_map = kwargs.get('game_map')
    
    results = []

    if not tcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'spell_success': False, 'message': Message('You cannot target a tile outside your field of view.', tcod.yellow)})
        return results
    
    new_trap = Trap('X', tcod.dark_crimson, caster, tf.trap_pillar_of_fire, damage=15)

    tile = game_map.tiles[target_x][target_y]

    if tile.block_sight:
        results.append({'spell_success': False, 'message': Message('You cannot cast spells in walls!', tcod.yellow)})
    else:
        tile.trap = new_trap
        results.append({'spell_success': True, 'message': Message('A pillar of fire erupts from the floor.', tcod.dark_crimson)})

    return results

# WATER SPELLS

def cast_minor_heal(*args, **kwargs):
    caster = args[0]
    heal_amount = kwargs.get('amount')

    results = []

    results.append({'message': Message('You cast minor heal on yourself', tcod.light_azure)})
    results.extend(caster.combat_entity.heal(heal_amount))

    return results

# EARTH SPELLS

def cast_stoneskin(*args, **kwargs):
    caster = args[0]
    results = []

    results.append({'message': Message('You cast stoneskin on yourself', tcod.lighter_sepia)})
    status_effect = effects.StatusEffect('Stoneskin', 10, amount=15, function=sfn.stoneskin_status_function, caster=caster)
    caster.combat_entity.add_status_effect(status_effect)

    return results

# LIGHTNING SPELLS

def cast_lightning(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')

    results = []

    target = None
    closest_distance = maximum_range + 1

    for entity in entities:
        if entity.combat_entity and entity != caster and tcod.map_is_in_fov(fov_map, entity.x, entity.y) and entity.combat_entity.hp > 0:
            distance = caster.distance_to_target(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        damage = damage - target.combat_entity.defense
        results.append({'spell_success': True, 'target': target, 'message': Message('A lightning bolt strikes the {0} with a loud thunder! The damage is {1}'.format(target.name, damage))})
        results.extend(target.combat_entity.take_damage(damage))
    else:
        results.append({'spell_success': False, 'target': None, 'message': Message('There is no enemy close enough for this spell.', tcod.red)})
    
    return results

def cast_lightning_rune(*args, **kwargs):
    caster = args[0]
    game_map = kwargs.get('game_map')


    results = []

    new_trap = Trap('Q', tcod.yellow, caster, tf.trap_lightning_rune, damage=10)

    tile = game_map.tiles[caster.x][caster.y]

    if tile.block_sight:
        # This technically shouldn't happen since the player can't be in a wall.
        results.append({'spell_success': False, 'message': Message('You cannot place a lightning rune in a wall!', tcod.yellow)})
    else:
        tile.trap = new_trap
        results.append({'spell_success': True, 'message': Message('You draw a lightning rune on the ground in front of you.', tcod.yellow)})

    return results


# AIR SPELLS

def caste_haste(*args, **kwargs):

    caster = args[0]
    results = []

    results.append({'message': Message('You cast haste on yourself', tcod.lighter_gray)})
    status_effect = effects.StatusEffect('Haste', 10, amount=None, function=sfn.haste_status_function, caster=caster)
    caster.combat_entity.add_status_effect(status_effect)

    return results

def cast_gust(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')

    results = []

    target = None
    closest_distance = maximum_range + 1

    for entity in entities:
        if entity.combat_entity and entity != caster and tcod.map_is_in_fov(fov_map, entity.x, entity.y) and entity.combat_entity.hp > 0:
            distance = caster.distance_to_target(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance
        
    if target:
        damage = damage - target.combat_entity.defense
        results.append({'spell_succes': True, 'target': target, 'message': Message('A gust of wind blows the {0} back and does {1} damage!'.format(target.name, damage))})
        results.extend(target.combat_entity.take_damage(damage))
        
        dx = abs(caster.x - target.x)
        dy = abs(caster.y - target.y)

        if dx > dy:
            target.x += dx
        else:
            target.y += dy 

    else:
        results.append({'spell_success': False, 'target': None, 'message': Message('There is no enemy close enough for this spell.', tcod.red)})
    
    return results



# NATURE SPELLS

def cast_drain(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')

    results = []

    targets = []

    for entity in entities:
        if entity.combat_entity and entity != caster and tcod.map_is_in_fov(fov_map, entity.x, entity.y) and entity.combat_entity.hp > 0:
            distance = caster.distance_to_target(entity)

            if distance <= maximum_range:
                targets.append(entity)
        
    if len(targets) == 0:
        results.append({'spell_success': False, 'target': None, 'message': Message('There are no enemies to drain.', tcod.lime)})
    else:
        for target in targets:
            new_damage = damage - target.combat_entity.defense
            results.append({'spell_success': True, 'target': target, 'message': Message('You drain {0} health from the {1}'.format(new_damage, target.name))})
            results.extend(target.combat_entity.take_damage(new_damage))
            results.extend(caster.combat_entity.heal(new_damage))
        
    return results

def cast_vines(*args, **kwargs):
    caster = args[0]
    fov_map = kwargs.get('fov_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')
    game_map = kwargs.get('game_map')
    
    results = []

    if not tcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'spell_success': False, 'message': Message('You cannot target a tile outside your field of view.', tcod.yellow)})
        return results
    
    new_trap = Trap('S', tcod.dark_green, caster, tf.trap_vines, damage=5, render_order=RenderOrder.HIGH_PRIO_TRAP)

    tile = game_map.tiles[target_x][target_y]

    if tile.block_sight:
        results.append({'spell_success': False, 'message': Message('You cannot cast spells in walls!', tcod.yellow)})
    else:
        tile.trap = new_trap
        results.append({'spell_success': True, 'message': Message('You cast vines on the floor.', tcod.dark_crimson)})

    return results

# PSYCHIC SPELLS

def cast_weaken(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    damage = kwargs.get('amount')
    maximum_range = kwargs.get('maximum_range')
    fov_map = kwargs.get('fov_map')

    results = []

    target = None
    closest_distance = maximum_range + 1

    for entity in entities:
        if entity.combat_entity and entity != caster and tcod.map_is_in_fov(fov_map, entity.x, entity.y) and entity.combat_entity.hp > 0:
            distance = caster.distance_to_target(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance
    
    if target:
        damage = damage - target.combat_entity.defense
        results.append({'spell_success': True, 'target': target, 'message': Message('You drain the {0} of part of its power!'.format(target.name), tcod.pink)})
        results.extend(target.combat_entity.update_power(damage * (-1)))
    else:
        results.append({'spell_success': False, 'target': None, 'message': Message('There is no enemy close enough for this spell.', tcod.pink)})
    
    return results