import numpy as np
import binary_heap_gmax as hp
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
tmparray = np.zeros((M,N))
def manhattan(start,end):
    distance = 0
    distance = abs(start[0]-end[0]) + abs(start[1]-end[1])
    return int(distance)
def gen_path(endnode, *arg):
    # find path from end to start
    path = []
    tmp = endnode
    #while tmp.father!=None:
        #path.append(tmp)
        #tmp = tmp.father
    if len(arg)==1:
        for i in range(arg[0]):
            path.append(tmp)
            coord = (lambda x,y:[x[0]+y[0],x[1]+y[1]])\
            (tmp.pointer, node2arrayidx(tmp, nodeList, grid))
            tmp = arrayidx2node(coord, nodeList, grid)
    else:
        while tmp.pointer!=[0,0]:
            path.append(tmp)
            coord = (lambda x,y:[x[0]+y[0],x[1]+y[1]])\
            (tmp.pointer, node2arrayidx(tmp, nodeList, grid))
            tmp = arrayidx2node(coord, nodeList, grid)
            path.append(startnode)
    return path
grid = gridworlds.grids[0]
grid.array = np.asarray([map(int, i) for i in alist])
grid.array[0,0] = 0
grid.array[M-1,N-1] = 0
nodeList = []
def gen_node(grid):
    # @type grid: array
    counti, countj = 0, 0
    #for i in grid.getarray():
    for i in tmparray:
        for j in i:
            if j==1:
                yield node(False, [counti,countj])
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
def probe(i, j, grid):
        # Bound check
    newblockidx = []
    try:
        tmparray[i+1,j]
    except IndexError:
        pass# at the bottom
    else:
        if grid.array[i+1,j]==1 and tmparray[i+1,j]==0:
            tmparray[i+1,j] = 1
            newblockidx.append([i+1,j])
    try:
        if i-1<0:
            raise IndexError
    except IndexError:
        pass# at the top
    else:
        if grid.array[i-1,j]==1 and tmparray[i-1,j]==0:
            tmparray[i-1,j] = 1
            newblockidx.append([i-1,j])
    try:
        tmparray[i,j+1]
    except IndexError:
        pass#at right
    else:
        if grid.array[i,j+1]==1 and tmparray[i,j+1]==0:
            tmparray[i,j+1] = 1
            newblockidx.append([i,j+1])
    try:
        if j-1<0:
            raise IndexError
    except IndexError:
        pass# at left
    else:
        if grid.array[i,j-1]==1 and tmparray[i,j-1]==0:
            tmparray[i,j-1] = 1
            newblockidx.append([i,j-1])
    return newblockidx
def blockinpath(path, nodeList, grid):
    """
    path has 5 nodes.
    return the former node before block or the 5th node
    """
    for i in path:
        if i == path[-1]:
            pathend = i
            break
        if i in blocklist:
            # stop at the first block set it's father as end
            pathend = node2node(i, i.pointer, nodeList, grid)
            break
    return pathend
# input start point end point
startpoint = [0, 0] 
endpoint = [M-1,N-1]
startnode = nodeList[arrayidx2nodeidx(startpoint, grid)]
endnode = nodeList[arrayidx2nodeidx(endpoint, grid)]
# initial openlist closelist
closelist = []
blocklist = []
newblockidx = []
# openlist is always a <node> binary heap
Endflag = False


def visitedaction(i, minnode):
    if minnode.g + 1 < i.g:
        # change i father to searched node
        # i.setfather(minnode)
        i.pointer = (lambda x, y: [x[0] - y[0], x[1] - y[1]]) \
            (node2arrayidx(minnode, nodeList, grid), node2arrayidx(i, nodeList, grid))
        # recalculate i's f and g
        i.g = minnode.g + 1
        i.setf()
        if i.listidx == 0:
            openlist.updateHeap('down')
            # elif openlist.hasChildNode(openlist.newlist.index(i))==False:
        elif openlist.hasChildNode(i.listidx) == False:
            openlist.updateHeap('up', i.listidx)
        else:
            if i.f < openlist.newlist[openlist.father_idx(i.listidx)].f:
                openlist.updateHeap('up', i.listidx)
            elif i.f > openlist.newlist[openlist.min_child_idx(i.listidx)].f:
                openlist.updateHeap('down', i.listidx)
            elif i.f == openlist.newlist[openlist.father_idx(i.listidx)].f and \
                            i.f == openlist.newlist[openlist.min_child_idx(i.listidx)].f:
                if openlist.g == 'max':
                    if openlist.newlist[openlist.father_idx(i.listidx)].g >= \
                            openlist.newlist[openlist.min_child_idx(i.listidx)].g:
                        # father has priority
                        openlist.updateHeap('up', i.listidx)
                    else:
                        openlist.updateHeap('down', i.listidx)
                if openlist.g == 'min':
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


def newnodeaction(i, minnode):
    i.pointer = (lambda x, y: [x[0] - y[0], x[1] - y[1]]) \
        (node2arrayidx(minnode, nodeList, grid), node2arrayidx(i, nodeList, grid))
    # calculate i's g h f
    if i.inclose == False:
        i.h = manhattan(node2arrayidx(i, nodeList, grid), \
                        node2arrayidx(endnode, nodeList, grid))
    i.g = minnode.g + 1
    i.setf()


while True:
    count = 0
    openlist = hp.Heap([])
    searchlist = []
    newblockidx = []
    # update new 1 to tmparray map
    newblockidx.extend(probe(startnode.arrayidx[0], startnode.arrayidx[1], grid))
    # update corresponding node to block
    for i in newblockidx:
        arrayidx2node(i, nodeList, grid).isBlock = True
        # clean node
        arrayidx2node(i, nodeList, grid).clean()
        # update recorded block to 1 in tmparray map
    for i in blocklist:
        i.isBlock = True
        i.clean()
    # clean blocklist
    blocklist = []
    if startnode.h==0:
        startnode.h = manhattan(node2arrayidx(startnode, nodeList, grid),\
                    node2arrayidx(endnode, nodeList, grid))
    startnode.g = 0
    startnode.setf()
    openlist.insert(startnode)
    # add startnode from openlist to closelist
    # minnode is the current searched point
    # do loop finding the node with smallest f value and
    # repeatly extend openlist and closelist until
    # endpoint in openlist
    try:
        while len(openlist.newlist)>1:
            searchlist = []
            minnode = openlist.pop()
            count = count + 1
            #if len(closelist) % 4==0 and len(closelist)!=0:
            if count==5:
                path = gen_path(minnode, 5)
                path.reverse()
                pathend = blockinpath(path, nodeList, grid)
                # update h value in closelist
                for i in closelist:
                    i.h = pathend.f - i.g
                startnode = pathend
                break
            closelist.append(minnode)
            # search current point
            # arrayidx = nodeidx2arrayidx(nodeList.index(minnode), grid)
            arrayidx = minnode.arrayidx
            # update tmparray map
            newblockidx.extend(probe(minnode.arrayidx[0], minnode.arrayidx[1], grid))
            # search area first ignore potential block
            searchlist = searcharea(searchlist, nodeList, arrayidx[0], arrayidx[1])
            # update corresponding node to block
            #for i in newblockidx:
            #    arrayidx2node(i, nodeList, grid).isBlock = True
            # add searchlist node to openlist if it has not already been in openlist and closelist
            # and set these nodes father the node was searched
            for i in searchlist:
                if i.listidx!=None:
                    # if node already in openlist, find whether path 
                    # searched node--> i has smaller g value
                    visitedaction(i, minnode)
                    continue
                if i.inclose:
                    continue
                #i.setfather(minnode)
                newnodeaction(i, minnode)
                # add it to scout list
                if i.arrayidx in newblockidx:
                    if i not in blocklist:
                        blocklist.append(i)
                openlist.insert(i)
                if i==endnode:
                    # find endnode in openlist, terminate
                    raise LoopEnd()
        # cannot reach the end
        if count!=5:
            print "cannot reach the end"
            Endflag = True
        if len(openlist.newlist)<=1:
            print " open list is empty"
    except LoopEnd:
        print "find the path!"
        Endflag = True
    if Endflag==True:
        break

path = gen_path(endnode)
matrix = np.zeros((M,N))
matrix_ = np.zeros((M,N))
for i in path:
    matrix[node2arrayidx(i, nodeList, grid)[0],node2arrayidx(i, nodeList, grid)[1]] = 1
print closelist[0:10], '\n', len(closelist)
f = open('closelistAA' + openlist.g + '.txt', 'w')
for i in closelist:
    matrix_[i.arrayidx[0], i.arrayidx[1]] = 1
for i in matrix_:
    for j in i:
        f.write(str(int(j)))
    f.write("\n")
f.close()
f = open('pathAA' + openlist.g + '.txt', 'w')
for i in matrix:
    for j in i:
        f.write(str(int(j)))
    f.write("\n")
f.close()








