class Heap:
    def __init__(self,oldlist):
        # Heap root
        self.root = 0
        # Raw list
        self.oldlist = oldlist
        # Ordered heaplist
        self.newlist = []
    def insert(self, value):
        """
        Add element to the list end

        @type value: int
        """
        self.newlist.append(value)
        self.updateHeap()
    def pop(self):
        """ Delete root element"""
        a = self.newlist[0]
        self.newlist[0] = self.newlist[-1]
        self.newlist.pop()
        self.updateHeap()
        return a
    def left_child_idx(self, i):
        """ 
        Find left child index

        @type i : int
        """
        return ((i + 1) << 1) - 1
    def right_child_idx(self, i):
        """ 
        Find right child index

        @type i : int
        """
        return (((i + 1) << 1) + 1) - 1
    def buildHeap(self, oldlist):
        """ Build a ordered list from a raw list"""
        for i in range(len(oldlist)):
            self.insert(self.oldlist[i])
        return self.newlist
    def updateHeap(self):
        """ Check Heap's order"""
        for i in range(len(self.newlist)):
            if not self.hasChildNode(i):
                break
            try: 
                print self.newlist[self.right_child_idx(i)]
            except IndexError:
                root = min(self.newlist[i],self.newlist[self.left_child_idx(i)])
            else:
                root = min(self.newlist[i],self.newlist[self.left_child_idx(i)],self.newlist[self.right_child_idx(i)])

            if root == self.newlist[i]:
                pass
            if root == self.newlist[self.left_child_idx(i)]:
                #self.newlist[i], self.newlist[self.left_child_idx(i)] = self.newlist[self.left_child_idx(i)], self.newlist[i]
                self.newlist[i],self.newlist[self.left_child_idx(i)] = \
                self.swap(self.newlist[i],self.newlist[self.left_child_idx(i)])
                continue
            if root == self.newlist[self.right_child_idx(i)]:
                #self.newlist[i], self.newlist[self.right_child_idx(i)] = self.newlist[self.right_child_idx(i)], self.newlist[i]
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

aa = Heap([11, 9, 10, 5, 6, 7, 8, 1, 2, 3, 4])
aa.buildHeap(aa.oldlist)

