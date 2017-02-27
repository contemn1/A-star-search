import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt
from enum import Enum
from scipy import sparse
class node:
    def __init__(self,block,arrayidx):
        """ 
        @type block: bool
        """
        self.f = 0
        self.g = 0
        self.h = 0
        self.father = None
        self.pointer = [0,0]
        self.isBlock = block  
        self.arrayidx = arrayidx
        self.listidx = None
        self.inclose = False
    def setf(self):
        self.f = self.g + self.h
    def setfather(self,fathernode):
        """ @type fathernode: node"""
        self.father = fathernode
    def clean(self):
        self.f = 0
        self.g = 0
        self.h = 0
        self.pointer = [0,0]
        self.listidx = None
        self.inclose = False
class array:
    def __init__(self,m,n):
        # m rows n colums
        self.m = m
        self.n = n
        self.array = np.zeros((m,n),np.int8)
        #self.array_ = np.random((1001,1001),np.bool)
        self.graph = nx.DiGraph()
        self.initgraph()
        self.initBlock()
        self.array = sparse.csr_matrix(self.array)
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
        #p_list = [True,True,True,False,False,False,False,False,False,False]
        traverselist = self.DFS()
        for i in traverselist:
            self.array[i[0],i[1]] = random.choice(p_list)
    def getarray(self):
        return self.array