import os
import shelve

def save_game(player, entities, game_map, message_log, game_state):
    with shelve.open('savegame.dat', 'n') as save_file:
        save_file['player_index'] = entities.index(player)
        save_file['entities'] = entities
        save_file['game_map'] = game_map
        save_file['message_log'] = message_log
        save_file['game_state'] = game_state

def load_game():
    if not os.path.isfile('savegame.dat'):
        raise FileNotFoundError

    with shelve.open('savegame.dat', 'r') as save_file:
        player_index = save_file['player_index']
        entities = save_file['entities']
        game_map = save_file['game_map']
        message_log = save_file['message_log']
        game_state = save_file['game_state']
    
    player = entities[player_index]

    return player, entities, game_map, message_log, game_state