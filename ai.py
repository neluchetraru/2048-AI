import copy
import random
directions = {
    'UP': 2,
    'LEFT': 1,
    'DOWN': -2,
    'RIGHT': -1
}


class Py2048AI:
    def __init__(self, depth):
        self.depth = depth

    # def evaluate(self, game):
    #     sum = 0
    #     for row in game.board:
    #         for elem in row:
    #             sum += elem
    #     return sum
    
    def evaluate(self, game):
        zero_tiles = 0
        for row in game.board:
            zero_tiles += row.count(0)
        return zero_tiles
    
    # def evaluate(self, game):
    #     zero_tiles = 0
    #     sum = 0

    #     for row in game.board:
    #         zero_tiles += row.count(0)
        
        
    #     for row in game.board:
    #         for elem in row:
    #             sum += elem
        
    #     avg_eval = (zero_tiles + sum)/2
    #     return avg_eval

    # def evaluate(self,game):
    #     weight_matrix = [[8,4,4,8],
    #                      [4,3,3,4],
    #                      [4,3,3,4],
    #                      [8,4,4,8]]
    #     sum = 0

    #     for i in range(4):
    #         for j in range(4):
    #             if game.board[i][j] != 0:
    #                 corner_distance = game.board[i][j] * weight_matrix[i][j] 
    #             sum += corner_distance

    #     return sum

    def expectimax(self, game, player, depth):
        if depth == 0:
            return (None, self.evaluate(game))

        if player == 0:  # AI  - MAX
            max_score = -1
            best_move = random.choice(list(directions.values()))
            for direction in directions.values():
                new_game = copy.deepcopy(game)
                new_game.update_move(direction)
                if new_game.board != game.board:
                    _, score = self.expectimax(new_game, 1, depth - 1)
                    if score > max_score:
                        max_score = score
                        best_move = direction
            return best_move, max_score
        if player == 1:  # Player - Chance
            chance_2 = 0
            chance_4 = 0
            no_0_tiles = 0
            for i in range(4):
                for j in range(4):
                    if game.board[i][j] == 0:
                        no_0_tiles += 1
                        new_game = copy.deepcopy(game)
                        new_game.board[i][j] = 2
                        _, score = self.expectimax(
                            new_game, 0, depth - 1)
                        chance_2 += 0.9 * score
                        new_game.board[i][j] = 4
                        _, score = self.expectimax(
                            new_game, 0, depth - 1)
                        chance_4 += 0.1 * score

            return (None, (chance_2 + chance_4)/no_0_tiles)
