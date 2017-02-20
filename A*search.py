import numpy as np
import binary_heap as hp
import random
import networkx as nx
import matplotlib.pyplot as plt
from node_array import *

# rows and colums
M = 7
N = 8
class BlockError(Exception):
    def __init__(self,node):
        """ @type node: node"""
        Exception.__init__(self)
        self.node = node
class LoopEnd(Exception):
    def __init__(self):
        Exception.__init__(self)
def manhattan(start,end):
    distance = 0
    distance = abs(start[0]-end[0]) + abs(start[1]-end[1])
    return int(distance)
# generate 50 gridworlds
def gen_gridworlds():
    for i in range(50):
        yield array(M,N)
grids = list(gen_gridworlds())
grid = grids[1]
grid.array[0,0] = 0
grid.array[M-1,N-1] = 0
#nx.draw(grid.graph)
#plt.savefig('ego_graph.png')
#plt.show()
nodeList = []
def gen_node(grid):
    # @type grid: array
    for i in grid.getarray():
        for j in i:
            if j==1:
                yield node(True)
            if j==0:
                yield node(False)
for n in gen_node(grid):
    nodeList.append(n)
def arrayidx2nodeidx(arrayidx):
    """ 
    input array index return nodelist index

    @type arrayidx: list
    """
    nodeidx = arrayidx[0] * grid.n + arrayidx[1]
    return nodeidx
def nodeidx2arrayidx(nodeidx):
    """ 
    input nodelist index return array index

    @type nodeidx: list
    """
    arrayidx = [0, 0]
    arrayidx[1] = nodeidx % grid.n
    arrayidx[0] = (nodeidx - arrayidx[1]) / grid.n
    return arrayidx
# search area for current point
def searcharea(searchlist, nodeList, i, j):
    """ i,j is the current point"""
    flag = []
    # Bound check
    try:
        grid.array[i+1,j]
    except IndexError:
        flag.append('bottom')# at the bottom
    else:
        searchlist.append(nodeList[arrayidx2nodeidx([i+1,j])])
    try:
        #grid.array[i-1,j]
        if i-1<0:
            raise IndexError
    except IndexError:
        flag.append('top')# at the top
    else:
        searchlist.append(nodeList[arrayidx2nodeidx([i-1,j])])
    try:
        grid.array[i,j+1]
    except IndexError:
        flag.append('right')#at right
    else:
        searchlist.append(nodeList[arrayidx2nodeidx([i,j+1])])
    try:
        #grid.array[i,j-1]
        if j-1<0:
            raise IndexError
    except IndexError:
        flag.append('left')# at left
    else:
        searchlist.append(nodeList[arrayidx2nodeidx([i,j-1])])
    # Block check
    removelist = []
    for i in searchlist:
        try:
            if i.isBlock:
                raise BlockError(i)
        except BlockError as e:
            removelist.append(e.node)
    if len(removelist)!=0:
        for i in removelist:
            searchlist.remove(i)
    return searchlist

# input start point end point
startpoint = [0, 0] 
endpoint = [M-1,N-1]
startnode = nodeList[arrayidx2nodeidx(startpoint)]
endnode = nodeList[arrayidx2nodeidx(endpoint)]
# initial openlist closelist
closelist = []
# openlist is always a <node> binary heap
openlist = hp.Heap([])
searchlist = []
openlist.insert(nodeList[arrayidx2nodeidx(startpoint)])
# add startnode from openlist to closelist
# minnode is the current searched point
# do loop finding the node with smallest f value and
# repeatly extend openlist and closelist until
# endpoint in openlist
try:
    while len(openlist.newlist)>=1:
        searchlist = []
        minnode = openlist.pop()
        closelist.append(minnode)
        # search current point
        arrayidx = nodeidx2arrayidx(nodeList.index(minnode))
        searchlist = searcharea(searchlist, nodeList, arrayidx[0], arrayidx[1])
        # add searchlist node to openlist if it has not already been in openlist and closelist
        # and set these nodes father the node was searched
        for i in searchlist:
            if i in openlist.newlist:
                # if node already in openlist, find whether path 
                # searched node--> i has smaller g value
                if minnode.g+1<i.g:
                    # change i father to searched node
                    i.setfather(minnode)
                    # recalculate i's f and g
                    i.g = minnode.g+1
                    i.setf() 
                    # update openlist heap
                    openlist.initialHeap(openlist.newlist)
                continue
            if i in closelist:
                continue
            i.setfather(minnode)
            # calculate i's g h f
            i.h = manhattan(nodeidx2arrayidx(nodeList.index(i)),\
            nodeidx2arrayidx(nodeList.index(endnode)))
            i.g = minnode.g+1
            i.setf()
            openlist.insert(i)
            if i==endnode:
                # find endnode in openlist, terminate
                raise LoopEnd()
    # cannot reach the end
    print "cannot reach the end"
except LoopEnd:
    print "find the path!"
def gen_path():
    # find path from end to start
    path = []
    tmp = endnode
    while tmp.father!=None:
        path.append(tmp)
        tmp = tmp.father
    path.append(startnode)
    return path
path = gen_path()
matrix = np.zeros((M,N))
for i in path:
    matrix[nodeidx2arrayidx(nodeList.index(i))[0],nodeidx2arrayidx(nodeList.index(i))[1]] = 1
print matrix
print grid.array








