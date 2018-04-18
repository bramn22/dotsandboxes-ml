import math
import random
import numpy as np
import copy
import agent.MCTS.board_evaluator as eval

player=1
dimension =3

class MCTS:

    def __init__(self):
        player = 1
        board = [
            [{"v": 0, "h": 0}, {"v": 0, "h": 0}],
            [{"v": 0, "h": 0}, {"v": 0, "h": 0}]]
        free_moves = [(0, 0, "h"), (0, 0, "v"),
                     (0, 1, "v"),
                      (1, 0, "h")]
        points = [0, 0]
        root = Node(None, board, free_moves, player, points)
        index = 0
        while index < 500 :
            index= index+1
            root_=self.selection(root)
            self.expansion(root_)
            child, winingP =self.simulation(root_)
            self.backpropagation(child,winingP)


        print(root)
        for child in root.children:
            print(child)
        # root = Node(parent=None, free_moves=[1, 2, 3, 4, 5], player=1)
        # print(root)
        # node = self.selection(root)
        # print(node)
        # print(node.children)
        # self.expansion(node)
        # print(node.children)
        # print(self.selection(node))
        # make initial state the root node
        pass

    def selection(self, root):
        print("Start of selection.")
        # calculate all next available nodes
        node = root

        while node.children:
            node = max(node.children, key=lambda c: c.uct())
        print("End of selection.")
        return node

    def expansion(self, node):
        print("Start of expansion.")
        node.expand_children()
        print("End of expansion.")

    def simulation(self, node):
        print("Start of simulation.")
        # pick node with strategy
        if node.children:
            child = self.select_random_child(node.children)
            print(child)
            winning_player = self.random_playout(child)
            return child, winning_player
        winning_player = self.random_playout(node)
        print("End of simulation.")
        return node, winning_player

    def backpropagation(self, node, winning_player):
        print("Start of backpropagation.")
        while node.parent is not None:
            node.visit_rate += 1
            if node.player == winning_player:
                node.win_rate += 1
            node = node.parent
        node.visit_rate +=1
        if node.player == winning_player:
            node.win_rate += 1
        print(node.children)
        print("End of backpropagation.")

    def random_playout(self, node):
        moves = node.free_moves
        points = [0, 0]
        cur_player = node.player
        board = node.board
        while moves:
            move_idx = self.select_random_idx_from_list(moves)
            move = moves[move_idx]
            # evaluate move using take_action (returns results , next player)
            cur_player = eval.user_action(move, cur_player, board, points)
        #   take action on random move from moves
            del moves[move_idx]
        # calculate if won or not
        final_score=[]
        for index in range(0, len(node.points)):
            final_score.append(node.points[index] + points[index])
        #final_score = node.points + points
        winning_player = np.argmax(final_score)+1 # (argmax returns index of highest score) + 1 -> player
        print("Player: {} ".format(winning_player))
        return winning_player

    def select_random_child(self, nodes):
        return nodes[self.select_random_idx_from_list(nodes)]


    def select_random_idx_from_list(self, list):
        return random.randint(0, len(list) - 1)

    def take_action(self, player, move, board, free_moves, points):
        # evaluate move
        next_player = eval.user_action(move, player, board, points)
        pass


class Node:
    win_rate = 0
    visit_rate = 0
    c = math.sqrt(2)

    def __init__(self, parent, board, free_moves, player, points):
        self.parent = parent
        self.board = board
        self.free_moves = free_moves
        self.children = []
        self.player = player
        self.points = points

    def expand_children(self):
        # translate free moves to child nodes
        if not self.children: # if children is emtpy
            for index, move in enumerate(self.free_moves):
                print(move)
                child_board = copy.deepcopy(self.board)
                child_points = copy.deepcopy(self.points)
                child_player = eval.user_action(move, self.player, child_board, child_points)
                child_free_moves = copy.deepcopy(self.free_moves) # makes copy of list
                del child_free_moves[index]
                self.children.append(Node(self, child_board, child_free_moves, child_player, child_points))


    def uct(self):
        if self.visit_rate == 0:
            return float('inf')
        return (self.win_rate/self.visit_rate) + self.c * math.sqrt(math.log(self.parent.visit_rate)/self.visit_rate)

    def __str__(self):
        return "Node: player-{}, wr-{}, vr-{}, free-moves-{}".format(self.player, self.win_rate, self.visit_rate, self.free_moves)

MCTS()