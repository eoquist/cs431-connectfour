"""
How this Connect Four Player works:

"""
__author__ = "Emilee Oquist"
# __license__ = ""
__date__ = "February 2023"

import sys
import random
import time
import math

# Your job is to modify the ComputerPlayerclass in connect4player.py
class ComputerPlayer:
    CONNECT_WINDOW_LEN = 4
    PLAYER_ID = 0
    DIFFICULTY = 1
    # scoring
    INFINITY = math.inf
    CONNECT3 = 100
    CONNECT2 = 10
    SOLO_DISC = 1
    ENEMY_DISC = 0
    # game piece representation
    EMPTY_SLOT = 0
    PLAYER1_DISC = 1
    PLAYER2_DISC = 2

    # Constructor: Takes a difficulty level (plies) and a player ID
    def __init__(self, id, difficulty_level):
        self.PLAYER_ID = id
        self.DIFFICULTY = difficulty_level

    # Returns an int indicating in which column to drop a disc. 
    def pick_move(self, rack):
        """
        Rack is a tuple of tuples,column-major order. 0 indicates empty, 1 or 2 indicate player discs. 
        Column 0 is on the left, and row 0 is on the bottom. 

        If the rack is under a certain dimension size then there's nothing that can be done but it should still play 
        """
        column_major_copy = [[row[column] for row in rack] for column in range(len(rack[0]))] # RIP row-major order
        scores = []
        play = 0
        for row in range(len(column_major_copy)):
            if not (column_major_copy[row][-1] == 0):
                scores.append(None)
                continue
            for column in range(len(column_major_copy[0]), 0, -1):
                if column_major_copy[row][column] == self.EMPTY_SLOT:
                    column_major_copy[row][column] = self.PLAYER_ID
                    minimax_score = self._minimax(column_major_copy, self.DIFFICULTY, self.PLAYER_ID)
                    scores.append(minimax_score)
                    column_major_copy[row][column] = self.EMPTY_SLOT
                else:
                    scores.append(None)

        play = column_major_copy.index(max(scores))
        return play

        # while True:
        #     # play = random.randrange(0, len(rack))
        #     if column_major_copy[play][-1] == 0:
        #         return play
            
        
    # Inspects windows of size 4 of diagonal elements from a 2D array.
    def _sliding_window(self,board):
        # gets the values not the coords
        rows = len(board)
        columns = len(board[0])
        quartet = []

        # print("vertical")
        for row in range(rows - self.CONNECT_WINDOW_LEN + 1):
            for col in range(columns):
                window = []
                for index_offset in range(self.CONNECT_WINDOW_LEN):
                    window.append(board[row + index_offset][col])
                # print(window)
                # window.count()
                quartet.append(window)

        # print("horizontal")
        for row in range(rows):
            for col in range(columns - self.CONNECT_WINDOW_LEN + 1):
                window = []
                for index_offset in range(self.CONNECT_WINDOW_LEN):
                    window.append(board[row][col + index_offset])
                # print(window)
                quartet.append(window)

        # print("down-left diagonal") 
        for row in range(rows - self.CONNECT_WINDOW_LEN + 1):
            for col in range(columns - self.CONNECT_WINDOW_LEN + 1):
                window = []
                for index_offset in range(self.CONNECT_WINDOW_LEN):
                    window.append(board[row + index_offset][col  + index_offset])
                # print(window)
                quartet.append(window)

        # print("up-right diagonal")
        for row in range(rows - self.CONNECT_WINDOW_LEN + 1):
            for col in range(columns - (self.CONNECT_WINDOW_LEN - 1)):
                window = []
                for index_offset in range(self.CONNECT_WINDOW_LEN):
                    window.append(board[row + index_offset][col  - index_offset])
                # print(window)
                quartet.append(window)
        
        return quartet
    

    def evaluate_quartet(self, quartet, player_disc):
        score = 0
        opponent_disc = self.PLAYER2_DISC
        if player_disc == self.PLAYER2_DISC:
            opponent_disc = self.PLAYER1_DISC

        player_disc_count = quartet.count(player_disc)
        opponent_disc_count = quartet.count(opponent_disc)
        empty_slot_count = quartet.count(self.EMPTY_SLOT)

        if player_disc_count == 4:
            score += self.INFINITY
        elif player_disc_count == 3 and empty_slot_count == 1:
            score += self.CONNECT3
        elif player_disc_count == 2 and empty_slot_count == 2:
            score += self.CONNECT2
        elif player_disc_count == 1 and empty_slot_count == 3:
            score += self.SOLO_DISC

        if opponent_disc_count == 4:
            score -= self.INFINITY
        elif opponent_disc_count == 3 and empty_slot_count == 1:
            score -= self.CONNECT3
        elif opponent_disc_count == 2 and empty_slot_count == 2:
            score -= self.CONNECT2
        elif opponent_disc_count == 1 and empty_slot_count == 3:
            score -= self.SOLO_DISC

        return score
    
    def _evaluate(self,board):
        rows = len(board)
        columns = len(board[0])
        score = 0
    
        # print("_evaluate vertical")
        for row in range(rows - self.CONNECT_WINDOW_LEN + 1):
            for col in range(columns):
                window = []
                for index_offset in range(self.CONNECT_WINDOW_LEN):
                    window.append(board[row + index_offset][col])
                score += self._evaluate_quartet(window, self.PLAYER_ID)

        # print("_evaluate horizontal")
        for row in range(rows):
            for col in range(columns - self.CONNECT_WINDOW_LEN + 1):
                window = []
                for index_offset in range(self.CONNECT_WINDOW_LEN):
                    window.append(board[row][col + index_offset])
                score += self._evaluate_quartet(window, self.PLAYER_ID)

        # print("_evaluate down-left diagonal") 
        for row in range(rows - self.CONNECT_WINDOW_LEN + 1):
            for col in range(columns - self.CONNECT_WINDOW_LEN + 1):
                window = []
                for index_offset in range(self.CONNECT_WINDOW_LEN):
                    window.append(board[row + index_offset][col  + index_offset])
                score += self._evaluate_quartet(window, self.PLAYER_ID)

        # print("_evaluate up-right diagonal")
        for row in range(rows - self.CONNECT_WINDOW_LEN + 1):
            for col in range(columns - (self.CONNECT_WINDOW_LEN - 1)):
                window = []
                for index_offset in range(self.CONNECT_WINDOW_LEN):
                    window.append(board[row + index_offset][col  - index_offset])
                score += self._evaluate_quartet(window, self.PLAYER_ID)

        return score


    def _minimax(self, board, depth, player):
        current_state_score = self._evaluate(board)
        legal_moves = self._get_legal_moves(board)
        column_choice = random.choice(legal_moves) # temporary random choice

        if depth == 0: # or is terminal
            return current_state_score

        if player == self.PLAYER_ID:
            best_value = -self.INFINITY
            for column in legal_moves:
                board_copy = board.copy()
                new_state = self.pick_move(board_copy)
                value = self._minimax(new_state, depth - 1, self.PLAYER_ID)
                if best_value > value[1]:
                    value = best_value
                    column_choice = column
            return column_choice, best_value
        else:
            best_value = self.INFINITY
            for column in legal_moves:
                board_copy = board.copy()
                new_state = self.pick_move(board_copy)
                value = self._minimax(new_state, depth - 1, self.PLAYER_ID)
                if best_value < value[1]:
                    value[1] = best_value
                    column_choice = column
            return column_choice, best_value

    
    # return array of valid moves
    def _get_legal_moves(self,rack):
        legal_moves = []
        for column in range(len(rack)):
            if rack[column][-1] == 0:
                legal_moves.append(column)
        return legal_moves
    