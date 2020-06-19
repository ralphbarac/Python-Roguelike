import tcod

class Trap:
    def __init__(self, char, colour, caster, function, **kwargs):
        self.char = char
        self.colour = colour
        self.caster = caster
        self.function = function
        self.function_kwargs = kwargs


