import tcod 
from random import randint

from components.ai import BasicEnemy, MagicEnemy
from components.bonfires import Bonfires
from components.book import BookSlots, Book
from components.combat_entity import CombatEntity
from components.item import Item
from components.page import Page
from components.spell import Spell, spells, cast_lightning


from item_functions import heal, invade_player, restore_mana

from entity import Entity

from game_messages import Message

from map_objects.rectangle import Rect
from map_objects.tile import Tile

from render_functions import RenderOrder

from utilities import from_dungeon_depth, random_choice_from_dict

class GameMap:
    def __init__(self, width, height, dungeon_depth=1):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

        self.dungeon_depth = dungeon_depth

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def generate_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities):
        rooms = []
        num_rooms = 0

        center_final_x = None
        center_final_y = None

        for r in range(max_rooms):
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            new_room = Rect(x, y, w, h)

            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                self.generate_room(new_room)

                (new_x, new_y) = new_room.get_center()

                center_final_x = new_x
                center_final_y = new_y

                if num_rooms == 0:

                    player.x = new_x
                    player.y = new_y
                else:
                    (prev_x, prev_y) = rooms[num_rooms - 1].get_center()

                    if randint(0, 1) == 1:
                        self.generate_horizontal_tunnel(prev_x, new_x, prev_y)
                        self.generate_vertical_tunnel(prev_y, new_y, new_x)
                    else:
                        self.generate_vertical_tunnel(prev_y, new_y, prev_x)
                        self.generate_horizontal_tunnel(prev_x, new_x, new_y)
                
                self.place_entities(new_room, entities)

                rooms.append(new_room)
                num_rooms += 1
        
        bonfire_component = Bonfires(self.dungeon_depth + 1)
        bonfire = Entity(center_final_x, center_final_y, '&', tcod.light_orange, 'Bonfire', render_order=RenderOrder.BONFIRES, bonfire=bonfire_component)
        entities.append(bonfire)
        

    def generate_room(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False
    
    def generate_horizontal_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def generate_vertical_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False
    
    def place_entities(self, room, entities):
        number_of_monsters = from_dungeon_depth([[2,1], [3,4], [5,6]], self.dungeon_depth)
        number_of_items = from_dungeon_depth([[1,1], [2,2], [3,3]], self.dungeon_depth)

        monster_chances = {'rat': from_dungeon_depth([[100, 1], [85, 3], [30, 5]], self.dungeon_depth), 
                           'zombie': from_dungeon_depth([[15, 3], [30, 5], [60,7]], self.dungeon_depth),
                           'wizard': from_dungeon_depth([[40, 3]], self.dungeon_depth),
                           'demon': from_dungeon_depth([[1, 1], [30, 6]], self.dungeon_depth),
                           }

        item_chances = {'invasion_scroll': 0,
                        'health_potion': from_dungeon_depth([[60, 1]], self.dungeon_depth),
                        'mana_potion': from_dungeon_depth([[60, 1]], self.dungeon_depth),
                        'blue_page': from_dungeon_depth([[10, 1], [5, 3], [2, 5], [1, 8]], self.dungeon_depth),        
                        'red_page': from_dungeon_depth([[10, 1], [5, 3], [2, 5], [1, 8]], self.dungeon_depth),
                        'brown_page': from_dungeon_depth([[10, 1], [5, 3], [2, 5], [1, 8]], self.dungeon_depth),
                        'yellow_page': from_dungeon_depth([[5, 1], [10, 3], [5, 5], [1, 8]], self.dungeon_depth),
                        'gray_page': from_dungeon_depth([[5, 1], [10, 3], [5, 5], [1, 8]], self.dungeon_depth),
                        'green_page': from_dungeon_depth([[5, 1], [10, 3], [5, 5], [1, 8]], self.dungeon_depth),
                        'pink_page': from_dungeon_depth([[2, 1], [5, 3], [10, 5], [5, 8]], self.dungeon_depth)
        }

        for i in range(number_of_monsters):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                monster_choice = random_choice_from_dict(monster_chances)
                if monster_choice == 'rat':
                    combat_entity_component = CombatEntity(hp=10, power=3, defense=2, xp=35)
                    ai_component = BasicEnemy()
                    monster = Entity(x, y, 'r', tcod.green, 'Rat', blocks=True, render_order=RenderOrder.ACTOR, combat_entity=combat_entity_component, ai=ai_component)
                elif monster_choice =='zombie':
                    combat_entity_component = CombatEntity(hp=16, power=5, defense=1, xp=100)
                    ai_component = BasicEnemy()
                    monster = Entity(x, y, 'Z', tcod.light_chartreuse, 'Zombie', blocks=True, render_order=RenderOrder.ACTOR, combat_entity=combat_entity_component, ai=ai_component)
                elif monster_choice =='wizard':
                    combat_entity_component = CombatEntity(hp=30, power=15, mana=300, defense=5, xp=200)
                    ai_component = MagicEnemy()
                    book_component = Book()
                    monster = Entity(x, y, 'W', tcod.pink, 'Wizard', blocks=True, render_order=RenderOrder.ACTOR, combat_entity=combat_entity_component, ai=ai_component, book=book_component, spells=cast_lightning)
                elif monster_choice =='demon':
                    combat_entity_component = CombatEntity(hp=300, power=30, defense=20, xp=300)
                    ai_component = BasicEnemy()
                    monster = Entity(x, y, 'D', tcod.crimson, 'Demon', blocks=True, render_order=RenderOrder.ACTOR, combat_entity=combat_entity_component, ai=ai_component)
                
                entities.append(monster)
        
        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_choice = random_choice_from_dict(item_chances)

                if item_choice == 'invasion_scroll':
                    item_component = Item(use_function=invade_player)
                    item = Entity(x, y, '!', tcod.darkest_orange, 'Invasion Scroll', render_order=RenderOrder.ITEM, item=item_component)
                elif item_choice == 'health_potion':
                    item_component = Item(use_function=heal, amount=10)
                    item = Entity(x, y, 'P', tcod.crimson, 'Health Potion', render_order=RenderOrder.ITEM, item=item_component)
                elif item_choice == 'mana_potion':
                    item_component = Item(use_function=restore_mana, amount=20)
                    item = Entity(x, y, 'P', tcod.azure, 'Mana Potion', render_order=RenderOrder.ITEM, item=item_component)
                elif item_choice == 'blue_page':
                    page_component = Page(BookSlots.ELEMENTAL_1, spell_list=spells[0], max_hp_bonus=3)
                    item = Entity(x, y, '+', tcod.blue, 'Blue Page', page=page_component)
                elif item_choice == 'red_page':
                    page_component = Page(BookSlots.ELEMENTAL_1, spell_list=spells[1], power_bonus=3)
                    item = Entity(x, y, '+', tcod.red, 'Red Page', page=page_component)
                elif item_choice == 'brown_page':
                    page_component = Page(BookSlots.ELEMENTAL_1, spell_list=spells[2], defense_bonus=5)
                    item = Entity(x, y, '+', tcod.darker_sepia, 'Brown Page', page=page_component)
                elif item_choice == 'yellow_page':
                    page_component = Page(BookSlots.ELEMENTAL_2, spell_list=spells[3])
                    item = Entity(x, y, '+', tcod.yellow, 'Yellow Page', page=page_component)
                elif item_choice == 'gray_page':
                    page_component = Page(BookSlots.ELEMENTAL_2, spell_list=spells[4])
                    item = Entity(x, y, '+', tcod.white, 'Gray Page', page=page_component)
                elif item_choice == 'green_page':
                    page_component = Page(BookSlots.ELEMENTAL_2, spell_list=spells[5])
                    item = Entity(x, y, '+', tcod.chartreuse, 'Green Page', page=page_component)
                elif item_choice == 'pink_page':
                    page_component = Page(BookSlots.LIFE, spell_list=spells[6])
                    item = Entity(x, y, '+', tcod.pink, 'Pink Page', page=page_component)

                entities.append(item)

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        
        return False
    
    def is_line_blocked(self, x, y, modifier):
        count = 0
        while count != modifier:
            if self.tiles[x][y].blocked:
                return True
            else:
                x += 1 # the issue is its checking wrong tiles, incrementing y when only moxing x doesnt check right tile
                y += 1
                count += 1
        
        return False

    def descend(self, player, message_log, constants):
        self.dungeon_depth += 1
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.generate_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'], constants['map_width'], constants['map_height'], player, entities)

        player.combat_entity.heal(player.combat_entity.max_hp)
        message_log.add_message(Message('The bonfire restores your health, and transports you deeper into the dungeon.', tcod.light_orange))

        return entities
