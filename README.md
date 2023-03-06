# cs431-connectfour

# Options include:
#    -0      0-player (computer-v-computer)
#    -1      1-player (human-v-computer)
#    -2      2-player (human-v-human)
#    -c      use colors (RRGGBB,RRGGBB)
#    -f      use a non-standard AI file
#    -h      print this help
#    -l      set AI level (#,#)
#    -n      non-graphics mode

# Point value is positive if it favors the AI, and negative if it favors its opponent.
# If it contains at least one disc of each color, it cannot be used to win. It is worth 0.
# If it contains 4 discs of the same color, it is worth ±∞ (since one player has won).
# If it contains 3 discs of the same color (and 1 empty) it is worth ±100.
# If it contains 2 discs of the same color (and 2 empties) it is worth ±10.
# If it contains 1 disc (and 3 empties) it is worth ±1.