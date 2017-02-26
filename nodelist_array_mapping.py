def arrayidx2nodeidx(arrayidx, grid):
    """ 
    input array index return nodelist index

    @type arrayidx: list
    """
    nodeidx = arrayidx[0] * grid.n + arrayidx[1]
    return nodeidx
def nodeidx2arrayidx(nodeidx, grid):
    """ 
    input nodelist index return array index

    @type nodeidx: list
    """
    arrayidx = [0, 0]
    arrayidx[1] = nodeidx % grid.n
    arrayidx[0] = (nodeidx - arrayidx[1]) / grid.n
    return arrayidx
def node2arrayidx(node, nodelist, grid):
    """ return arrayidx"""
    #arrayidx = nodeidx2arrayidx(nodelist.index(node), grid)
    return node.arrayidx
def arrayidx2node(arrayidx, nodelist, grid):
    """return node"""
    return nodelist[arrayidx2nodeidx(arrayidx, grid)]
def node2node(node, shift, nodelist, grid):
    """
    tagetnode = node + shift

    @param node: current node
    @param shift: node shift value like [0,1] [-1,0]
    """
    arrayidx = node2arrayidx(node, nodelist, grid)
    arrayidx = [arrayidx[0] + shift[0], arrayidx[1] + shift[1]]
    newnode = arrayidx2node(arrayidx, nodelist, grid)
    return newnode