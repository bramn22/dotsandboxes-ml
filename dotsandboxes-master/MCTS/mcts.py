import math
import random
import numpy as np

import agent.MCTS.board_evaluator as eval

player=1
dimension =3

class MCTS:

    def __init__(self):
        root = Node(parent=None, free_moves=[1, 2, 3, 4, 5], player=1)
        print(root)
        node = self.selection(root)
        print(node)
        print(node.children)
        self.expansion(node)
        print(node.children)
        print(self.selection(node))
        # make initial state the root node

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
        # pick node with strategy
        child = self.select_random_child(node.children)
        self.random_playout(child)
        pass

    def backpropagation(self, node, winning_player):
        print("Start of backpropagation.")
        while node.parent is not None:
            node.visit_rate += 1
            if node.player == winning_player:
                node.win_rate += 1
            node = node.parent
        print("End of backpropagation.")

    def random_playout(self, node):
        moves = node.free_moves
        points = [0., 0.]
        while moves:
            move_idx = self.select_random_idx_from_list(moves)
            move = moves[move_idx]
            # evaluate move using take_action (returns results , next player)
            next_player = 1
        #   take action on random move from moves
            del moves[move_idx]
        # calculate if won or not
        # node.points + points -> decide winning_player
        winning_player = 1
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

    def __init__(self, parent, free_moves, player, closed_box):
        self.parent = parent
        self.free_moves = free_moves
        self.children = []
        self.player = player
        self.closed_box = closed_box

    def expand_children(self):
        # translate free moves to child nodes
        if not self.children: # if children is emtpy
            for index, _ in enumerate(self.free_moves):
                temp_free_moves = list(self.free_moves) # makes copy of list
                del temp_free_moves[index]
                if self.closed_box:
                    self.children.append(Node(self, temp_free_moves, self.player)) # if closed box -> give incremented points for current player
                else:
                    self.children.append(Node(self, temp_free_moves, (3 - self.player))) # give current points

    def uct(self):
        if self.visit_rate == 0:
            return float('inf')
        return (self.win_rate/self.visit_rate) + self.c * math.sqrt(math.log(self.parent.visit_rate)/self.visit_rate)

    def __str__(self):
        return "Node: player-{}, wr-{}, vr-{}, free-moves-{}".format(self.player, self.win_rate, self.visit_rate, self.free_moves)

MCTS()