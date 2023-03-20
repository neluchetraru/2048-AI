from ai import Py2048AI
from logic import Py2048
import time
import copy
import sys

def score(game):
    sum = 0
    for row in game.board:
        for elem in row:
            sum += elem
    return sum


def printBoard(board):
    print('\tGame Board')
    print('----------------------------')
    for row in board:
        print(*row, sep='\t', end='\n')
    print('----------------------------')


def runGame(depth):
    #Depth = 3
    ai = Py2048AI(depth)
    #board size:4x4
    game = Py2048(4, 4)

    while not game.gameover:
        best_move, _ = ai.expectimax(game, 0, ai.depth,"weightMatrix")
        print('Best move: ', best_move)
        game.update_move(best_move)
        printBoard(game.board)
        game.add_tile()
        printBoard(game.board)
        print('Score: ', score(game))
        game.check_gameover()

    return score(game)

depth = int(sys.argv[1])
runGame(depth)
