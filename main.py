from ai import Py2048AI
from logic import Py2048
import time
import copy


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


def runGame():
    ai = Py2048AI(5)
    game = Py2048(4, 4)

    while not game.gameover:
        best_move, _ = ai.expectimax(game, 0, ai.depth)
        print('Best move: ', best_move)
        game.update_move(best_move)
        printBoard(game.board)
        game.add_tile()
        printBoard(game.board)
        game.check_gameover()

    return score(game)


runGame()
# def main():
#     filename = 'ExpectiMax_total_score_heuristic.csv'
#     with open(filename, 'w') as f:
#         f.write('iteration, score\n')

#     for i in range(100):
#         print('Iteration: ', i)
#         score = runGame()
#         with open(filename, 'a') as f:
#             f.write(str(i) + ', ' + str(score) + '\n')


# if __name__ == '__main__':
#     main()
