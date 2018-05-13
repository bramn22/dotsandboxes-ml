import math
import random
import numpy as np
import copy
import board_evaluator as eval
import time

class MCTS:

    def __init__(self, board, free_moves, player, timelimit):
        self.timelimit = timelimit - 0.03
        points = [0, 0]
        self.root = Node(None, board, free_moves, player, None, points)

    def start_timer(self):
        self.ask_time = time.time()

    def check_time(self):
        cur_time = time.time()
        return cur_time - self.ask_time < self.timelimit

    def update_root(self, moves_made, board, free_moves, player):
        root_created = False
        points = self.root.points
        for move_made in moves_made:
            if self.root.children:
                self.root = [x for x in self.root.children if x.move == move_made][0]
                points = self.root.points
            else:
                root_created = True
                eval.user_action(move_made, player, board, points)
        if root_created:
            self.root = Node(None, board, free_moves, player, None, points)

    def run(self, board, free_moves, player):
        self.start_timer()
        if not self.root.children:
            self.expansion(self.root)
        self.moves_playout = [move for move in free_moves]
        self.moves_playout_stats = [[0, 0] for _ in free_moves]

        while self.check_time():
            index = index+1
            selected = self.selection(self.root)
            child = self.expansion(selected)
            if child is not None:
                winning_player = self.simulation(child)
                self.backpropagation(child, winning_player)
            else:
                winning_player = np.argmax(selected.points) + 1
                self.backpropagation(selected, winning_player)
        max_child = max(self.root.children, key=lambda c: c.win_rate)

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
        moves_done = []
        while moves:
            move_idx = self.select_random_idx_from_list(moves)
            move = moves[move_idx]
            moves_done.append(move)
            # evaluate move using take_action (returns results , next player)
            next_player, _ = eval.user_action(move, next_player, board, points)
        #   take action on random move from moves
            del moves[move_idx]
        # calculate if won or not
        final_score = [sum(x) for x in zip(node.points, points)]
        #for index in range(0, len(node.points)):
        #    final_score.append(node.points[index] + points[index])

        winning_player = np.argmax(final_score)+1 # (argmax returns index of highest score) + 1 -> player
        for move in moves_done:
            node.update_playout_stats(move, winning_player,node.parent.next_player)


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
        self.moves_playout = [move for move in free_moves]
        self.moves_playout_stats = [[0, 0] for _ in free_moves]
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
                child_player, _ = eval.user_action(move, self.next_player, child_board, child_points)
                child_free_moves = copy.deepcopy(self.free_moves) # makes copy of list
                del child_free_moves[index]
                self.children.append(Node(self, child_board, child_free_moves, child_player, move, child_points))


    def uct(self):
        if self.visit_rate == 0:
            return float('inf')
        beta = math.sqrt(200/(3*self.parent.visit_rate + 200))
        stats = self.parent.moves_playout_stats[self.parent.moves_playout.index(self.move)]
        if stats[1] != 0:
            return (1-beta)*(self.win_rate/self.visit_rate) + beta*(stats[0]/stats[1]) + self.c * math.sqrt(math.log(self.parent.visit_rate)/self.visit_rate)
        else:
            return (self.win_rate / self.visit_rate) + self.c * math.sqrt(
                math.log(self.parent.visit_rate) / self.visit_rate)

    def __str__(self):
        return "Node: next_player-{}, wr-{}, vr-{}, free-moves-{}, move-{}, pointsmade-{}".format(self.next_player, self.win_rate, self.visit_rate, self.free_moves,self.move, self.points)


    def update_playout_stats(self, move, won,parent_nextplayer):
        if self.parent:
            if won == parent_nextplayer: #TODO check if certainly not a mistake
                self.moves_playout_stats[self.moves_playout.index(move)][0] += 1
            self.moves_playout_stats[self.moves_playout.index(move)][1] += 1
            self.parent.update_playout_stats(move, won, parent_nextplayer)
            #Part added
            if self.children:
                for child in self.children:
                    if move in child.free_moves:
                        if won == child.next_player:
                            child.moves_playout_stats[child.moves_playout.index(move)][1] += 1
                        child.moves_playout_stats[child.moves_playout.index(move)][1] += 1
            #End new part
        else:
            if won == parent_nextplayer: #TODO check if certainly not a mistake
                self.moves_playout_stats[self.moves_playout.index(move)][0] += 1
            self.moves_playout_stats[self.moves_playout.index(move)][1] += 1
            for child in self.children:
                if move in child.free_moves:
                    if won == child.next_player:
                        child.moves_playout_stats[child.moves_playout.index(move)][1] += 1
                    child.moves_playout_stats[child.moves_playout.index(move)][1] += 1