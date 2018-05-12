import math
import random
import numpy as np
import copy
import board_evaluator_optimized as eval
import time

class MCTS:

    class Chain:

        def __init__(self):
            self.is_loop = False
            self.boxes = []
            self.edges = []

        def box_in_chain(self, box):
            return box in self.boxes

    def rule_based_move(self, board, boxes):
        chains = []

        for (i, j), box in np.ndenumerate(boxes):
            if box == 3:
                already_in_chain = False
                for chain in chains:
                    if chain.box_in_chain((i, j)):
                        already_in_chain = True
                        break
                if not already_in_chain:
                    chain = self.Chain()
                    _board = copy.deepcopy(board)
                    _boxes = copy.deepcopy(boxes)
                    self.follow_chain(_board, _boxes, (i, j), chain)
                    chains.append(chain)
        if len(chains) >= 1:
            print("chains found: ", len(chains))

        chains_list = [c for c in chains if not c.is_loop]
        loops_list = [c for c in chains if c.is_loop]
        not_stupid_move_0 = [c for c in chains_list if len(c.boxes) != 3]
        if not_stupid_move_0:
            return not_stupid_move_0[0].edges[0]
        not_stupid_move_1 = [c for c in loops_list if len(c.boxes) > 4]
        if not_stupid_move_1:
            return not_stupid_move_1[0].edges[0]
        if len(chains_list) > 0 and len(loops_list) > 0:
            return loops_list[0].edges[0]
        if len(loops_list) >= 2:
            return loops_list[0].edges[0]
        if len(chains_list) >= 2:
            return chains_list[0].edges[0]




    def follow_chain(self, board, boxes, start_pos, chain):
        # chain is automatically updated (pointer to list) and method returns whether chain is a loop or not.
        i, j = start_pos
        connecting_box = (-1, -1)
        connecting_edge = (-1, -1, -1)
        # check which edge is free (can only be 1)
        if board[i][j]['h'] == 0:
            connecting_box = (i-1, j)
            connecting_edge = (i, j, 'h')
        elif board[i][j]['v'] == 0:
            connecting_box = (i, j-1)
            connecting_edge = (i, j, 'v')
        elif board[i][j+1]['v'] == 0:
            connecting_box = (i, j+1)
            connecting_edge = (i, j+1, 'v')
        elif board[i+1][j]['h'] == 0:
            connecting_box = (i+1, j)
            connecting_edge = (i+1, j, 'h')

        chain.edges.append(connecting_edge)
        chain.boxes.append((i, j))

        # if connecting box is out of bounds
        if connecting_box[0] < 0 or connecting_box[0] >= boxes.shape[0] or connecting_box[1] < 0 or connecting_box[1] >= boxes.shape[1]:
            return
        # if connecting box has 2 edges
        elif boxes[connecting_box[0], connecting_box[1]] == 2:
            # close connecting edge
            board[connecting_edge[0]][connecting_edge[1]][connecting_edge[2]] = 1
            # rinse and repeat
            self.follow_chain(board, boxes, connecting_box, chain)
            return
        # if connecting box had 3 edges
        elif boxes[connecting_box[0], connecting_box[1]] == 3:
            # set loop boolean in chain
            chain.is_loop = True
            # stop chain (return)
            return
        # if connecting box has 0 or 1 edges
        else:
            # stop chain (return)
            return



    def __init__(self, board, free_moves, player, timelimit):
        _board = copy.deepcopy(board)
        self.timelimit = timelimit - 0.05
        nb_rows = np.shape(board)[0] - 1
        nb_cols = np.shape(board)[1] - 1
        self.boxes = np.zeros(shape=(nb_rows, nb_cols))
        points = [0, 0]
        self.root = Node(None, self.boxes, free_moves, player, None, points, False)

    def start_timer(self):
        self.ask_time = time.time()

    def check_time(self):
        cur_time = time.time()
        return cur_time - self.ask_time < self.timelimit

    def update_root(self, moves_made, free_moves, player):
        root_created = False
        points = self.root.points
        for move_made in moves_made:
            if self.root.children:
                self.root = [x for x in self.root.children if x.move == move_made][0]
                self.boxes = self.root.boxes
                points = self.root.points
            else:
                root_created = True
                eval.user_action(move_made, player, points, self.boxes)
        if root_created:
            self.root = Node(None, self.boxes, free_moves, player, None, points, False)

    def run(self, board, player):
        self.start_timer()
        #player = 3 - player
        print(player)
        rb_move = self.rule_based_move(board, self.boxes)

        if not self.root.children:
            self.expansion(self.root)

        while self.check_time():
            selected = self.selection(self.root)
            child = self.expansion(selected)
            if child is not None:
                winning_player = self.simulation(child)
                self.backpropagation(child, winning_player)
            else:
                winning_player = np.argmax(selected.points) + 1
                self.backpropagation(selected, winning_player)
        max_child = max(self.root.children, key=lambda c: c.win_rate)

        if rb_move is not None:
            return (Node(None, None, None, None, rb_move, None, None), -1)
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
        orig_node = node
        while node.parent is not None:
            node.visit_rate += 1
            if node.parent.next_player == winning_player: # maybe take parent next_player
                node.win_rate += 1 #+ 0.1*orig_node.points[winning_player]
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
        boxes = copy.deepcopy(node.boxes)
        while moves:
            #move_idx = self.select_random_idx_from_list(moves)
            #move = moves[move_idx]
            move_idx = self.select_with_chain_heuristic(moves, boxes)
            move = moves[move_idx]
            # evaluate move using take_action (returns results , next player)
            next_player, _ = eval.user_action(move, next_player, points, boxes)
        #   take action on random move from moves
            del moves[move_idx]
        # calculate if won or not
        final_score = [sum(x) for x in zip(node.points, points)]
        #for index in range(0, len(node.points)):
        #    final_score.append(node.points[index] + points[index])

        winning_player = np.argmax(final_score)+1 # (argmax returns index of highest score) + 1 -> player
        #print("Player: {} ".format(winning_player))
        return winning_player

    def select_with_chain_heuristic(self, moves, boxes):
        probs = np.empty(shape=len(moves))
        for i, move in enumerate(moves):
            _boxes = copy.deepcopy(boxes)
            boxes_closed = eval.check_boxes(move, _boxes)+1
            probs[i] = (boxes_closed*boxes_closed)

        probs = np.divide(probs, np.sum(probs))
        return np.random.choice(range(len(moves)), 1, p=probs)[0]

    def select_random_child(self, nodes):
        return nodes[self.select_random_idx_from_list(nodes)]


    def select_random_idx_from_list(self, list):
        return random.randint(0, len(list) - 1)


class Node:



    def __init__(self, parent, boxes, free_moves, next_player, move, points, closed_box):
        self.win_rate = 0
        self.visit_rate = 0
        self.c = math.sqrt(2)
        self.box_closed_in_move = False
        self.parent = parent
        self.boxes = boxes
        self.free_moves = free_moves
        self.children = []
        self.next_player = next_player
        self.points = points
        self.move = move
        self.box_closed_in_move = closed_box
        if self.box_closed_in_move:
            self.chain_length = 1
        else:
            self.chain_length = 0

    def expand_children(self):
        child_has_closed_box = False
        # translate free moves to child nodes
        if not self.children: # if children is emtpy
            for index, move in enumerate(self.free_moves):
                #print(move)
                child_boxes = copy.deepcopy(self.boxes)
                child_points = copy.deepcopy(self.points)
                child_player, closed_box = eval.user_action(move, self.next_player, child_points, child_boxes)
                if closed_box:
                    child_has_closed_box = True
                child_free_moves = copy.deepcopy(self.free_moves) # makes copy of list
                del child_free_moves[index]
                self.children.append(Node(self, child_boxes, child_free_moves, child_player, move, child_points, closed_box))
        if child_has_closed_box:
            self.update_chain_length()

    def update_chain_length(self):
        if self.box_closed_in_move:
            self.chain_length += 1
            if self.parent is not None:
                self.parent.update_chain_length()


    def uct(self):
        if self.visit_rate == 0:
            return float('inf')
        # (self.win_rate/self.visit_rate) + self.c * math.sqrt(math.log(self.parent.visit_rate)/self.visit_rate) +
        boxes_left = (np.shape(self.boxes)[0]) * (np.shape(self.boxes)[1]) - sum(self.points)
        beta = math.sqrt(100 / (3 * self.parent.visit_rate + 100)) #TODO : select param
        # return (self.win_rate/self.visit_rate) + self.c * math.sqrt(math.log(self.parent.visit_rate)/self.visit_rate) + self.chain_length
        #return self.chain_length / (boxes_left + 1) + 0.5 * (self.win_rate / self.visit_rate)
        return beta*(self.chain_length / (boxes_left + 1)) + (1-beta) * (self.win_rate / self.visit_rate)

    def __str__(self):
        return "Node: next_player-{}, wr-{}, vr-{}, move-{}, pointsmade-{}, chain_length-{}".format(self.next_player, self.win_rate, self.visit_rate, self.move, self.points, self.chain_length)
