
class Tree:
    root = None

    def addNode(self, n):
        if (self.root is None):
            self.root = n
        else:
            self.root.addNode(n)

    def addValue(self,index,val):
        n = Node(index,val)
        self.addNode(n)


    def traverse(self):
        l = []
        self.root.visit(l)
        return(l)

    def search(self, i):
        return(self.root.search(i))

class Node:
    index = None
    value = None
    left = None
    right = None

    def __init__(self, i, val):
        self.index = i
        self.value = val

    def addNode(self, n):
        if(n.index < self.index):
            if(self.left is None):
                self.left = n
            else:
                self.left.addNode(n)
        elif(n.index > self.index):
            if(self.right is None):
                self.right = n
            else:
                self.right.addNode(n)

    def visit(self, l):
        if(self.right is not None ):
             self.right.visit(l)
        l.append(self.value)
        if(self.left is not None):
             self.left.visit(l)

    def search(self,i):
        if(self.index == i):
            return(self.value)
        elif(i > self.index) and (self.right is not None ):
            return(self.right.search(i))
        elif(i < self.index) and (self.left is not None ):
            return(self.left.search(i))
        return None

"""
CodeExample:
# initializing new tree
tree = Tree()
# Adding new Node
n = Node(5, 5)
tree.addNode(n)
# Adding value for cleaner code
tree.addValue(7,7)

# Getting sorted list from binary tree. high to low
list = tree.traverse()
[7,5]

# Search the binary tree. Nonetype if nothing exists
search = tree.search(5)
5

"""
