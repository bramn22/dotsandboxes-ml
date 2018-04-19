import math
import random
import numpy as np
import copy
import board_evaluator as eval


class MCTS:

    def __init__(self):
        pass

    def run(self, board, free_moves, player):
        #player = 3 - player
        print(player)
        points = [0, 0]
        root = Node(None, board, free_moves, player, None, points) # opposite player just played the last move
        self.expansion(root)
        index = 0
        while index < 1000:
            index = index+1
            selected = self.selection(root)
            child = self.expansion(selected)
            if child is not None:
                winning_player = self.simulation(child)
                self.backpropagation(child, winning_player)
            else:
                winning_player = np.argmax(selected.points) + 1
                self.backpropagation(selected, winning_player)
        max_child = max(root.children, key=lambda c: c.win_rate)
        n = max_child
        print(n)
        print(n.points)
        while n.children:
            n = max(n.children, key=lambda c: c.win_rate)
            print(n)
            print(n.points)

        return max_child, max_child.win_rate/max_child.visit_rate # TODO add move to max_child


    def selection(self, root):
        #print("Start of selection.")
        # calculate all next available nodes
        node = root

        while node.children:
            node = max(node.children, key=lambda c: c.uct())
        #print("End of selection.")
        return node

    def expansion(self, node):
        #print("Start of expansion.")
        node.expand_children()
        if node.children:
            return self.select_random_child(node.children)
        else:
            return None
        #print("End of expansion.")

    def simulation(self, node):
        #print("Start of simulation.")
        # pick node with strategy
            #print(child)
        winning_player = self.random_playout(node)
        return winning_player
        #print("End of simulation.")

    def backpropagation(self, node, winning_player):
        #print("Start of backpropagation.")
        while node.parent is not None:
            node.visit_rate += 1
            if node.parent.next_player == winning_player: # maybe take parent next_player
                node.win_rate += 1
            node = node.parent
        node.visit_rate +=1
        if node.next_player == 3 - winning_player: # maybe take parent next_player
            node.win_rate += 1
        #print(node.children)
        #print("End of backpropagation.")

    def random_playout(self, node):
        moves = copy.deepcopy(node.free_moves)
        points = [0, 0]
        next_player = node.next_player
        board = copy.deepcopy(node.board)
        while moves:
            move_idx = self.select_random_idx_from_list(moves)
            move = moves[move_idx]
            # evaluate move using take_action (returns results , next player)
            next_player = eval.user_action(move, next_player, board, points)
        #   take action on random move from moves
            del moves[move_idx]
        # calculate if won or not
        final_score = [sum(x) for x in zip(node.points, points)]
        #for index in range(0, len(node.points)):
        #    final_score.append(node.points[index] + points[index])

        winning_player = np.argmax(final_score)+1 # (argmax returns index of highest score) + 1 -> player
        #print("Player: {} ".format(winning_player))
        return winning_player

    def select_random_child(self, nodes):
        return nodes[self.select_random_idx_from_list(nodes)]


    def select_random_idx_from_list(self, list):
        return random.randint(0, len(list) - 1)


class Node:
    win_rate = 0
    visit_rate = 0
    c = math.sqrt(2)

    def __init__(self, parent, board, free_moves, next_player, move, points):
        self.parent = parent
        self.board = board
        self.free_moves = free_moves
        self.children = []
        self.next_player = next_player
        self.points = points
        self.move = move

    def expand_children(self):
        # translate free moves to child nodes
        if not self.children: # if children is emtpy
            for index, move in enumerate(self.free_moves):
                #print(move)
                child_board = copy.deepcopy(self.board)
                child_points = copy.deepcopy(self.points)
                child_player = eval.user_action(move, self.next_player, child_board, child_points)
                child_free_moves = copy.deepcopy(self.free_moves) # makes copy of list
                del child_free_moves[index]
                self.children.append(Node(self, child_board, child_free_moves, child_player, move, child_points))


    def uct(self):
        if self.visit_rate == 0:
            return float('inf')
        return (self.win_rate/self.visit_rate) + self.c * math.sqrt(math.log(self.parent.visit_rate)/self.visit_rate)

    def __str__(self):
        return "Node: next_player-{}, wr-{}, vr-{}, free-moves-{}, move-{}, pointsmade-{}".format(self.next_player, self.win_rate, self.visit_rate, self.free_moves,self.move, self.points)

MCTS()