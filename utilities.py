from random import randint

def from_dungeon_depth(table, dungeon_depth):
    for(value, depth) in reversed(table):
        if dungeon_depth >= depth:
            return value
    
    return 0

def random_choice_index(chances):
    random_chance = randint(1, sum(chances))

    total = 0
    choice = 0
    for i in chances:
        total += i

        if random_chance <= total:
            return choice
        
        choice += 1

def random_choice_from_dict(choice_dict):
    choices = list(choice_dict.keys())
    chances = list(choice_dict.values())

    return choices[random_choice_index(chances)]