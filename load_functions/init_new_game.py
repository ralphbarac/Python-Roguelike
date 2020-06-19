import tcod

from components.book import Book
from components.combat_entity import CombatEntity
from components.inventory import Inventory
from components.level import Level

from entity import Entity

from game_messages import MessageLog
from game_states import GameStates

from map_objects.game_map import GameMap

from render_functions import RenderOrder 

def get_constants():
    window_title = 'CS 4483 Prototype'

    # Entire game screen values
    screen_width = 150
    screen_height = 100

    # Values for map
    map_width = int(screen_width * 0.8)
    map_height = int(screen_height * 0.8)

    # Values for status bars. Panel values are used for the bottom portion of the screen under the map
    bar_width = 20
    panel_height = int((screen_height - map_height) / 2)
    panel_y = screen_height - panel_height

    # Values for message console
    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1
    
    # Values for room parameters
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    max_monsters_per_room = 2
    max_items_per_room = 2

    # Field of View Range
    fov_radius = 10

    constants = {
        'window_title': window_title,
        'screen_width': screen_width,
        'screen_height': screen_height,
        'map_width': map_width,
        'map_height': map_height,
        'bar_width': bar_width,
        'panel_height': panel_height,
        'panel_y': panel_y,
        'message_x': message_x,
        'message_width': message_width,
        'message_height': message_height,
        'room_max_size': room_max_size,
        'room_min_size': room_min_size,
        'max_rooms': max_rooms,
        'max_monsters_per_room': max_monsters_per_room,
        'max_items_per_room': max_items_per_room,
        'fov_radius': fov_radius
    }

    return constants

def get_game_variables(constants):
    combat_entity_component = CombatEntity(hp=100, mana=100, power=5, defense=2)
    inventory_component = Inventory(26) # Capacity of 26 because that's the length of the alphabet and streamlines controls
    level_component = Level()
    book_component = Book()
    player = Entity(0, 0, '@', tcod.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR, combat_entity=combat_entity_component, inventory=inventory_component, level=level_component, book=book_component)
    entities = [player]

    game_map = GameMap(constants['map_width'], constants['map_height'])
    game_map.generate_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'], constants['map_width'], constants['map_height'], player, entities)

    message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

    game_state = GameStates.PLAYERS_TURN

    return player, entities, game_map, message_log, game_state