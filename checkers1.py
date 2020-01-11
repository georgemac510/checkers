# import packages
import pygame

#initialize pieces
empty = 0
friendly = {'pawn': 1, 'king': 3}
enemy = {'pawn': 2, 'king': 4}

#initialize board size
rows = 8
columns = 8

# create board
def create_board():
    board = [[empty for column in range(columns)] for row in range(rows)]
    return board


#>>> board = [[0]*8 for i in range(8)]
#>>> print(board)
