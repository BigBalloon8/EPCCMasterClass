import random


class Map:
    def __init__(self):
        gridsize = [10,10]
        self.map = [[[] for _ in range(gridsize[0])]for _ in range(gridsize[1])]
    
    def empty_pos(self, id):
        while True:
            x, y = random.randint(0, 9), random.randint(0, 9) 
            if len(self.map[y][x]) == 0:
                self.map[y][x].append(id)
                return [x,y]
    
    def update_player(self, id, id_pos, move, user_info):
        self.map[id_pos[1]][id_pos[0]].remove(id)
        newpos = id_pos
        newpos[0] += move[0]
        newpos[1] += move[1]
        assert newpos[0] >= 0 and newpos[1] >= 0
        pos_array = self.map[newpos[1]][newpos[0]]
        infected = False
        for user_id in pos_array:
            if user_info[user_id]["infected"]:
                infected = True
        self.map[newpos[1]][newpos[0]].append(id)
        return infected , newpos
        


