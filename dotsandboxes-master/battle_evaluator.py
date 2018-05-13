

from dotsandboxesagent import DotsAndBoxesAgent as Random
from dotsandboxesagentMCTS import DotsAndBoxesAgent as MCTS
from dotsandboxesagentMCTS_chains import DotsAndBoxesAgent as Chains
from dotsandboxesagentMCTS_heavy_playout import DotsAndBoxesAgent as Heavy
from dotsandboxesagentMCTS_rule_based import DotsAndBoxesAgent as RuleBased

from dotsandboxesagentMCTS_rave2 import  DotsAndBoxesAgent as Rave2

from board_evaluator import user_action
import copy
import numpy as np
import logging
import time

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class BattleEvaluator:
    def __init__(self, agent1_class, agent2_class, nb_cols, nb_rows, timelimit):
        results = []
        #times = []
        for i in range(50):
            print("Game ", i)
            self.reset_game(agent1_class, agent2_class, nb_cols, nb_rows, timelimit)
            self.run()
            results.append(copy.copy(self.points))
            winners = [np.argmax(r) + 1 if r[0] != r[1] else 0 for r in results]
            print("3---Player 1: {}, Player 2: {}, Draw: {}".format(winners.count(1), winners.count(2), winners.count(0)))
            #times.append(self.agent1.mcts.timing)
        print(results)
        winners = [np.argmax(r)+1 if r[0]!=r[1] else 0 for r in results]
        print(winners)
        print("3---Player 1: {}, Player 2: {}, Draw: {}".format(winners.count(1), winners.count(2), winners.count(0)))
        #print("avg start times: ", np.mean(times))
    def reset_game(self, agent1_class, agent2_class, nb_cols, nb_rows, timelimit):
        self.cur_player = 1
        self.cur_ended = False
        self.points = [0, 0]
        self.agent1 = agent1_class(player=self.cur_player, nb_rows=nb_rows, nb_cols=nb_cols, timelimit=timelimit)
        self.agent2 = agent2_class(player=3-self.cur_player, nb_rows=nb_rows, nb_cols=nb_cols, timelimit=timelimit)

        rows = []
        for ri in range(nb_rows + 1):
            columns = []
            for ci in range(nb_cols + 1):
                columns.append({"v": 0, "h": 0})
            rows.append(columns)
        self.board = rows

    def run(self):
        while not self.cur_ended:
            if self.cur_player == 1:
                #ask_time = time.time()
                move = self.agent1.next_action()
                #recv_time = time.time()
                #diff_time = recv_time - ask_time
                #logger.info("Move received after (s): {}".format(diff_time))
                if move is not None:
                    r, c, o = move
                    self.agent1.register_action(r, c, o, self.cur_player)
                    self.agent2.register_action(r, c, o, self.cur_player)
                    self.cur_player, _ = user_action(move=(r, c, o), cur_player=self.cur_player, cells=self.board, points=self.points)
                else:
                    self.cur_ended = True
            elif self.cur_player == 2:
                #ask_time = time.time()
                move = self.agent2.next_action()
                #recv_time = time.time()
                #diff_time = recv_time - ask_time
                #self.p2_ex_times.append(diff_time)
                #logger.info("Move received after (s): {}".format(diff_time))
                if move is not None:
                    r, c, o = move
                    self.agent1.register_action(r, c, o, self.cur_player)
                    self.agent2.register_action(r, c, o, self.cur_player)
                    self.cur_player, _ = user_action(move=(r, c, o), cur_player=self.cur_player, cells=self.board, points=self.points)
                else:
                    self.cur_ended = True
        print("Game ended")
        print(self.points)



def main():
    #init board and agents
    nb_rows = 3
    nb_cols = 3
    timelimit = 0.5


    random_agent = RuleBased
    mcts_agent = Random


    BattleEvaluator(random_agent, mcts_agent, nb_rows, nb_cols, timelimit)

main()