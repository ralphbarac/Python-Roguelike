import tcod

from game_messages import Message

from components.status_effects import StatusEffect

import status_effect_functions as sfn

from map_objects import tile

def trap_lightning_rune(*args, **kwargs):
    amount = args[0].get('damage')
    entity = args[1]

    results = []
    results.append({'message': Message('{0} steps on the lightning rune! It explodes and deals {1} damage!'.format(entity.name, amount), tcod.yellow)})
    results.extend(entity.combat_entity.take_damage(amount))

    return results

def trap_pillar_of_fire(*args, **kwargs):
    amount = args[0].get('damage')
    entity = args[1]

    results = []
    results.append({'message': Message('{0} walks into the pillar of fire. It deals {1} damage!'.format(entity.name, amount), tcod.dark_crimson)})
    results.extend(entity.combat_entity.take_damage(amount))
    return results

def trap_vines(*args, **kwargs):
    amount = args[0].get('damage')
    entity = args[1]

    results = []

    status_effect = StatusEffect('Vines', 10, amount=amount, function=sfn.vines_status_function, caster=entity)
    entity.combat_entity.add_status_effect(status_effect)

    return results