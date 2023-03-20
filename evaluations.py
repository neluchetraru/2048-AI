from ai import Py2048AI
from logic import Py2048
import copy
import sys
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

def reached2048(game,win):
    
    for row in game.board:
        for elem in row:
            if elem == 2048:
                win = True
    return win


def test_evaluation(num_games,eval_func):

    ai = Py2048AI(3)
    
    
    scores = []
    win = False
    wins = 0

    for i in range(num_games):
        game = Py2048(4, 4)
        while not game.gameover:
            best_move,_ = ai.expectimax(game,0,ai.depth,eval_func)
            game.update_move(best_move)
            game.add_tile()
            printBoard(game.board)
            game.check_gameover()

        scores.append(score(game))
        wins +=  reached2048(game,win)
       
    
    print("Average score: ", sum(scores) / len(scores))
    print("Standard deviation: ", (statistics.stdev(scores)))
    print("Number of wins: ", wins)
    print(scores)


num_games = int(sys.argv[1])
eval_func = sys.argv[2]
test_evaluation(num_games,eval_func)

