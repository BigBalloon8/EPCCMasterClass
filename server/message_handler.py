import socket
from multiprocessing import Queue
import json

from map import Map

class Handler:
    def __init__(self):
        self.users = []
        self.address_lookup = {}
        self.map = Map()

    
    def __call__(self, message: str, address: str):
        print(address, message)
        if len(message) == 0:
            if address in self.address_lookup.keys():
                return
        header, packet = message.split(":")
        print(header)
        if header == "new_user":
            print("initialising user")
            return self.init_user(packet, address).encode()
        elif header == "mv":
            return self.move(packet, address).encode()
        elif header == "map":
            return self.get_map().encode()
        elif header == "users":
            return self.get_users().encode()
        else:
            raise Exception


    def init_user(self, username, address):
        if address in self.address_lookup.keys():
            return json.dumps(self.users[self.address_lookup[address]])
        id = len(self.users)
        start_pos = self.map.empty_pos(id)
        user_info = {
            "name": username,
            "address": address,
            "id": id,
            "location": start_pos,
            "infected": False
        }
        self.address_lookup[address] = id
        self.users.append(user_info)
        return json.dumps(user_info)

    def move(self, move, address):
        move = json.loads(move)
        id = self.address_lookup[address]
        try:
            infected, new_pos = self.map.update_player(id, self.users[id]["location"], move, self.users)
            self.users[id]["infected"] = infected
            self.users[id]["location"] = new_pos
            return "0"
        except AssertionError:
            return "1"

    def get_map(self): 
        return json.dumps(self.map.map)

    def get_users(self):
        return json.dumps(self.users)

    


def message_handler(message_queue: Queue):
    handler = Handler()
    while True:
        sock, address, message = message_queue.get()
        return_message = handler(message, address)
        if return_message:
            print(f"sending: '{return_message.decode()}', to {address}'")
            sock.sendall(return_message)