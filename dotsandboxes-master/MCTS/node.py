import math


class Node(object):
    state=None
    parent=None
    childNodes=[]

    def __init__(self,state,parent,childNodes):
        self.state=state
        self.parent=parent
        self.childNodes=childNodes


    #Still needs to return the max value using UCT
    @property
    def childNodes(self):
        return self.childNodes
    @property
    def get_state(self):
        return self.state



    @property
    def getparent(self):
        return self.parent

    def addchild(self,node):
        self.childNodes.add(node)

    def findBestWithUCT(self):
        f_nr_visits = getattr(self.state,"get_visits")
        parent_visits = f_nr_visits()
        t_list=[]
        for i in self.childNodes:
            t_list.append(self.uct_value(parent_visits, i))
        return max(t_list)

    def uct_value(parentvisit,node):
        f_win_score= getattr(node, "get_wins")
        win_score = f_win_score()
        f_child_state = getattr(node,"get_state")
        child_state = f_child_state()
        f_child_state_visits = getattr(child_state,"get_visits")
        nr_of_visits = f_child_state_visits()
        if(nr_of_visits==0):
            #as sys.maxsize() doesnt work
            nr_of_visits= 999999
        return (win_score/ nr_of_visits) + 1.41* math.sqrt(math.log(parentvisit)/nr_of_visits)




def make_Node(state, parent ,childNodes):
    node = Node(state,parent,childNodes)
    return node


