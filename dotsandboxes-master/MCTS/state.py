


class State(object):
    board =[]
    nr_of_visits=0


    def __init__(self,board):
        self.board=board

    def get_visits(self):
        return self.nr_of_visits

def makeBoard(board):
    state = State(board)
    return state
