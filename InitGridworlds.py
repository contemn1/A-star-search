from node_array import *

class GridWorlds:
    def __init__(self):
        # rows and colums
        self.M = 1001
        self.N = 1
        self.grids = list(self.gen_gridworlds())
    # generate 50 gridworlds
    def gen_gridworlds(self):
        for i in range(1):
            yield array(self.M,self.N)

