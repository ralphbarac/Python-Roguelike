import tcod

from game_messages import Message

from network import Network

def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity.combat_entity.hp == entity.combat_entity.max_hp:
        results.append({'consumed': False, 'message': Message('You are already at full health', tcod.yellow)})
    else:
        entity.combat_entity.heal(amount)
        results.append({'consumed': True, 'message': Message('You drink the health potion.', tcod.yellow)})
    
    return results

def restore_mana(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity.combat_entity.mana == entity.combat_entity.max_mana:
        results.append({'consumed': False, 'message': Message('You are already at full mana', tcod.yellow)})
    else:
        entity.combat_entity.restore_mana(amount)
        results.append({'consumed': True, 'message': Message('You drink the mana potion', tcod.yellow)})
    
    return results

def invade_player(*args, **kwargs):
    results = []

    results.append({'invade': True, 'consumed': True, 'message': Message('Searching for a player to invade...', tcod.lighter_crimson)})

    return results
