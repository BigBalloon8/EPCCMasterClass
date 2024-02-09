from .client import setup_client
import time
from multiprocessing import Queue, Process
import numpy as np

"""
example_user_info = {
    "name": "USERNAME",
    "id": 0,
    "location": (0,0),
    "infected": False
}
"""

MOVES = {
            "up": np.array([-1, 0]),
            "down": np.array([1,0 ]),
            "left": np.array([0,-1]),
            "right": np.array([1,0])
        }

class API:
    def __init__(self, username:str = None, verbose = 0):
        # TODO check vaild username
        self.send_q = Queue()
        self.recv_q = Queue()
        client = Process(target=setup_client, args=(self.send_q, self.recv_q))
        client.start()

        self.send_q.put(f"new_user:{username}")
        while True:
            if not self.recv_q.empty():
                self.user_info = self.recv_q
                break
        self.map = None

    def move(self, direction: str = "forward"):
        time.sleep(0.2)
        self.send_q.put(f"mv:{moves[direction]}")
        while True:
            if not self.recv_q.empty():
                return self.recv_q.get()

    def get_map(self):
        self.send_q.put("map")
        while True:
            if not self.recv_q.empty():
                return self.recv_q.get()

    def _get_user_info(self, id):
        self.send_q("get_user:{id}")
        while True:
            if not self.recv_q.empty():
                return self.recv_q.get()

    def is_infected(self, id):
        time.sleep(0.4)
        _user_info = self._get_user_info(id)
        return _user_info["infected"]
    