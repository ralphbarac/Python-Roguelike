import tcod

from enum import Enum

from game_states import GameStates

from menus import book_screen, character_screen, inventory_menu, level_up_menu, spell_menu

class RenderOrder(Enum):
    BONFIRES = 1
    CORPSE = 2
    ITEM = 3
    ACTOR = 4
    HIGH_PRIO_TRAP = 5

# This function allows the player to hover over a monster and see its name.
def hover_names(mouse, entities, fov_map):
    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name for entity in entities if entity.x == x and entity.y == y and tcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    names = ', '.join(names)

    return names.capitalize()


def render_bar(panel, x, y, total_width, name, value, maximum, bar_colour, bg_colour):
    bar_width = int(float(value) / maximum * total_width)   

    tcod.console_set_default_background(panel, bg_colour)
    tcod.console_rect(panel, x, y, total_width, 2, False, tcod.BKGND_SCREEN)

    tcod.console_set_default_background(panel, bar_colour)
    if bar_width > 0:
        tcod.console_rect(panel, x, y, bar_width, 2, False, tcod.BKGND_SCREEN)

    tcod.console_set_default_foreground(panel, tcod.white)
    tcod.console_print_ex(panel, int(x + total_width / 2), y, tcod.BKGND_NONE, tcod.CENTER,
    '{0}'.format(name))
    tcod.console_print_ex(panel, int(x + total_width / 2), y + 1, tcod.BKGND_NONE, tcod.CENTER,
    '{0}/{1}'.format(value, maximum))

def render_enemy_bar(panel, x, y, total_width, name, value, maximum, bar_colour, bg_colour):
    bar_width = int(float(value) / maximum * total_width)

    tcod.console_set_default_background(panel, bg_colour)
    tcod.console_rect(panel, x, y, total_width, 2, False, tcod.BKGND_SCREEN)

    tcod.console_set_default_background(panel, bar_colour)
    if bar_width > 0:
        tcod.console_rect(panel, x, y, bar_width, 2, False, tcod.BKGND_SCREEN)
    
    tcod.console_set_default_foreground(panel, tcod.white)
    tcod.console_print_ex(panel, int(x + total_width / 2), y, tcod.BKGND_NONE, tcod.CENTER, '{0}'.format(name))
    tcod.console_print_ex(panel, int(x + total_width / 2), y + 1, tcod.BKGND_NONE, tcod.CENTER, '{0}/{1}'.format(value, maximum))



def render_all(console, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height, bar_width, panel_height, panel_y, mouse, game_state):
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = tcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight
                trap = game_map.tiles[x][y].trap

                if visible:
                    if wall:
                        tcod.console_put_char_ex(console, x, y, '#', tcod.white, tcod.black)
                    elif trap:
                        tcod.console_put_char_ex(console, x, y, trap.char, trap.colour, tcod.gray)
                    else:
                        tcod.console_put_char_ex(console, x, y, ' ', tcod.white, tcod.gray)
                    
                    game_map.tiles[x][y].explored = True

                elif game_map.tiles[x][y].explored:
                    if wall:
                        tcod.console_put_char_ex(console, x, y, '#', tcod.gray, tcod.black)
                    else:
                        tcod.console_put_char_ex(console, x, y, ' ', tcod.lightest_gray, tcod.black)

    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    for entity in entities_in_render_order:
        draw_entity(console, entity, fov_map, game_map)

    tcod.console_blit(console, 0, 0, screen_width, screen_height, 0, 0, 0)

    tcod.console_set_default_background(panel, tcod.black)
    tcod.console_clear(panel)

    y = 1
    for message in message_log.messages:
        tcod.console_set_default_foreground(panel, message.colour)
        tcod.console_print_ex(panel, message_log.x, y, tcod.BKGND_NONE, tcod.LEFT, message.text)
        y += 1

    render_bar(panel, 1, 1, bar_width, 'HP', player.combat_entity.hp, player.combat_entity.max_hp, tcod.light_red, tcod.darker_red)
    render_bar(panel, 1, 3, bar_width, 'MANA', player.combat_entity.mana, player.combat_entity.max_mana, tcod.light_blue, tcod.darker_blue)

    tcod.console_print_ex(panel, screen_width - bar_width, 0, tcod.BKGND_NONE, tcod.LEFT, 'Visible Enemies:')

    y = 1
    for entity in entities:
        if entity.combat_entity and entity is not player and tcod.map_is_in_fov(fov_map, entity.x, entity.y) and entity.combat_entity.hp > 0:
            render_enemy_bar(panel, screen_width - bar_width, y, bar_width, '{0} '.format(entity.name), entity.combat_entity.hp, entity.combat_entity.max_hp, tcod.light_red, tcod.darker_red)
            y += 2

    tcod.console_print_ex(panel, screen_width - bar_width - 20, 0, tcod.BKGND_NONE, tcod.LEFT, 'Dungeon Depth: {0}'.format(game_map.dungeon_depth))
    tcod.console_print_ex(panel, screen_width - bar_width - 20, 1, tcod.BKGND_NONE, tcod.LEFT, 'Score: {0}'.format(player.score))

    tcod.console_set_default_foreground(panel, tcod.light_gray)
    tcod.console_print_ex(panel, 1, 0, tcod.BKGND_NONE, tcod.LEFT, hover_names(mouse, entities, fov_map))

    tcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)

    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = 'Press the key next to an item to use it. Press Esc to cancel.\n'
        else:
            inventory_title = 'Press the key next to an item to drop it. Press Esc to cancel.\n'

        inventory_menu(console, inventory_title, player, 50, screen_width, screen_height)
    
    elif game_state == GameStates.SPELL_LIST:
        spell_menu(console, 'Spell List', player, 50, screen_width, screen_height)
    
    elif game_state == GameStates.LEVEL_UP:
        level_up_menu(console, 'Level Up! Choose a stat to raise', player, 40, screen_width, screen_height)

    elif game_state == GameStates.CHARACTER_SCREEN:
        character_screen(player, 30, 10, screen_width, screen_height)
    
    elif game_state == GameStates.BOOK_SCREEN:
        book_screen(player, 30, 10, screen_width, screen_height)

def clear_all(console, entities):
    for entity in entities:
        clear_entity(console, entity)

def draw_entity(console, entity, fov_map, game_map):
    if tcod.map_is_in_fov(fov_map, entity.x, entity.y) or (entity.bonfire and game_map.tiles[entity.x][entity.y].explored):
        tcod.console_set_default_foreground(console, entity.colour)
        tcod.console_put_char(console, entity.x, entity.y, entity.char, tcod.BKGND_NONE)

def clear_entity(console, entity):
    tcod.console_put_char(console, entity.x, entity.y, ' ', tcod.BKGND_NONE)