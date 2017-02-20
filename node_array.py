import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt

class node:
    def __init__(self,block):
        """ 
        @type block: bool
        """
        self.f = 0
        self.g = 0
        self.h = 0
        self.father = None
        self.isBlock = block  
    def setf(self):
        self.f = self.g + self.h
    def setfather(self,fathernode):
        """ @type fathernode: node"""
        self.father = fathernode
class array:
    def __init__(self,m,n):
        # m rows n colums
        self.m = m
        self.n = n
        self.array = np.zeros((m,n))
        self.graph = nx.DiGraph()
        self.initgraph()
        self.initBlock()
    def DFS(self):
        traverselist = list(nx.dfs_preorder_nodes(self.graph,(0,0)))
        return traverselist
    def gen_index(self):
        for i in range(self.m):
            for j in range(self.n):
                yield (i,j)
    def initgraph(self):
        for i in self.gen_index():
            self.graph.add_node(i)
        for i in self.gen_index():
            if i[1]==len(range(self.n))-1 and i[0]!=len(range(self.m))-1:
                self.graph.add_edge(i,(i[0]+1,i[1]))
            elif i[0]==len(range(self.m))-1 and i[1]!=len(range(self.n))-1:
                self.graph.add_edge(i,(i[0],i[1]+1))
            elif i[1]==len(range(self.n))-1 and i[0]==len(range(self.m))-1:
                pass
            else:
                self.graph.add_edge(i,(i[0]+1,i[1]))
                self.graph.add_edge(i,(i[0],i[1]+1))
        # convert to undirected
        self.graph = self.graph.to_undirected()
    def initBlock(self):
        # block chance 0.3
        p_list = [1,1,1,0,0,0,0,0,0,0]
        traverselist = self.DFS()
        for i in traverselist:
            self.array[i[0],i[1]] = random.choice(p_list)
    def getarray(self):
        return self.array
