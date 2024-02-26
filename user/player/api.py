from client import setup_client
import time
from multiprocessing import Queue, Process
import json

"""
example_user_info = {
    "name": "USERNAME",
    "id": 0,
    "location": (0,0),
    "infected": False
}
"""

MOVES = {
            "up":    [0, -1],
            "down":  [0, 1],
            "left":  [-1, 0],
            "right": [1, 0]
        }

class API:
    def __init__(self, username:str = None, verbose = 0, port=54321):
        # TODO check vaild username
        self.send_q = Queue()
        self.recv_q = Queue()
        client = Process(target=setup_client, args=(self.send_q, self.recv_q, port))
        client.start()

        self.send_q.put(f"new_user:{username}")
        self.local_info = json.loads(self.recv_q.get())                
        self.map = None
        self.users = None
        self._update_users()
        self._update_map()

    def _update_map(self):
        self.send_q.put("map:-")
        self.map = json.loads(self.recv_q.get())

    def _update_users(self):
        self.send_q.put("users:-")
        self.users = json.loads(self.recv_q.get())
        self.local_info = self.users[self.local_info["id"]]


    def move(self, direction: str = "forward"):
        time.sleep(0.2)
        move = MOVES[direction]
        pos = self.local_info["location"]
        if (pos[0] + move[0] >= len(self.map[0])) or (pos[1] + move[1] >= len(self.map)) or (pos[0] + move[0] < 0) or (pos[1] + move[1] < 0):
            raise ValueError(f"Move in direction {direction} would cause position out side of map, Location: {pos}, Move: {move}, Map Size: ({len(self.map[0])},{len(self.map)})")
        self.send_q.put(f"mv:{move}")
        self.recv_q.get()
        new_pos = [pos[0] + move[0], pos[1] + move[1]]
        self.local_info["location"] = new_pos
    
    def print_map(self):
        self._update_map()
        for row in self.map:
            print(row)
    
    def am_i_infected(self):
        self._update_users()
        return self.users[self.local_info["id"]]["infected"]

    def __repr__(self):
        self._update_map()
        base = ""
        for row in self.map:
            base += str(row) + "\n"
        return base

    @property
    def position(self):
        return self.local_info
    
    def help():
        help_message = """

        """

        
    