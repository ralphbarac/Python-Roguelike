import tcod

from game_states import GameStates

def handle_generic_input(key, game_state):
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_input(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_input(key)
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_input(key)
    elif game_state == GameStates.LEVEL_UP:
        return handle_level_up_menu_input(key)
    elif game_state == GameStates.CHARACTER_SCREEN:
        return handle_character_screen_input(key)
    elif game_state == GameStates.BOOK_SCREEN:
        return handle_book_screen_input(key)
    elif game_state == GameStates.SPELL_LIST:
        return handle_spell_list_input(key)
    elif game_state == GameStates.TARGETING:
        return handle_targeting_input(key)

    return {}

def handle_player_turn_input(key):

    # Get the character that was pressed
    key_char = chr(key.c)
    
    # Movement (we allow for arrowpad usage, WASD standard, and QEZX for diagonal movements)
    if key.vk == tcod.KEY_UP or key_char == 'w':
        return {'move': (0, -1)}
    elif key.vk == tcod.KEY_DOWN or key_char == 's':
        return {'move': (0, 1)}
    elif key.vk == tcod.KEY_LEFT or key_char == 'a':
        return {'move': (-1, 0)}
    elif key.vk == tcod.KEY_RIGHT or key_char == 'd':
        return {'move': (1, 0)}
    elif key_char == 'q':
        return {'move': (-1, -1)}
    elif key_char == 'e':
        return {'move': (1, -1)}
    elif key_char == 'z':
        return {'move': (-1, 1)}
    elif key_char == 'x':
        return {'move': (1, 1)}
    elif key_char == 'h':
        return {'wait': True}

    # Picking up items in the world
    if key_char == 'g':
        return {'pickup': True}
    # Showing the player their inventory
    elif key_char == 'i':
        return {'show_inventory': True}
    elif key_char == 'k':
        return {'drop_inventory': True}
    elif key.vk == tcod.KEY_ENTER:
        return {'use_bonfire': True}
    elif key_char == 'c':
        return {'show_character_screen': True}
    elif key_char == 'b':
        return {'show_book_screen': True}
    elif key_char == 'm':
        return {'show_spell_list': True}

    # Exiting the game
    if key.vk == tcod.KEY_ESCAPE:
        return {'exit': True}
    
    # If no key was pressed
    return {}

def handle_inventory_input(key):
    # Converts the key pressed into an index (a = 0, b = 1, etc)
    index = key.c - ord('a')

    # If the key press was a valid inventory index we return that index
    if index >= 0:
        return {'inventory_index': index}
    
    # Exiting the game
    if key.vk == tcod.KEY_ESCAPE:
        return {'exit': True}
    
    return {}

def handle_main_menu_input(key):
    # Get the character that was pressed
    key_char = chr(key.c)

    if key_char == 'a':
        return {'new_game': True}
    elif key_char == 'b':
        return {'load_game': True}
    elif key_char == 'c' or key.vk == tcod.KEY_ESCAPE:
        return {'exit': True}
    
    return {}

def handle_level_up_menu_input(key):
    if key:
        key_char = chr(key.c)

        if key_char == 'a':
            return {'level_up': 'hp'}
        elif key_char == 'b':
            return {'level_up': 'mp'}
        elif key_char == 'c':
            return {'level_up': 'pow'}
        elif key_char =='d':
            return {'level_up': 'def'}
    
    return {}

def handle_character_screen_input(key):
    if key.vk == tcod.KEY_ESCAPE:
        return {'exit': True}
    
    return {}

def handle_book_screen_input(key):
    if key.vk == tcod.KEY_ESCAPE:
        return {'exit': True}
    
    return {}

def handle_spell_list_input(key):
    # Converts the key pressed into an index (a = 0, b = 1, etc)
    index = key.c - ord('a')

    # If the key press was a valid inventory index we return that index
    if index >= 0:
        return {'spell_list_index': index}
    
    # Exiting the game
    if key.vk == tcod.KEY_ESCAPE:
        return {'exit': True}
    
    return {}

def handle_targeting_input(key):
    if key.vk == tcod.KEY_ESCAPE:
        return {'exit': True}
    
    return {}

def handle_mouse(mouse):
    (x, y) = (mouse.cx, mouse.cy)

    if mouse.lbutton_pressed:
        return {'left_click': (x, y)}
    elif mouse.rbutton_pressed:
        return {'right_click': (x, y)}
    
    return {}

def handle_player_dead_input(key):
    
    # Get the character that was pressed
    key_char = chr(key.c)

    if key_char == 'i':
        return {'show_inventory': True}
    
    if key.vk == tcod.KEY_ESCAPE:
        return {'exit': True}
    
    return {}