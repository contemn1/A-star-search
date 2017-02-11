class Heap:
    def __init__(self,oldlist):
        self.root = 0
        self.leftChild = None
        self.rightChild = None
        self.currentSize = 0
        self.oldlist = oldlist
        self.newlist = []
    def insert(self,value):
        #add to the end
        self.newlist.append(value)
        self.updateHeap()
    def pop(self,newlist):
        a = newlist[0]
        newlist[0] = newlist[-1]
        newlist.pop()
        self.updateHeap()
        return a
    def left_child_idx(self, i):
        return ((i + 1) << 1) - 1
    def right_child_idx(self, i):
        return (((i + 1) << 1) + 1) - 1
    def buildHeap(self, oldlist):
        for i in range(len(oldlist)):
            self.insert(self.oldlist[i])
        return self.newlist
    def updateHeap(self):
        for i in range(len(self.newlist)):
            if not self.hasChildNode(self.newlist,i):
                break
            try: 
                print self.newlist[self.right_child_idx(i)]
            except IndexError:
                root = min(self.newlist[i],self.newlist[self.left_child_idx(i)])
            else:
                root = min(self.newlist[i],self.newlist[self.left_child_idx(i)],self.newlist[self.right_child_idx(i)])
            #if newlist[self.right_child_idx(i)]==None:
            #    root = min(newlist[i],newlist[self.left_child_idx(i)])
            #root = min(newlist[i],newlist[self.left_child_idx(i)],newlist[self.right_child_idx(i)])
            if root == self.newlist[i]:
                pass
            if root == self.newlist[self.left_child_idx(i)]:
                self.newlist[i], self.newlist[self.left_child_idx(i)] = self.newlist[self.left_child_idx(i)], self.newlist[i]
                continue
                #self.swap(newlist[i],newlist[self.left_child_idx(i)])
            if root == self.newlist[self.right_child_idx(i)]:
                self.newlist[i], self.newlist[self.right_child_idx(i)] = self.newlist[self.right_child_idx(i)], self.newlist[i]
                #self.swap(newlist[i],newlist[self.right_child_idx(i)])
    def hasChildNode(self,newlist,i):
        if self.left_child_idx(i)>=len(newlist):
            return False
        return True
    def swap(self,a,b):
        return b,a
    '''def LessOrEq(self,a,b):
        if a <= b:
            return True'''
    def setRoot(self,value):
        self.root = value
    def getRoot(self):
        return self.root

aa = Heap([11, 9, 10, 5, 6, 7, 8, 1, 2, 3, 4])
aa.buildHeap(aa.oldlist)
