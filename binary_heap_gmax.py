import math
class Heap:
    """
    Remember to use validate() method to check order's correctness
    """
    def __init__(self,oldlist):
        '''
        node is a cell in maze, nodelist is a list of node,
        sort nodelist by node.f

        @type oldlist:nodelist
        @type newlist:nodelist
        '''
        # Heap root
        self.root = 0
        # Raw list
        self.oldlist = oldlist
        # Ordered heaplist
        self.newlist = []
        self.g = 'max'
    def insert(self, value):
        """
        Add element to the list end, and from bottom to top update

        @type value: node
        """
        self.newlist.append(value)
        value.listidx = len(self.newlist)-1
        self.updateHeap('up')
    def pop(self):
        """ 
        Delete root element
        
        return a node
        """
        if len(self.newlist)==1:
            a = self.newlist[0]
            a.listidx = None
            self.newlist.pop()
            return a
        if len(self.newlist)==0:
            return EOFError
        a = self.newlist[0]
        a.listidx = None
        self.newlist[0] = self.newlist[-1]
        self.newlist[0].listidx = 0
        self.newlist.pop()
        self.updateHeap('down')
        return a
    def left_child_idx(self, i):
        """ 
        Find left child index, 2k+1

        @type i : int
        """
        return ((i + 1) << 1) - 1
    def right_child_idx(self, i):
        """ 
        Find right child index, 2k+2

        @type i : int
        """
        return (((i + 1) << 1) + 1) - 1
    def father_idx(self, i):
        return int(math.floor((i - 1) >> 1))
    def min_child_idx(self, i):
        if self.right_child_idx(i)>=len(self.newlist):
            return ((i + 1) << 1) - 1
        if self.newlist[self.left_child_idx(i)].f < self.newlist[self.right_child_idx(i)].f:
            return ((i + 1) << 1) - 1
        elif self.newlist[self.left_child_idx(i)].f == self.newlist[self.right_child_idx(i)].f:
            if self.newlist[self.left_child_idx(i)].g >= self.newlist[self.right_child_idx(i)].g:
                return ((i + 1) << 1) - 1
            else:
                return (((i + 1) << 1) + 1) - 1
        else :
            return (((i + 1) << 1) + 1) - 1
    def initialHeap(self, olist):
        self.oldlist = olist
        self.newlist = []
        self.buildHeap(self.oldlist)
    def buildHeap(self, oldlist):
        """ Build a ordered list from a raw list"""
        for i in range(len(oldlist)):
            self.insert(self.oldlist[i])
        return self.newlist
    def validate(self):
        """ check Heap order's correctness"""
        # from top to bottom
        for i in range(len(self.newlist)):
            if not self.hasChildNode(i):
                # reach the bottom end
                break
            try: 
                self.newlist[self.right_child_idx(i)]
            except IndexError:
                root = min(self.newlist[i].f,self.newlist[self.left_child_idx(i)].f)
            else:
                root = min(self.newlist[i].f,self.newlist[self.left_child_idx(i)].f,\
                self.newlist[self.right_child_idx(i)].f)
            if root == self.newlist[i].f:
                continue
            if root == self.newlist[self.left_child_idx(i)].f:
                return False
            if root == self.newlist[self.right_child_idx(i)].f:
                return False
        return True
    def updateHeap(self, Type, *arg):
        """ Check Heap's order"""
        if Type=='down':
            if len(arg)==1:
                i = arg[0]
            else:
                i = 0
            # from top to bottom
            while self.hasChildNode(i):
                try: 
                    self.newlist[self.right_child_idx(i)]
                except IndexError:
                    if self.newlist[i].f>self.newlist[self.left_child_idx(i)].f:
                        self.newlist[i], self.newlist[self.left_child_idx(i)] = \
                        self.swap(self.newlist[i], self.newlist[self.left_child_idx(i)])
                        i = self.left_child_idx(i)
                        break
                    elif self.newlist[i].f==self.newlist[self.left_child_idx(i)].f:
                        # choose g
                        self.newlist[i], self.newlist[self.left_child_idx(i)] =\
                        self.gmax(self.newlist[i],self.newlist[self.left_child_idx(i)])
                        i = self.left_child_idx(i)
                        break
                    else:
                        i = self.left_child_idx(i)
                        break
                if self.newlist[i].f > self.newlist[self.right_child_idx(i)].f or \
                self.newlist[i].f > self.newlist[self.left_child_idx(i)].f:
                    self.newlist[i], self.newlist[self.min_child_idx(i)] = \
                    self.swap(self.newlist[i], self.newlist[self.min_child_idx(i)])
                    #i = self.min_child_idx(i)
                elif self.newlist[i].f == self.newlist[self.right_child_idx(i)].f and \
                self.newlist[i].f == self.newlist[self.left_child_idx(i)].f:
                    # choose g
                    self.newlist[i], self.newlist[self.min_child_idx(i)] = \
                    self.gmax(self.newlist[i],self.newlist[self.min_child_idx(i)])
                elif self.newlist[i].f == self.newlist[self.right_child_idx(i)].f:
                    self.newlist[i], self.newlist[self.right_child_idx(i)] = \
                    self.gmax(self.newlist[i],self.newlist[self.right_child_idx(i)])
                elif self.newlist[i].f == self.newlist[self.left_child_idx(i)].f:
                    self.newlist[i], self.newlist[self.left_child_idx(i)] = \
                    self.gmax(self.newlist[i],self.newlist[self.left_child_idx(i)])
                else: pass
                i = self.min_child_idx(i)
        if Type=='up':
            # from bottom to top
            if len(arg)==1:
                i = arg[0]
            else:
                i = len(self.newlist)-1
            while self.father_idx(i)>=0:
                if self.newlist[i].f<self.newlist[self.father_idx(i)].f:
                    self.newlist[i], self.newlist[self.father_idx(i)] = \
                    self.swap(self.newlist[i], self.newlist[self.father_idx(i)])
                elif self.newlist[i].f==self.newlist[self.father_idx(i)].f:
                    # choose g
                    self.newlist[self.father_idx(i)], self.newlist[i] =\
                    self.gmax(self.newlist[self.father_idx(i)],self.newlist[i])
                else: pass
                i = self.father_idx(i)
    def hasChildNode(self,i):
        """
        If current node has child node return true.

        @type i: int
        """
        if self.left_child_idx(i)>=len(self.newlist):
            return False
        return True
    def swap(self,a,b):
        a, b = b, a
        a.listidx, b.listidx = b.listidx, a.listidx
        return a,b
    def setRoot(self,value):
        """
        Root is the minimum value

        @type value: int
        """
        self.root = value
    def getRoot(self):
        return self.root
    def gmax(self,*args):
        # pick up node with larger g
        if len(args)==3:
            if args[0].g>=args[1].g and args[0].g>=args[2].g:
                return args[0]
            if args[1].g>=args[0].g and args[1].g>=args[2].g:
                return args[1]
            if args[2].g>=args[0].g and args[2].g>=args[1].g:
                return args[2]
        if len(args)==2:
            if args[0].g>=args[1].g:
                return args[0], args[1]
            if args[1].g>=args[0].g:
                args = list(args)
                args[0] , args[1] = args[1], args[0]
                args[0].listidx , args[1].listidx = args[1].listidx, args[0].listidx
                return args[0], args[1]
    def gmin(self,*args):
        if len(args)==2:
            if args[0].g<=args[1].g:
                return args[0], args[1]
            if args[1].g<=args[0].g:
                args = list(args)
                args[0] , args[1] = args[1], args[0]
                args[0].listidx , args[1].listidx = args[1].listidx, args[0].listidx
                return args[1], args[0]
#aa = Heap([11, 9, 10, 5, 6, 7, 8, 1, 2, 3, 4])
#aa.buildHeap(aa.oldlist)

