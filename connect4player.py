"""
This Connect Four AI player is called by connect4.py
It uses the minimax algorithm to choose which moves to make
based on the difficulty level specified by the user on the 
command-line. The difficulty level of the AI represents how 
many plies the minimax algorithm will use
"""

__author__ = "Emilee Oquist"    # Received help from Lucas, Jared
__license__ = "MIT"
__date__ = "February 2023"

import sys
import random
import time
import math


class ComputerPlayer:
    # game mode
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


    def __init__(self, id, difficulty_level):
        """
        Constructor: Takes a difficulty level (plies) and a player ID
        :param player_id: int representing the player ID (either 1 or 2)
        :param difficulty_level: int representing the difficulty level (plies)
        """
        self.PLAYER_ID = id
        self.DIFFICULTY = difficulty_level
        self.BEST_MOVE = -1
        self.BEST_SCORE = self.NEGATIVE_INFINITY


    def pick_move(self, rack):
        """
        Returns an int indicating in which column to drop a disc.
        :param rack: 2D list representing the game board with the current state of discs
        :return: int representing the column number to drop a disc
        """
        self.BEST_MOVE = -1
        self.BEST_SCORE = self.NEGATIVE_INFINITY
        tuple_to_list_copy = [list(tuple) for tuple in rack]
        score = self._minimax(tuple_to_list_copy,
                              self.DIFFICULTY, self.PLAYER_ID)
        if rack[self.BEST_MOVE][-1] != 0:
            return self._get_next_move(self.BEST_MOVE)
        return self.BEST_MOVE


    def _minimax(self, rack, depth, player):
        """
        Recursively search for the best move to make using the minimax algorithm.
        :param rack: a 2d column-major array of the game state.
        :param depth: the current depth of the search tree.
        :param player: the ID of the current player.
        :return: A numeric score representing the quality of the current game state.
        """
        current_state_score = self._evaluate(rack)

        # terminal state
        if self._is_terminal_condition(depth, current_state_score):
            return current_state_score

        opponent_disc = self.PLAYER2_DISC
        if player == self.PLAYER2_DISC:
            opponent_disc = self.PLAYER1_DISC

        # maximizing player
        if player == self.PLAYER_ID:
            best_score = self.NEGATIVE_INFINITY
            for column in range(len(rack)):
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
        # minimizing player
        else:
            best_score = self.INFINITY
            for column in range(len(rack)):
                next_legal_move = self._get_next_move(rack, column)
                if next_legal_move == -1:
                    continue
                rack[column][next_legal_move] = player
                minimax_score = self._minimax(rack, depth - 1, opponent_disc)
                best_score = min(best_score, minimax_score)
                rack[column][next_legal_move] = self.EMPTY_SLOT

        return best_score


    def _evaluate_quartet(self, quartet):
        """
        Evaluate the quartet of slots given by _evaluate and return its score based on the discs within.
        :param quartet: a 1D list of 4 slots
        :return: the quartet's score.
        """
        opponent_disc = self.PLAYER2_DISC
        if self.PLAYER_ID == self.PLAYER2_DISC:
            opponent_disc = self.PLAYER1_DISC

        player_disc_count = quartet.count(self.PLAYER_ID)
        opponent_disc_count = quartet.count(opponent_disc)

        if (player_disc_count > 0) and (opponent_disc_count > 0):
            return self.NOTHING

        # Player disc scoring
        if player_disc_count == 4:
            return self.INFINITY
        if player_disc_count == 3:
            return self.CONNECT3
        if player_disc_count == 2:
            return self.CONNECT2
        if player_disc_count == 1:
            return self.SOLO_DISC
        # Opponent disc scoring
        if opponent_disc_count == 4:
            return self.NEGATIVE_INFINITY
        if opponent_disc_count == 3:
            return -self.CONNECT3
        if opponent_disc_count == 2:
            return -self.CONNECT2
        if opponent_disc_count == 1:
            return -self.SOLO_DISC

        return 0  # empty


    def _evaluate(self, rack):
        """
        Evaluate the given game rack.
        :param rack: a 2d column-major array of the game state.
        :return: the rack's score.
        """
        rows = len(rack[0])
        columns = len(rack)
        offset = self.CONNECT_WINDOW_LEN - 1
        score = 0

        for row in range(rows):  # avoiding multiple nested for-loops
            for col in range(columns):

                if (row + offset) < rows:  # vertical
                    vertical_quartet = [rack[col][row + index_offset]
                                        for index_offset in range(self.CONNECT_WINDOW_LEN)]
                    score += self._evaluate_quartet(vertical_quartet)

                    if (col + offset) < columns:  # up-right
                        upright_quartet = [rack[col + index_offset][row + index_offset]
                                           for index_offset in range(self.CONNECT_WINDOW_LEN)]
                        score += self._evaluate_quartet(upright_quartet)

                if (col + offset) < columns:  # horizontal
                    horizontal_quartet = [rack[col + index_offset][row]
                                          for index_offset in range(self.CONNECT_WINDOW_LEN)]
                    score += self._evaluate_quartet(horizontal_quartet)

                    if (row - offset) >= 0:  # down-right
                        downright_quartet = [rack[col + index_offset][row - index_offset]
                                             for index_offset in range(self.CONNECT_WINDOW_LEN)]
                        score += self._evaluate_quartet(downright_quartet)

        return score


    def _get_next_move(self, rack, column_index):
        """
        Get the next available column index to place a disc in.
        :param rack: a 2d column-major array of the game state.
        :param column_index: the index of the column to check.
        :return: the index of the next available row in the column, or -1 if the column is full.
        """
        for row in range(len(rack[column_index])):
            if rack[column_index][row] == 0:
                return row
        return -1


    def _is_terminal_condition(self, depth, score):
        """
        Determine if the current state of the game is a terminal state for minimax.
        :param depth: An integer representing the current depth of the search tree.
        :param score: A numeric score representing the quality of the current game state.
        :return: True if the current state is terminal, False otherwise.
        """
        if depth == 0:
            return True
        if score == self.INFINITY:
            return True
        if score == self.NEGATIVE_INFINITY:
            return True
        return False
