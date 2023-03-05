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

    def __init__(self, id, difficulty_level):
        """
        Constructor, takes a difficulty level (likely the # of plies to look
        ahead), and a player ID that's either 1 or 2 that tells the player what
        its number is.
        """
        pass

    def pick_move(self, rack):
        """
        Pick the move to make. It will be passed a rack with the current board
        layout, column-major. A 0 indicates no token is there, and 1 or 2
        indicate discs from the two players. Column 0 is on the left, and row 0 
        is on the bottom. It must return an int indicating in which column to 
        drop a disc. The player current just pauses for half a second (for 
        effect), and then chooses a random valid move.
        """

        """
        If the rack is under a certain dimension size then there's nothing that can be done but it should still play 

        Sliding window technique for 1x4, 4x1, and diagonal 4 up-right and diagonal 4 down-left
        """
        time.sleep(0.5)  # pause purely for effect--real AIs shouldn't do this
        while True:
            play = random.randrange(0, len(rack))
            if rack[play][-1] == 0:
                return play
    
    # Inspects windows of size 4 of diagonal elements from a 2D array.
    def sliding_window(self,board):
        rows = len(board)
        columns = len(board[0])
        quartet = []

        # vertical
        for row in range(rows - (rows - self.CONNECT_WINDOW_LEN) - 1):
            for col in range(columns):
                # gets the values not the coords
                window = []
                for index_offset in range(self.CONNECT_WINDOW_LEN):
                    window.append(board[row + index_offset][j])
                quartet.append(window)

        # horizontal
        for row in range(rows):
            for col in range(columns - (rows - self.CONNECT_WINDOW_LEN) - 1):
                # gets the values not the coords
                window = [board[row][col + index_offset] for index_offset in range(self.CONNECT_WINDOW_LEN)]
                quartet.append(window)

        # down-left diagonal
        for row in range(rows - self.CONNECT_WINDOW_LEN + 1):
            for col in range(columns - self.CONNECT_WINDOW_LEN + 1):
                # gets the values not the coords
                window = [board[row + index_offset][col + index_offset] for index_offset in range(self.CONNECT_WINDOW_LEN)]
                quartet.append(window)

        # up-right diagonal
        for row in range(rows - self.CONNECT_WINDOW_LEN + 1):
            for col in range(self.CONNECT_WINDOW_LEN - 1, columns):
                # gets the values not the coords
                window = [board[row + index_offset][col - index_offset] for index_offset in range(self.CONNECT_WINDOW_LEN)]
                quartet.append(window)
        
        print("quartets " + str(len(quartet)))
    
    def evaluate(self,board):
        # Point value is positive if it favors the AI, and negative if it favors its opponent.
        # If it contains at least one disc of each color, it cannot be used to win. It is worth 0.
        # If it contains 4 discs of the same color, it is worth ±∞ (since one player has won).
        # If it contains 3 discs of the same color (and 1 empty) it is worth ±100.
        # If it contains 2 discs of the same color (and 2 empties) it is worth ±10.
        # If it contains 1 disc (and 3 empties) it is worth ±1.
        pass

if __name__ == "__main__":
    board = [[i * 7 + j for j in range(7)] for i in range(6)]
    board_zip = list(zip(*board)) # transpose/splat
    col_widths = [max(len(str(element)) for element in col) for col in board_zip]

    # Print out each element, aligned by column
    print("=======================")
    print("BOARD")
    for row in board:
        for i, element in enumerate(row):
            print(str(element).ljust(col_widths[i]), end=' ')
        print()
    print("=======================")
    player = ComputerPlayer(1,1)
    player.sliding_window(board)

    # print(f"Arguments count: {len(sys.argv)}")
    # for i, arg in enumerate(sys.argv):
    #     print(f"Argument {i:>6}: {arg}")
