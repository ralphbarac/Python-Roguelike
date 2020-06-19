from game_messages import Message

import status_effect_functions as sfn

import tcod

class StatusEffect:
    def __init__(self, name, total_turns, function, amount=None, **kwargs):
        self.name = name
        self.amount = amount
        self.total_turns = total_turns
        self.turns_left = total_turns
        self.owner = kwargs.get('caster')
        self.function=function
        self.function_kwargs=kwargs

