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
        print("best move " + str(self.BEST_MOVE))

        # rand if -1 or col full
        return self.BEST_MOVE

    
    def _minimax(self, rack, depth, player):
        current_state_score = self._evaluate(rack)
        # print("minimax current state score " + str(current_state_score))

        # terminal
        if depth == 0:  
            return current_state_score
        
        if current_state_score == self.INFINITY:
            return self.INFINITY
        elif current_state_score == self.NEGATIVE_INFINITY:
            return self.NEGATIVE_INFINITY

        opponent_disc = self.PLAYER2_DISC
        if player == self.PLAYER2_DISC:
            opponent_disc = self.PLAYER1_DISC

        if player == self.PLAYER_ID:
            best_score = self.NEGATIVE_INFINITY
            for column in range(len(rack)):
                if (rack[column][-1] != 0):
                    continue # top of column full

                next_legal_move = self._get_next_move(rack, column)
                if next_legal_move == -1:
                    continue
                rack[column][next_legal_move] = self.PLAYER_ID
                minimax_score = self._minimax(rack, depth - 1, opponent_disc)
                print("minimax downright score " + str(minimax_score))
                best_score = max(best_score, minimax_score)
                if (depth == self.DIFFICULTY) and (best_score > self.BEST_SCORE):  
                    self.BEST_SCORE = best_score
                    self.BEST_MOVE = column
                rack[column][next_legal_move] = self.EMPTY_SLOT
        else:
            best_score = self.INFINITY
            for column in range(len(rack)):
                if (rack[column][-1] != 0):
                    continue # top of column full

                next_legal_move = self._get_next_move(rack, column)
                if next_legal_move == -1:
                    continue
                rack[column][next_legal_move] = opponent_disc
                minimax_score = self._minimax(rack, depth - 1, self.PLAYER_ID)
                best_score = min(best_score, minimax_score)
                rack[column][next_legal_move] = self.EMPTY_SLOT
        
        return best_score

    def _evaluate_quartet(self, quartet, player_disc):
        opponent_disc = self.PLAYER2_DISC
        if player_disc == self.PLAYER2_DISC:
            opponent_disc = self.PLAYER1_DISC

        player_disc_count = 0
        opponent_disc_count = 0
        empty_slot_count = 0

        for disc in quartet:
            if disc == player_disc:
                player_disc_count += 1
            elif disc == opponent_disc:
                opponent_disc_count += 1
            else:
                empty_slot_count += 1
        
        # player_disc_count = quartet.count(player_disc)
        # opponent_disc_count = quartet.count(opponent_disc)
        # empty_slot_count = quartet.count(self.EMPTY_SLOT)

        if (player_disc_count > 0) and (opponent_disc_count > 0):
            return self.NOTHING

        if player_disc_count == 4:
            return self.INFINITY
        elif player_disc_count == 3 and empty_slot_count == 1:
            return self.CONNECT3
        elif player_disc_count == 2 and empty_slot_count == 2:
            return self.CONNECT2
        elif player_disc_count == 1 and empty_slot_count == 3:
            return self.SOLO_DISC

        if opponent_disc_count == 4:
            return self.NEGATIVE_INFINITY
        elif opponent_disc_count == 3 and empty_slot_count == 1:
            return -self.CONNECT3
        elif opponent_disc_count == 2 and empty_slot_count == 2:
            return -self.CONNECT2
        elif opponent_disc_count == 1 and empty_slot_count == 3:
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
                    quartet = [rack[col][row], rack[col][row+1], rack[col][row+2], rack[col][row+3]]
                    temp = self._evaluate_quartet(quartet, self.PLAYER_ID)
                    # print(quartet)
                    # print(temp)
                    # score += temp
                    # score += self._evaluate_quartet(quartet, self.PLAYER_ID)
                    
                    if (col + offset) < columns: # up-right
                        quartet = [rack[col][row],rack[col+1][row+1], rack[col+2][row+2], rack[col+3][row+3]]
                        temp = self._evaluate_quartet(quartet, self.PLAYER_ID)
                        # print(quartet)
                        # print(temp)
                        # score += temp
                        # score += self._evaluate_quartet(quartet, self.PLAYER_ID)
                
                if (col + offset) < columns: # horizontal
                    quartet = [rack[col][row], rack[col+1][row], rack[col+2][row], rack[col+3][row]]
                    temp = self._evaluate_quartet(quartet, self.PLAYER_ID)
                    # print(quartet)
                    # print(temp)
                    # score += temp
                    # score += self._evaluate_quartet(quartet, self.PLAYER_ID)

                    if (row - offset) >= 0: # down-right
                        quartet = [rack[col][row+3],rack[col+1][row+2], rack[col+2][row+1], rack[col+3][row]]
                        temp = self._evaluate_quartet(quartet, self.PLAYER_ID)
                        print(quartet)
                        print(temp)
                        # score += temp
                        # score += self._evaluate_quartet(quartet, self.PLAYER_ID)
                        quartet = []
        return score

    # get next open column
    def _get_next_move(self, rack, column_index):
        for col in range(len(rack[column_index])):
            if rack[column_index][-1] == 0:
                return col
        return -1
