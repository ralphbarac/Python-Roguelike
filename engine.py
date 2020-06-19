import tcod

from death_functions import kill_monster, kill_player
from entity import get_blocking_entities
from fov_functions import initialize_fov, recompute_fov
from game_messages import Message
from game_states import GameStates
from input import handle_generic_input, handle_main_menu_input, handle_mouse
from load_functions.init_new_game import get_constants, get_game_variables
from load_functions.data_loaders import load_game, save_game
from menus import main_menu, message_box
from render_functions import clear_all, render_all

from network import Network

"""
def check_invasion(network):
    msg = {'header': 'am_i_host', 'data': None}
    response = network.send(msg)
    if(response['header'] == 'host_true'):
        return True
    else:
        return False
"""


def game(player, entities, game_map, message_log, game_state, console, panel, constants):
   # am_i_host = False
   # am_i_invader = False

    fov_recompute = True

    fov_map = initialize_fov(game_map)


    key = tcod.Key()
    mouse = tcod.Mouse()

    """
    network = Network()     
    network.connect()                # Connect to the game server, adds player to the list of available hosts
    """

    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state    # Previous state keeps track of game state previous to opening a menu (or similar) so we can return to that state

    targeting_spell = None

    # Beginning of game loop
    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE_PRESS, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, constants['fov_radius'])

        render_all(console, panel, entities, player, game_map, fov_map, fov_recompute, message_log, constants['screen_width'], constants['screen_height'], constants['bar_width'], constants['panel_height'], constants['panel_y'], mouse, game_state)
        tcod.console_flush()

        clear_all(console, entities)

        action = handle_generic_input(key, game_state)
        mouse_action = handle_mouse(mouse)

        # These actions come from the input.py file
        move = action.get('move')
        wait = action.get('wait')
        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        inventory_index = action.get('inventory_index')
        use_bonfire = action.get('use_bonfire')
        level_up = action.get('level_up')
        show_character_screen = action.get('show_character_screen')
        show_book_screen = action.get('show_book_screen')
        show_spell_list = action.get('show_spell_list')
        spell_list_index = action.get('spell_list_index')
        drop_inventory = action.get('drop_inventory')
        exit = action.get('exit')

        left_click = mouse_action.get('left_click')
        right_click = mouse_action.get('right_click')

        # Initialize an array to store actions the player takes
        player_turn_results = []

        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move

            dest_x = player.x + dx
            dest_y = player.y + dy 
           
            if not game_map.is_blocked(dest_x, dest_y):
                target = get_blocking_entities(entities, dest_x, dest_y)

                if target:
                    attack_results = player.combat_entity.attack(target)
                    player_turn_results.extend(attack_results)
                else:
                    player.move(dx, dy)
                    if player.isHasted():
                        if not game_map.is_blocked(dest_x + dx, dest_y + dy):
                            player.move(dx, dy)
                    fov_recompute = True
                
                game_state = GameStates.STATUS_EFFECT_RESOLUTIONS
        
        elif wait:
            game_state = GameStates.STATUS_EFFECT_RESOLUTIONS
        
        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y:
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)

                    break
            else:
                message_log.add_message(Message('There are no items to pick up here.', tcod.yellow))
        
        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY
        
        if drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY
        
        if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(player.inventory.items):
            item = player.inventory.items[inventory_index]
            
            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(player.inventory.use(item))
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))
        
        if game_state == GameStates.TARGETING:
            if left_click:
                target_x, target_y = left_click

                spell_result = player.book.cast_spell(targeting_spell, entities=entities, game_map=game_map, fov_map=fov_map, target_x=target_x, target_y=target_y)
                player_turn_results.extend(spell_result)

            elif right_click:
                player_turn_results.append({'targeting_cancelled': True})
        
        if show_spell_list:
            previous_game_state = game_state
            game_state = GameStates.SPELL_LIST
        
        if spell_list_index is not None and previous_game_state != GameStates.PLAYER_DEAD and spell_list_index < len(player.book.get_book_spell_list()):
            spell = player.book.spell_list[spell_list_index]

            if game_state == GameStates.SPELL_LIST:
                player_turn_results.extend(player.book.cast_spell(spell, entities=entities, fov_map=fov_map, game_map=game_map))
        
        if use_bonfire and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.bonfire and entity.x == player.x and entity.y == player.y:
                    player.score += 50
                    entities = game_map.descend(player, message_log, constants)
                    fov_map = initialize_fov(game_map)
                    fov_recompute = True
                    tcod.console_clear(console)

                    break

                else:
                    message_log.add_message(Message('There is no bonfire here to rest at.', tcod.yellow))
        
        if level_up:
            player.score = player.score + (player.level.current_level * 200)
            if level_up == 'hp':
                player.combat_entity.base_max_hp += 20
            elif level_up == 'mp':
                player.combat_entity.base_max_mana += 20
            elif level_up == 'pow':
                player.combat_entity.base_power += 5
            elif level_up == 'def':
                player.combat_entity.base_defense += 5

            player.combat_entity.hp = player.combat_entity.max_hp       # We set health and mana to max mana to 'refill' on level-up
            player.combat_entity.mana = player.combat_entity.max_mana
            game_state = previous_game_state
        
        if show_character_screen:
            previous_game_state = game_state
            game_state = GameStates.CHARACTER_SCREEN
       
        if show_book_screen:
            previous_game_state = game_state
            game_state = GameStates.BOOK_SCREEN
        

        if exit:
            # Exiting from the inventory returns us to the previous game state
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY, GameStates.CHARACTER_SCREEN, GameStates.BOOK_SCREEN, GameStates.SPELL_LIST):
                game_state = previous_game_state
            elif game_state == GameStates.TARGETING:
                player_turn_results.append({'targeting_cancelled': True})
            # Otherwise game exits
            else:             
                return True

        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')         # message message comes whenever a player is notified of an event (various files)
            dead_entity = player_turn_result.get('dead')        # dead message comes from combat_entity class 
            item_added = player_turn_result.get('item_added')   # item_added message comes from inventory class
            item_consumed = player_turn_result.get('consumed')  # consumed message comes from the inventory class
            item_dropped = player_turn_result.get('item_dropped') # item_dropped message comes from the inventory class
            equip = player_turn_result.get('equip')               # equip message comes from the inventory class
             # invade = player_turn_result.get('invade')           # invade message comes from the item_functions class
            targeting = player_turn_result.get('targeting')     # targeting message comes from book class
            targeting_cancelled = player_turn_result.get('targeting_cancelled') # targetting_cancelled message comes from engine
            spell_success = player_turn_result.get('spell_success') # spell_success comes from the spell functions class
            xp = player_turn_result.get('xp')

            if message:
                message_log.add_message(message)
            
            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)
                
                message_log.add_message(message)
            
            if item_added:
                entities.remove(item_added)
                game_state = GameStates.STATUS_EFFECT_RESOLUTIONS
            
            if item_consumed:
                game_state = GameStates.STATUS_EFFECT_RESOLUTIONS
            
            if targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING

                targeting_spell = targeting

                message_log.add_message(targeting_spell.targeting_message)
            
            if targeting_cancelled:
                game_state = previous_game_state

                message_log.add_message(Message('Targetting cancelled'))

            if spell_success:
                game_state = previous_game_state
            
            if item_dropped:
                entities.append(item_dropped)
                game_state = GameStates.STATUS_EFFECT_RESOLUTIONS
            
            if equip:
                equip_results = player.book.toggle_page(equip)

                for equip_result in equip_results:
                    equipped = equip_result.get('equipped')
                    dequipped = equip_result.get('dequipped')

                    if equipped:
                        message_log.add_message(Message('You equipped the {0}'.format(equipped.name)))
                    
                    if dequipped:
                        message_log.add_message(Message('You dequipped the {0}'.format(dequipped.name)))
                
                game_state = GameStates.STATUS_EFFECT_RESOLUTIONS


            """
            if invade:
               msg = {'header': 'invade', 'data': None}
               response = network.send(msg)

               if(response['header'] == 'no_host_found'):
                   message = Message('No available hosts found to invade.', tcod.dark_pink)
                   message_log.add_message(message)
                   game_state = GameStates.STATUS_EFFECT_RESOLUTIONS
               elif(response['header'] == 'invading_player'):
                    message = Message('You are invading a new world...', tcod.dark_pink)
                    am_i_invader = True
                    message_log.add_message(message)
                    
                    if response['header'] == 'game_vars':
                        old_entities = entities     # we need to store the old game state
                        entities = response['data'][0]  # making invaders entities the hosts entities
                        entities.append(response['data'][1]) # adding the host to the entity list for the invader
                        entities.append(player) # adding the invader to his own entity list
                        game_map = response['data'][2]  # changing the invaders map to the hosts map
                        print("WE GOT HERE")
                    
                    game_state = GameStates.INVADER
               elif(response['header'] == 'already_in_session'):
                    message = Message('You are already in an invasion instance!', tcod.dark_pink)
                    message_log.add_message(message)
            """
            
            if xp:
                player.score += xp
                leveled_up = player.level.add_xp(xp)
                message_log.add_message(Message('You gain {0} experience points.'.format(xp)))

                if leveled_up:
                    player.score = player.score + (player.level.current_level * 200)
                    message_log.add_message(Message('You have leveled up! You reached level {0}'.format(player.level.current_level) + '!', tcod.pink))
                    previous_game_state = game_state
                    game_state = GameStates.LEVEL_UP
               
                
        if game_state == GameStates.STATUS_EFFECT_RESOLUTIONS:

            for entity in entities:
                if entity.combat_entity:
                    status_effect_results = entity.combat_entity.apply_status_effects()
                    for status_effect_result in status_effect_results:
                        message_log.add_message(status_effect_result.get('message'))
                    if game_map.tiles[entity.x][entity.y].trap:
                        if game_map.tiles[entity.x][entity.y].trap.caster != entity:
                            trap_results = game_map.tiles[entity.x][entity.y].trap.function(game_map.tiles[entity.x][entity.y].trap.function_kwargs, entity)
                            for trap_result in trap_results:
                                message = trap_result.get('message')
                                dead_entity = trap_result.get('dead')
                                xp = trap_result.get('xp')

                                if message:
                                    message_log.add_message(message)
                                
                                if dead_entity:
                                    if dead_entity == player:
                                        message, game_state = kill_player(dead_entity)
                                    else:
                                        message = kill_monster(dead_entity)

                                if xp:
                                    leveled_up = player.level.add_xp(xp)
                                    player.score += xp 
                                    message_log.add_message(Message('You gain {0} experience points.'.format(xp)))

                                    if leveled_up:
                                        message_log.add_message(Message('You have leveled up! You reached level {0}'.format(player.level.current_level) + '!', tcod.pink))
                                        previous_game_state = game_state
                                        game_state = GameStates.LEVEL_UP

                            game_map.tiles[entity.x][entity.y].trap = None 
            
            # We check if the player has been invaded and if so get the game ready to send to the invader.
            """
            if am_i_host == False and am_i_invader == False:
                am_i_host = check_invasion(network)
                if am_i_host == True:
                    player.set_name('Host')
                    message = Message('You are being invaded!!', tcod.light_crimson)
                    message_log.add_message(message)
                    game_state = GameStates.INVASION_HOST
                else:
                    game_state = GameStates.ENEMY_TURN
            """
            
            game_state = GameStates.ENEMY_TURN
            # This portion needs implementation, game state changes upon your game being invaded or you invading another game.
            # Need to load the correct map (hosts), entities, etc, on both screens. 

        """
        if game_state == GameStates.INVASION_HOST:    
            
            print("inside client invasion host")
            game_vars = (entities, player, game_map)
            msg = {'header': 'host_sending_vars', 'data': 'test'}
            print("pre object send")
            response = network.send(msg)
            print("post object send")
            print(response)
            

            game_state = GameStates.ENEMY_TURN
        
        if game_state == GameStates.INVADER:
            game_state = GameStates.ENEMY_TURN
        
        """

        if game_state == GameStates.ENEMY_TURN:

            for entity in entities:

                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            message_log.add_message(message)
                        
                        if dead_entity:
                            
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)
                            
                            message_log.add_message(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break
                    
                    if game_state == GameStates.PLAYER_DEAD:
                        break
                
            else:
                    game_state = GameStates.PLAYERS_TURN
    

def main():
    
    constants = get_constants()

    # Reads image file for font type
    tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    # Creates the screen given width, height, title, and a boolean for fullscreen
    tcod.console_init_root(constants['screen_width'], constants['screen_height'], constants['window_title'], False)

    console_main = tcod.console_new(constants['screen_width'], constants['screen_height'])
    console_panel = tcod.console_new(constants['screen_width'], constants['panel_height'])

    player = None
    entities = []
    game_map = None
    message_log = None
    game_state = None

    show_main_menu = True
  
    key = tcod.Key()
    mouse = tcod.Mouse()

    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, key, mouse)

        if show_main_menu:
            main_menu(console_main, constants['screen_width'], constants['screen_height'])
            
            tcod.console_flush()

            action = handle_main_menu_input(key)

            new_game = action.get('new_game')
            exit_game = action.get('exit')

            if new_game:
                player, entities, game_map, message_log, game_state = get_game_variables(constants)
                game_state = GameStates.PLAYERS_TURN

                show_main_menu = False
            elif exit_game:
                break
        else:
            tcod.console_clear(console_main)
            game(player, entities, game_map, message_log, game_state, console_main, console_panel, constants)

            show_main_menu = True
    
if __name__ == '__main__':
    main()