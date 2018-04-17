
class Tree(object):
    root = None

    def __init__(self,root):
        self.root=root

    @root.setter
    def setroot(self, value):
        self.root = value

    @property
    def getroot(self):
        return self.root

    def addchild(self,parent,child):
        func = getattr(parent,"addchild")
        func(child)




def make_tree(root):
    tree = Tree(root)
    return tree