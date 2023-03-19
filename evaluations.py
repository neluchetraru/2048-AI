from ai import Py2048AI
from logic import Py2048
import copy
import statistics

def printBoard(board):

    print('\tGame Board')
    print('----------------------------')
    for row in board:
        print(*row, sep='\t', end='\n')
    print('----------------------------')

def score(game):
    sum = 0
    for row in game.board:
        for elem in row:
            sum += elem
    return sum

def test_evaluation(num_games):

    ai = Py2048AI(3)
    
    
    scores = []

    for i in range(num_games):
        game = Py2048(4, 4)
        while not game.gameover:
            best_move,_ = ai.expectimax(game,0,ai.depth)
            game.update_move(best_move)
            game.add_tile()
            printBoard(game.board)
            game.check_gameover()

        scores.append(score(game))
    return scores




scores = test_evaluation(10)
print("Average score: ", sum(scores) / len(scores))
print("Standard deviation: {}".format(statistics.stdev(scores)))
print(scores)