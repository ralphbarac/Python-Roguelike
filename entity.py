import tcod

import math

from components.item import Item

from game_messages import Message

from render_functions import RenderOrder

class Entity:
    """
    This class represents all objects in our game world. Players, enemies, items, etc.
    """

    def __init__(self, x, y, char, colour, name, blocks=False, render_order=RenderOrder.CORPSE, combat_entity=None, ai=None, item=None, inventory=None, bonfire=None, level=None, page=None, book=None, spells=[], effects=[], score=0):
        self.x = x
        self.y = y
        self.char = char
        self.colour = colour
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.combat_entity = combat_entity
        self.ai = ai
        self.item = item
        self.inventory = inventory
        self.bonfire = bonfire
        self.level = level
        self.page = page
        self.book = book
        self.spells = spells
        self.effects = effects
        self.haste_bonus = 0
        self.score = 0

        # Using composition instead of inheritance to build entities that can do different things.

        if self.combat_entity:
            self.combat_entity.owner = self
        
        if self.ai:
            self.ai.owner = self
        
        if self.item:
            self.item.owner = self
        
        if self.inventory:
            self.inventory.owner = self
        
        if self.bonfire:
            self.bonfire.owner = self
        
        if self.level:
            self.level.owner = self
        
        if self.book:
            self.book.owner = self

        if self.page:
            self.page.owner = self

            if not self.item:
                item = Item()
                self.item = item
                self.item.owner = self
        
        if self.spells:
            self.spells.owner = self
        
        if self.effects:
            self.effects.owner = self
        
    def set_name(self, name):
        self.name = name
        
    def move(self, dx, dy):
        self.x = self.x + dx 
        self.y = self.y + dy 

    def move_towards(self, target_x, target_y, game_map, entities):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (game_map.is_blocked(self.x + dx, self.y + dy) or get_blocking_entities(entities, self.x + dx, self.y + dy)):
            self.move(dx, dy)
    
    # This algorithm is a known 8-directional pathfinding algorithm for enemy units taken from: http://www.roguebasin.com and also desrcibed 
    # on WikiPedia here: https://en.wikipedia.org/wiki/A*_search_algorithm
    def move_astar(self, target, entities, game_map):
        # Create a FOV map that has the dimensions of the map
        fov = tcod.map_new(game_map.width, game_map.height)

        for effect in self.effects:
            if effect.name == 'Vines':
              return

        # Scan the current map each turn and set all the walls as unwalkable
        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                tcod.map_set_properties(fov, x1, y1, not game_map.tiles[x1][y1].block_sight,
                                           not game_map.tiles[x1][y1].blocked)

        # Scan all the objects to see if there are objects that must be navigated around
        # Check also that the object isn't self or the target (so that the start and the end points are free)
        # The AI class handles the situation if self is next to the target so it will not use this A* function anyway
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                # Set the tile as a wall so it must be navigated around
                tcod.map_set_properties(fov, entity.x, entity.y, True, False)

        # Allocate a A* path
        # The 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal moves are prohibited
        my_path = tcod.path_new_using_map(fov, 1.41)

        # Compute the path between self's coordinates and the target's coordinates
        tcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        # Check if the path exists, and in this case, also the path is shorter than 25 tiles
        # The path size matters if you want the monster to use alternative longer paths (for example through other rooms) if for example the player is in a corridor
        # It makes sense to keep path size relatively low to keep the monsters from running around the map if there's an alternative path really far away
        if not tcod.path_is_empty(my_path) and tcod.path_size(my_path) < 25:
            # Find the next coordinates in the computed full path
            x, y = tcod.path_walk(my_path, True)
            if x or y:
                # Set self's coordinates to the next path tile
                self.x = x
                self.y = y
        else:
            # Keep the old move function as a backup so that if there are no paths (for example another monster blocks a corridor)
            # it will still try to move towards the player (closer to the corridor opening)
            self.move_towards(target.x, target.y, game_map, entities)

            # Delete the path to free memory
        tcod.path_delete(my_path)
    
    def distance_to_target(self, target):
        dx = target.x - self.x
        dy = target.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)
    
    def distance(self, x, y):
        return math.sqrt((x-self.x) ** 2 + (y - self.y) ** 2)
    
    def isHasted(self):
        if self.haste_bonus > 0:
            return True

   
    
def get_blocking_entities(entities, dest_x, dest_y):
    for entity in entities:
        if entity.blocks and entity.x == dest_x and entity.y == dest_y:
            return entity
    
    return None


