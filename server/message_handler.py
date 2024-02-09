import socket
from multiprocessing import Queue
import numpy as np
import json

from map import Map

class Handler:
    def __info__(self):
        self.users = []
        self.address_lookup = {}
        self.map = Map()

    
    def __call__(self, message: str, address: str):
        header, packet = message.split(":")
        if header == "get_new":
            self.init_user(packet, address)

    def init_user(self, username, address):
        if address in self.address_lookup.keys():
            ...
        id = len(self.users)
        start_pos = self.map.empty_pos
        user_info = {
            "name": username,
            "address": address,
            "id": id,
            "location": f"{start_pos}",
            "infected":False
        }
        self.address_lookup[address] = id
        self.users.append(user_info)
        return json.dumps(user_info)

    def move(self, move, address):
        id = self.address_lookup[address]
        infected = self.map.update_player(id, self.users[id]["location"], move, self.users)
        self.users["infected"] = infected



    


def message_handler(message_queue: Queue):
    handler = Handler()
    while True:
        if not message_queue.empty():
            sock, address, message = message_queue.get()
            
            sock.sendall(response.encode('utf-8'))