import sys
import numpy as np
import binary_heap_gmin as hp
import random
import networkx as nx
import matplotlib.pyplot as plt
#from node_array import *
from InitGridworlds import *
from nodelist_array_mapping import *
from Astar_Exception import *
from InputData import *
# generate 50 gridworlds
gridworlds = GridWorlds()
# rows and colums
M = gridworlds.M
N = gridworlds.N

def manhattan(start,end):
    distance = 0
    distance = abs(start[0]-end[0]) + abs(start[1]-end[1])
    return int(distance)
def gen_path(endnode):
    # find path from end to start
    path = []
    tmp = endnode
    #while tmp.father!=None:
        #path.append(tmp)
        #tmp = tmp.father
    while tmp.pointer!=[0,0]:
        path.append(tmp)
        coord = (lambda x,y:[x[0]+y[0],x[1]+y[1]])\
        (tmp.pointer, node2arrayidx(tmp, nodeList, grid))
        tmp = arrayidx2node(coord, nodeList, grid)
    path.append(startnode)
    return path
grid = gridworlds.grids[0]
print sys.getsizeof(grid.array)
grid.array = np.asarray([map(int, i) for i in alist])
grid.array[0,0] = 0
grid.array[M-1,N-1] = 0
nodeList = []
def gen_node(grid):
    # @type grid: array
    counti, countj = 0, 0
    for i in grid.getarray():
        for j in i:
            if j==1:
                yield node(True, [counti,countj])
            if j==0:
                yield node(False, [counti,countj])
            countj = countj + 1
        countj = 0
        counti = counti + 1
for n in gen_node(grid):
    nodeList.append(n)

# search area for current point
def searcharea(searchlist, nodeList, i, j):
    """ i,j is the current point"""
    # Bound check
    try:
        grid.array[i+1,j]
    except IndexError:
        pass# at the bottom
    else:
        searchlist.append(nodeList[arrayidx2nodeidx([i+1,j], grid)])
    try:
        #grid.array[i-1,j]
        if i-1<0:
            raise IndexError
    except IndexError:
        pass# at the top
    else:
        searchlist.append(nodeList[arrayidx2nodeidx([i-1,j], grid)])
    try:
        grid.array[i,j+1]
    except IndexError:
        pass#at right
    else:
        searchlist.append(nodeList[arrayidx2nodeidx([i,j+1], grid)])
    try:
        #grid.array[i,j-1]
        if j-1<0:
            raise IndexError
    except IndexError:
        pass# at left
    else:
        searchlist.append(nodeList[arrayidx2nodeidx([i,j-1], grid)])
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
endpoint = [M-1, N-1]
startnode = nodeList[arrayidx2nodeidx(startpoint, grid)]
endnode = nodeList[arrayidx2nodeidx(endpoint, grid)]
# initial openlist closelist
closelist = []
# openlist is always a <node> binary heap
openlist = hp.Heap([])
searchlist = []
openlist.insert(startnode)
# add startnode from openlist to closelist
# minnode is the current searched point
# do loop finding the node with smallest f value and
# repeatly extend openlist and closelist until
# endpoint in openlist
def Astar():
    try:
        while len(openlist.newlist)>=1:
            searchlist = []
            minnode = openlist.pop()
            closelist.append(minnode)
            minnode.inclose = True
            # search current point
            """Warning arrayidx = nodeidx2arrayidx(nodeList.index(minnode), grid)"""
            arrayidx = minnode.arrayidx
            searchlist = searcharea(searchlist, nodeList, arrayidx[0], arrayidx[1])
            # add searchlist node to openlist if it has not already been in openlist and closelist
            # and set these nodes father the node was searched
            searchlistnodeupdate(searchlist,minnode)
            """for i in searchlist:
                if i in openlist.newlist:
                    # if node already in openlist, find whether path 
                    # searched node--> i has smaller g value
                    if minnode.g+1<i.g:
                        # change i father to searched node
                        #i.setfather(minnode)
                        i.pointer = (lambda x,y:[x[0]-y[0],x[1]-y[1]])\
                        (node2arrayidx(minnode, nodeList, grid), node2arrayidx(i, nodeList, grid))
                        # recalculate i's f and g
                        i.g = minnode.g+1
                        i.setf() 
                        # update openlist heap
                        if openlist.newlist.index(i)==0:
                            openlist.updateHeap('down')
                        elif openlist.hasChildNode(openlist.newlist.index(i))==False:
                            openlist.updateHeap('up', openlist.newlist.index(i))
                        else:
                            if i.f < openlist.newlist[openlist.father_idx(openlist.newlist.index(i))].f:
                                openlist.updateHeap('up', openlist.newlist.index(i))
                            elif i.f > openlist.newlist[openlist.min_child_idx(openlist.newlist.index(i))].f:
                                openlist.updateHeap('down', openlist.newlist.index(i))
                            else:
                                pass
                        #openlist.initialHeap(openlist.newlist)
                    continue
                if i in closelist:
                    continue
                #i.setfather(minnode)
                i.pointer = (lambda x,y:[x[0]-y[0],x[1]-y[1]])\
                (node2arrayidx(minnode, nodeList, grid), node2arrayidx(i, nodeList, grid))
                # calculate i's g h f
                i.h = manhattan(node2arrayidx(i, nodeList, grid),\
                node2arrayidx(endnode, nodeList, grid))
                i.g = minnode.g+1
                i.setf()
                openlist.insert(i)
                if i==endnode:
                    # find endnode in openlist, terminate
                    raise LoopEnd()"""
        # cannot reach the end
        print "cannot reach the end"
    except LoopEnd:
        print "find the path!"
def simpleadd(a,b):
    return [a[0]+b[0],a[1]+b[1]]
def simplesub(a,b):
    return [a[0]-b[0],a[1]-b[1]]
def visitedaction(i,minnode):
    if minnode.g+1<i.g:
        i.pointer = simplesub(node2arrayidx(minnode, nodeList, grid), node2arrayidx(i, nodeList, grid))
        i.g = minnode.g+1
        i.setf() 
            #if openlist.newlist.index(i)==0:
        if i.listidx==0:
            openlist.updateHeap('down')
            #elif openlist.hasChildNode(openlist.newlist.index(i))==False:
        elif openlist.hasChildNode(i.listidx)==False:
            openlist.updateHeap('up', i.listidx)
        else:
            if i.f < openlist.newlist[openlist.father_idx(i.listidx)].f:
                openlist.updateHeap('up', i.listidx)
            elif i.f > openlist.newlist[openlist.min_child_idx(i.listidx)].f:
                openlist.updateHeap('down', i.listidx)
            elif i.f == openlist.newlist[openlist.father_idx(i.listidx)].f and \
            i.f == openlist.newlist[openlist.min_child_idx(i.listidx)].f:
                if openlist.g=='max':
                    if openlist.newlist[openlist.father_idx(i.listidx)].g >= \
                    openlist.newlist[openlist.min_child_idx(i.listidx)].g:
                        # father has priority
                        openlist.updateHeap('up', i.listidx)
                    else:
                        openlist.updateHeap('down', i.listidx)
                if openlist.g=='min':
                    if openlist.newlist[openlist.father_idx(i.listidx)].g <= \
                    openlist.newlist[openlist.min_child_idx(i.listidx)].g:
                        # father has priority
                        openlist.updateHeap('up', i.listidx)
                    else:
                        openlist.updateHeap('down', i.listidx)
            elif i.f == openlist.newlist[openlist.father_idx(i.listidx)].f:
                openlist.updateHeap('up', i.listidx)
            elif i.f == openlist.newlist[openlist.min_child_idx(i.listidx)].f:
                openlist.updateHeap('down', i.listidx)
            else:
                pass
            #openlist.initialHeap(openlist.newlist
def searchlistnodeupdate(searchlist,minnode):
    for i in searchlist:
        #if i in openlist.newlist:
        if i.listidx!=None:
            visitedaction(i, minnode)
            """if minnode.g+1<i.g:
                i.pointer = simplesub(node2arrayidx(minnode, nodeList, grid), node2arrayidx(i, nodeList, grid))
                i.g = minnode.g+1
                i.setf() 
                #if openlist.newlist.index(i)==0:
                if i.listidx==0:
                    openlist.updateHeap('down')
                #elif openlist.hasChildNode(openlist.newlist.index(i))==False:
                elif openlist.hasChildNode(i.listidx)==False:
                    openlist.updateHeap('up', i.listidx)
                else:
                    if i.f < openlist.newlist[openlist.father_idx(i.listidx)].f:
                        openlist.updateHeap('up', i.listidx)
                    elif i.f > openlist.newlist[openlist.min_child_idx(i.listidx)].f:
                        openlist.updateHeap('down', i.listidx)
                    else:
                        pass
                #openlist.initialHeap(openlist.newlist)"""
            continue
        if i.inclose:
            continue
        newnodeaction(i, minnode)
        openlist.insert(i)
        if i==endnode:
            raise LoopEnd()


def newnodeaction(i, minnode):
    i.pointer = simplesub(node2arrayidx(minnode, nodeList, grid), node2arrayidx(i, nodeList, grid))
    i.h = manhattan(node2arrayidx(i, nodeList, grid), \
                    node2arrayidx(endnode, nodeList, grid))
    i.g = minnode.g + 1
    i.setf()


Astar()

path = gen_path(endnode)
matrix = np.zeros((M,N))
matrix_ = np.zeros((M,N))
for i in path:
    matrix[node2arrayidx(i, nodeList, grid)[0],node2arrayidx(i, nodeList, grid)[1]] = 1
print matrix[0:10,0:10]
print grid.array[0:10,0:10]
print len(closelist)
f = open('closelist' + openlist.g + '.txt', 'w')
for i in closelist:
    matrix_[i.arrayidx[0], i.arrayidx[1]] = 1
for i in matrix_:
    for j in i:
        f.write(str(int(j)))
    f.write("\n")
f.close()
f = open('path' + openlist.g + '.txt', 'w')
for i in matrix:
    for j in i:
        f.write(str(int(j)))
    f.write("\n")
f.close()
# min [<node_array.node instance at 0x10db0cd88>, <node_array.node instance at 0x10db0ccb0>, <node_array.node instance at 0x10dadb638>, <node_array.node instance at 0x10db0cbd8>, <node_array.node instance at 0x10dadb560>, <node_array.node instance at 0x10db0cb00>, <node_array.node instance at 0x10dadb488>, <node_array.node instance at 0x10db0ca28>, <node_array.node instance at 0x10dadb3b0>, <node_array.node instance at 0x10db0c950>]

# max [<node_array.node instance at 0x116a02d40>, <node_array.node instance at 0x116a02c68>, <node_array.node instance at 0x1169e25f0>, <node_array.node instance at 0x116a02b90>, <node_array.node instance at 0x1169e2518>, <node_array.node instance at 0x116a02ab8>, <node_array.node instance at 0x1169e2440>, <node_array.node instance at 0x116a029e0>, <node_array.node instance at 0x1169e2368>, <node_array.node instance at 0x116a02908>]

#exit = raw_input("pelease input:\n")








