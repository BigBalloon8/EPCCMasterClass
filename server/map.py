import random
import numpy as np


class Map:
    def __init__(self):
        gridsize = [10,10]
        self.map = [[[] for _ in range(gridsize[0])]for _ in range(gridsize[1])]
    
    @property
    def empty_pos(self):
        while True:
            x, y = random.randint(0, 19), random.randint(0, 19) 
            if self.map[x][y] == 0:
                return np.array([x,y], dtype=np.uint8)
    
    def update_player(self, id, id_pos, move, user_info):
        self.map[id_pos[1]][id_pos[0]].remove(id)
        newpos = id_pos
        newpos[0] += move[0]
        newpos[1] += move[1]
        pos_array = self.map[newpos[1]][newpos[0]]
        infected = False
        for user_id in pos_array:
            if user_info[user_id]["infected"]:
                infected = True
                
        self.map[newpos[1]][newpos[0]].append(id)
        return infected
        


