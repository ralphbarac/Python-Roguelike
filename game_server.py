# Server file for network component of gameplay

import socket
from _thread import start_new_thread
import sys

from components import *
from map_objects import *
from entity import Entity

import tcod

import pickle

import random

server = "127.0.0.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection...")

available_hosts = []        # People available to be invaded

# These two lists should have the same indexes for players in the same game. ie. host_list[0] and invader_list[0] should be in the same game

host_list = []              # Hosts with active invasions
invader_list = []           # Active invaders

class Player:
    def __init__(self, conn, addr, host=False, game_state=None):
        self.conn = conn
        self.addr = addr
        self.host = host
        self.game_state = game_state

def matchmake(player):
    if(len(available_hosts) <= 0):
        host = None
    else:
        host = random.choice(available_hosts)
        host.host = True
        available_hosts.remove(host)
    return host

def invasion_thread(host, invader, game_state):
    invasion_finish = False
    print("INVASION FUNCTION")
    while invasion_finish == False:
        try:
            data = pickle.loads(host.conn.recv(4096 * 4))
            print("DATA IN INVASION FUNCTION")
            print(data)
        except:
            break
        
        if data['header'] == "am_i_host":
            print("TESTING HERE ALSO!")
            data = pickle.loads(host.conn.recv(4096 * 4))
            print("DID WE GET HERE? IF SO DATA BELOW??")
            print(data)

def client_thread(player):
    while True:
        try:
            data = pickle.loads(player.conn.recv(4096 * 4))
            print(data)
        except:
            break

        if data['header'] == "am_i_host":
            if player.host == True:
                msg = {'header': 'host_true', 'data': None}
                host_list.append(player)
                player.conn.send(pickle.dumps(msg))
            else:
                msg = {'header': 'host_false', 'data': None}
                player.conn.send(pickle.dumps(msg))

        if data['header'] == "invade":
            available_hosts.remove(player)      # don't want player in the pool of potential invadable hosts

            if player.host == True:
                msg = {'header': 'already_in_session', 'data': None}
                player.conn.send(pickle.dumps(msg))
                available_hosts.append(player)

            host = matchmake(player)    
            if(host is None):
                available_hosts.append(player)  # since there was no invasion the player is placed back into the active pool
                msg = {'header': 'no_host_found', 'data': None}
                player.conn.send(pickle.dumps(msg))
            else:
                invader_list.append(player)
                msg = {'header': 'invading_player', 'data': None}
                player.conn.send(pickle.dumps(msg))

        if data['header'] == "host_sending_vars":
            print("HERE")
            game_state = data['data']
            index = host_list.index(player)
            print("GOT GAME STATE STORED")
            msg = {'header': 'ok', 'data': None}
            player.conn.send(pickle.dumps(msg))
            print("SENT BACK MESSAGE")
           # start_new_thread(invasion_thread, (host_list[index], invader_list[index], game_state))

while True:
    connection = s.accept() # player is a (conn, addr) tuple

    player = Player(connection[0], connection[1], False)

    print("Connected to:", player.addr)

    available_hosts.append(player)
    # print("Available hosts are: {0}".format(available_hosts))
    
    start_new_thread(client_thread, (player,))



