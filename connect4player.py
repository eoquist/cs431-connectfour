"""
How this Connect Four Player works:

"""
# Received help from Lucas, Jared
__author__ = "Emilee Oquist"
__license__ = "MIT"
__date__ = "February 2023"

import sys
import random
import time
import math

# Your job is to modify the ComputerPlayerclass in connect4player.py


class ComputerPlayer:
    PLAYER_ID = 1
    DIFFICULTY = 1
    CONNECT_WINDOW_LEN = 4
    # scoring
    INFINITY = float('inf')
    NEGATIVE_INFINITY = float('-inf')
    CONNECT3 = 100
    CONNECT2 = 10
    SOLO_DISC = 1
    NOTHING = 0
    # game piece representation
    EMPTY_SLOT = 0
    PLAYER1_DISC = 1
    PLAYER2_DISC = 2
    # playing
    BEST_MOVE = 0
    BEST_SCORE = 0

    # Constructor: Takes a difficulty level (plies) and a player ID
    def __init__(self, id, difficulty_level):
        self.PLAYER_ID = id
        self.DIFFICULTY = difficulty_level
        self.BEST_MOVE = -1
        self.BEST_SCORE = self.NEGATIVE_INFINITY

    # Returns an int indicating in which column to drop a disc.
    def pick_move(self, rack):
        tuple_to_list_copy = [list(tuple) for tuple in rack]
        score = self._minimax(tuple_to_list_copy, self.DIFFICULTY, self.PLAYER_ID)
        # print("best move " + str(self.BEST_MOVE))
        # print("best score " + str(self.BEST_SCORE))
        return self.BEST_MOVE

    
    def _minimax(self, rack, depth, player):
        current_state_score = self._evaluate(rack)
        # print("minimax current state score " + str(current_state_score))

        # terminal
        if depth == 0 or current_state_score == self.INFINITY or current_state_score == self.NEGATIVE_INFINITY: 
            # print("minimax depth 0 score")
            # print(current_state_score) 
            return current_state_score
        

        opponent_disc = self.PLAYER2_DISC
        if player == self.PLAYER2_DISC:
            opponent_disc = self.PLAYER1_DISC

        if player == self.PLAYER_ID:
            best_score = self.NEGATIVE_INFINITY
            for column in range(len(rack)):
                # if (rack[column][-1] != 0):
                #     continue # top of column full

                next_legal_move = self._get_next_move(rack, column)
                if next_legal_move == -1:
                    continue
                rack[column][next_legal_move] = player
                minimax_score = self._minimax(rack, depth - 1, opponent_disc)
                best_score = max(best_score, minimax_score)
                rack[column][next_legal_move] = self.EMPTY_SLOT
                if (depth == self.DIFFICULTY) and (best_score > self.BEST_SCORE):  
                    self.BEST_SCORE = best_score
                    self.BEST_MOVE = column 
        else:
            best_score = self.INFINITY
            for column in range(len(rack)):
                # if (rack[column][-1] != 0):
                #     continue # top of column full

                next_legal_move = self._get_next_move(rack, column)
                if next_legal_move == -1:
                    continue
                rack[column][next_legal_move] = player
                minimax_score = self._minimax(rack, depth - 1, opponent_disc)
                best_score = min(best_score, minimax_score)
                rack[column][next_legal_move] = self.EMPTY_SLOT
        
        # print("best_score")
        # print(best_score)
        # print("player is")
        print(player)
        return best_score

    def _evaluate_quartet(self, quartet):
        opponent_disc = self.PLAYER2_DISC
        if self.PLAYER_ID == self.PLAYER2_DISC:
            opponent_disc = self.PLAYER1_DISC

        player_disc_count = 0
        opponent_disc_count = 0

        for disc in quartet:
            if disc == self.PLAYER_ID:
                player_disc_count += 1
            elif disc != 0:
                opponent_disc_count += 1
        

        if (player_disc_count > 0) and (opponent_disc_count > 0):
            # print("both player have tokens in quartet")
            return self.NOTHING

        if player_disc_count == 4:
            # print("player win")
            return self.INFINITY
        if player_disc_count == 3 :
            # print("player 3")
            # return self.CONNECT3
            return 100
        if player_disc_count == 2:
            # print("player 2")
            # return self.CONNECT2
            return 10
        if player_disc_count == 1:
            # print("player 1")
            # return self.SOLO_DISC
            return 1
        if opponent_disc_count == 4:
            # print("opponent win")
            return self.NEGATIVE_INFINITY
        if opponent_disc_count == 3:
            # print("opponent 3")
            # return -self.CONNECT3
            return -100
        if opponent_disc_count == 2:
            # print("opponent 2")
            # return -self.CONNECT2
            return -10
        if opponent_disc_count == 1:
            # print("opponent 1")
            return -self.SOLO_DISC

        return 0 # empty

    def _evaluate(self, rack):
        rows = len(rack[0])
        columns = len(rack)
        offset = self.CONNECT_WINDOW_LEN - 1
        score = 0

        for row in range(rows):
            for col in range(columns):

                if (row + offset) < rows: # vertical
                    vertical_quartet = [rack[col][row + index_offset] for index_offset in range(self.CONNECT_WINDOW_LEN)]
                    score += self._evaluate_quartet(vertical_quartet)

                    if (col + offset) < columns: # up-right
                        upright_quartet = [rack[col + index_offset][row + index_offset] for index_offset in range(self.CONNECT_WINDOW_LEN)]
                        score += self._evaluate_quartet(upright_quartet)

                if (col + offset) < columns: # horizontal
                    horizontal_quartet = [rack[col + index_offset][row] for index_offset in range(self.CONNECT_WINDOW_LEN)]
                    score += self._evaluate_quartet(horizontal_quartet)

                    if (row - offset) >= 0: # down-right
                        downright_quartet = [rack[col + index_offset][row - index_offset] for index_offset in range(self.CONNECT_WINDOW_LEN)]
                        score += self._evaluate_quartet(downright_quartet)
        

        # for row in range(rows):
        #     for col in range(columns):
        #         quartet = [0,0,0,0]
        #         # print("[c"+str(col)+",r"+str(row)+"]")

        #         if (row + offset) < rows: # vertical
        #             for index_offset in range(self.CONNECT_WINDOW_LEN):
        #                 # print("[c"+str(col)+",r"+str(row + index_offset)+"]")
        #                 quartet[index_offset] = rack[col][row + index_offset]
        #             # temp = self._evaluate_quartet(quartet, self.PLAYER_ID)
        #             # print(quartet)
        #             # print(temp)
        #             score += self._evaluate_quartet(quartet, self.PLAYER_ID)
                    
        #             if (col + offset) < columns: # up-right
        #                 for index_offset in range(self.CONNECT_WINDOW_LEN):
        #                     quartet[index_offset] = rack[col + index_offset][row + index_offset]
        #                 # temp = self._evaluate_quartet(quartet, self.PLAYER_ID)
        #                 score += self._evaluate_quartet(quartet, self.PLAYER_ID)
                
        #         if (col + offset) < columns: # horizontal
        #             for index_offset in range(self.CONNECT_WINDOW_LEN):
        #                 quartet[index_offset] = rack[col + index_offset][row]
        #             # temp = self._evaluate_quartet(quartet, self.PLAYER_ID)
        #             score += self._evaluate_quartet(quartet, self.PLAYER_ID)

        #             if (row + offset) < rows: # down-right
        #                 for index_offset in range(self.CONNECT_WINDOW_LEN):
        #                     quartet[index_offset] = rack[col + index_offset][row - index_offset]
        #                 # temp = self._evaluate_quartet(quartet, self.PLAYER_ID)
        #                 # print(quartet)
        #                 # print(temp)
        #                 score += self._evaluate_quartet(quartet, self.PLAYER_ID)
        return score

    # get next open column
    def _get_next_move(self, rack, column_index):
        # for col in range(len(rack[column_index])):
        #     if rack[column_index][-1] == 0:
        #         return col
        # return -1

        for row in range(len(rack[column_index])):
            if rack[column_index][row] == 0:
                return row
        return -1

    def _is_full(self, rack):
        for column in range(len(rack)):
            if rack[column][-1] != 0:
                pass