import socket
import pickle

from components import *
from entity import Entity
from map_objects import *


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 5555
        self.addr = (self.server, self.port)
   
    def connect(self):
        try:
            self.client.connect(self.addr)
        except:
            pass
    
    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            data = pickle.loads(self.client.recv(4096 * 4))
            return data
        except socket.error as e:
            print(e)
    
    def send_obj(self, data):
        try:
            self.client.send(pickle.dumps(data))
            data = pickle.loads(self.client.recv(4096 * 4))
            return data
        except socket.error as e:
            print(e)
    