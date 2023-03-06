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
        """
        # This will slow things down but I misunderstood things
        column_major = [[row[column] for row in rack] for column in range(len(rack[0]))]
        # If the rack is under a certain dimension size then there's nothing that can be done but it should still play 

        play, minimax_score = self._minimax(column_major, self.DIFFICULTY, self.PLAYER_ID)
        # play, minimax_score = self._minimax_alphabeta(column_major, self.DIFFICULTY, -self.INFINITY, self.INFINITY, self.PLAYER_ID)

        # WIP
        time.sleep(0.5)  # pause purely for effect--real AIs shouldn't do this
        while True:
            # play = random.randrange(0, len(rack))
            if column_major[play][-1] == 0:
                return play
            
        
    
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
    

    def _evaluate(self,board):
        rows = len(board)
        columns = len(board[0])
        score = 0
        column_choice = 0 # need to find best column

        def evaluate_quartet(self, quartet, player_disc):
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
    
        # print("_evaluate vertical")
        for row in range(rows - self.CONNECT_WINDOW_LEN + 1):
            for col in range(columns):
                window = []
                for index_offset in range(self.CONNECT_WINDOW_LEN):
                    window.append(board[row + index_offset][col])
                score += self._evaluate_quartet(window, self.PLAYER_ID)
                # if score +INFINTY then column_choice = col

        # print("_evaluate horizontal")
        for row in range(rows):
            for col in range(columns - self.CONNECT_WINDOW_LEN + 1):
                window = []
                for index_offset in range(self.CONNECT_WINDOW_LEN):
                    window.append(board[row][col + index_offset])
                score += self._evaluate_quartet(window, self.PLAYER_ID)
                # find col ?

        # print("_evaluate down-left diagonal") 
        for row in range(rows - self.CONNECT_WINDOW_LEN + 1):
            for col in range(columns - self.CONNECT_WINDOW_LEN + 1):
                window = []
                for index_offset in range(self.CONNECT_WINDOW_LEN):
                    window.append(board[row + index_offset][col  + index_offset])
                score += self._evaluate_quartet(window, self.PLAYER_ID)
                # find col ?

        # print("_evaluate up-right diagonal")
        for row in range(rows - self.CONNECT_WINDOW_LEN + 1):
            for col in range(columns - (self.CONNECT_WINDOW_LEN - 1)):
                window = []
                for index_offset in range(self.CONNECT_WINDOW_LEN):
                    window.append(board[row + index_offset][col  - index_offset])
                score += self._evaluate_quartet(window, self.PLAYER_ID)
                # find col ?


    def _minimax(self, board, depth, player):
        if depth == 0: # or is terminal
            return self._evaluate(board)
        legal_moves = self._get_legal_moves(board)

        if player == self.PLAYER_ID:
            best_value = -self.INFINITY
            column_choice = random.choice(legal_moves) # temporary random choice
            for column in legal_moves:
                board_copy = board.copy()
                new_state = self.pick_move(board_copy)
                value = self._minimax(new_state, depth - 1, self.PLAYER_ID)
                if best_value > value:
                    value = best_value
                    column_choice = column
            return column_choice, best_value
        else:
            best_value = self.INFINITY
            column_choice = random.choice(legal_moves) # temporary random choice
            for column in legal_moves:
                board_copy = board.copy()
                new_state = self.pick_move(board_copy)
                value = self._minimax(new_state, depth - 1, self.PLAYER_ID)
                if best_value < value:
                    value = best_value
                    column_choice = column
            return column_choice, best_value

    
    # return array of valid moves
    def _get_legal_moves(self,rack):
        legal_moves = []
        for column in range(len(rack)):
            if rack[column][-1] == 0:
                legal_moves.append(column)
        return legal_moves
    