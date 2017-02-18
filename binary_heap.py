class Heap:
    """
    Remember to use validate() method to check order's correctness
    """
    def __init__(self,oldlist):
        '''
        node is a cell in maze, nodelist is a list of node,
        sort nodelist by node.f

        @type oldlist:nodelist
        '''
        # Heap root
        self.root = 0
        # Raw list
        self.oldlist = oldlist
        # Ordered heaplist
        self.newlist = []
    def insert(self, value):
        """
        Add element to the list end

        @type value: node
        """
        self.newlist.append(value)
        self.updateHeap('up')
    def pop(self):
        """ Delete root element"""
        a = self.newlist[0]
        self.newlist[0] = self.newlist[-1]
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
    def updateHeap(self, Type):
        """ Check Heap's order"""
        if Type=='down':
            # from top to bottom
            for i in range(len(self.newlist)):
                if not self.hasChildNode(i):
                    # reach the bottom end
                    break
                try: 
                    print self.newlist[self.right_child_idx(i)]
                except IndexError:
                    root = min(self.newlist[i].f,self.newlist[self.left_child_idx(i)].f)
                else:
                    root = min(self.newlist[i].f,self.newlist[self.left_child_idx(i)].f,\
                    self.newlist[self.right_child_idx(i)].f)
                if root == self.newlist[i].f:
                    continue
                if root == self.newlist[self.left_child_idx(i)].f:
                    self.newlist[i],self.newlist[self.left_child_idx(i)] = \
                    self.swap(self.newlist[i],self.newlist[self.left_child_idx(i)])
                    continue
                if root == self.newlist[self.right_child_idx(i)].f:
                    self.newlist[i],self.newlist[self.right_child_idx(i)] = \
                    self.swap(self.newlist[i],self.newlist[self.right_child_idx(i)])
        if Type=='up':
            # from bottom to top
            for i in range(len(self.newlist),-1,-1):
                if not self.hasChildNode(i):
                    continue
                try: 
                    # whether it only has left child
                    print self.newlist[self.right_child_idx(i)]
                except IndexError:
                    # compare root and left child only
                    root = min(self.newlist[i].f,self.newlist[self.left_child_idx(i)].f)
                else:
                    # compare heap
                    root = min(self.newlist[i].f,self.newlist[self.left_child_idx(i)].f,\
                    self.newlist[self.right_child_idx(i)].f)
                if root == self.newlist[i].f:
                    # heap has correct order
                    continue
                if root == self.newlist[self.left_child_idx(i)].f:
                    # swap left child and root
                    self.newlist[i],self.newlist[self.left_child_idx(i)] = \
                    self.swap(self.newlist[i],self.newlist[self.left_child_idx(i)])
                    continue
                if root == self.newlist[self.right_child_idx(i)].f:
                    # swap right child and root
                    self.newlist[i],self.newlist[self.right_child_idx(i)] = \
                    self.swap(self.newlist[i],self.newlist[self.right_child_idx(i)])
    def hasChildNode(self,i):
        """
        If current node has child node return true.

        @type i: int
        """
        if self.left_child_idx(i)>=len(self.newlist):
            return False
        return True
    def swap(self,a,b):
        return b,a
    def setRoot(self,value):
        """
        Root is the minimum value

        @type value: int
        """
        self.root = value
    def getRoot(self):
        return self.root

#aa = Heap([11, 9, 10, 5, 6, 7, 8, 1, 2, 3, 4])
#aa.buildHeap(aa.oldlist)

