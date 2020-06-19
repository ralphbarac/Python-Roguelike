import tcod 

from game_messages import Message

def stoneskin_status_function(*args, **kwargs):
    total_turns = args[0]
    turns_left = args[1]
    amount = args[2]
    caster = args[3]
    
    results = []

    if turns_left == total_turns:
        results.append({'message': Message('Your stoneskin status grants you {0} bonus defense.'.format(amount), tcod.lighter_sepia)})
        caster.combat_entity.update_defense(amount)
    elif turns_left == 1:
        caster.combat_entity.update_defense(amount * -1)
        results.append({'message': Message('Your stoneskin status has worn off!', tcod.lighter_sepia)})

    return results

def haste_status_function(*args, **kwargs):
    total_turns = args[0]
    turns_left = args[1]
    caster = args[3]

    results = []

    if turns_left == total_turns:
        results.append({'message': Message('Your haste spell grants you extra movement each turn.', tcod.lighter_gray)})
        caster.haste_bonus = 1
    elif turns_left == 1:
        caster.haste_bonus = 0
        results.append({'message': Message('Your haste status has worn off!', tcod.lighter_gray)})
    
    return results

def vines_status_function(*args, **kwargs):
    total_turns = args[0]
    turns_left = args[1]
    amount = args[2]
    entity = args[3]

    results = []

    if turns_left == total_turns:
        results.append({'message': Message('The vines restrict the movement of the {0}'.format(entity.name), tcod.darker_green)})
        results.extend(entity.combat_entity.take_damage(amount))
    elif turns_left == 1:
        results.append({'message': Message('The vines on the {0} dissapear!'.format(entity.name), tcod.darker_green)})

    return results  