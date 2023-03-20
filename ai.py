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

    def evaluate_sum(self, game):
        sum = 0
        for row in game.board:
            for elem in row:
                sum += elem
        return sum
    
    def evaluate_zero_tiles(self, game):
        zero_tiles = 0
        for row in game.board:
            zero_tiles += row.count(0)
        return zero_tiles  
    

    def evaluate_uniformity(self,game):
        tiles = {}
        same_tiles = 0
        for row in game.board:
            for elem in row:
                if elem in tiles:
                    tiles[elem] += 1
                else: 
                    tiles[elem] = 1

        same_tiles = sum(tiles.values()) 
        return same_tiles
    
    def evaluate_weight_matrix(self,game):
        weight_matrix_4_corners = [[100,25,25,100],
                                    [25,5,5,25],
                                    [25,5,5,25],
                                    [100,25,25,100]]
        
        weight_matrix_1_corner = [[100,50,25,14],
                                [25,14,7,3],
                                [14,7,3,2],
                                [7,3,2,1]]

        sum = 0

        for i in range(4):
            for j in range(4):
                if game.board[i][j] != 0:
                    sum += game.board[i][j] * weight_matrix_1_corner[i][j] 
        
        return sum
    
    def evaluate_mono(self,game):
        best = -1
        for i in range(4):
            current = 0
            for row in range(4):
                for col in range(3):
                    if game.board[row][col] >= game.board[row][col + 1]:
                        current += 1
            for col in range(4):
                for row in range(3):
                    if game.board[row][col] >= game.board[row + 1][col]:
                        current += 1
            if current > best:
                best = current
            # Rotate the board 90 degrees clockwise
            game.board = list(zip(*game.board[::-1]))
        return best

    def ZM(self, game):
        sum = self.evaluate_zero_tiles(game) + self.evaluate_mono(game) 
        return sum
    
    def ZS(self, game):
        sum = self.evaluate_zero_tiles(game) + self.evaluate_sum(game) 
        return sum

    def UZ(self, game):
        sum = self.evaluate_uniformity(game) + self.evaluate_zero_tiles(game) 
        return sum
    
    def WS(self,game):
        sum = self.evaluate_weight_matrix(game) + self.evaluate_sum(game) 
        return sum

    def WSZ(self,game):
        sum = self.evaluate_weight_matrix(game) + self.evaluate_sum(game) + self.evaluate_zero_tiles(game)
        return sum
    
    def WSZweight(self,game):
        sum = self.evaluate_weight_matrix(game)*0.5 + self.evaluate_sum(game)*0.1 + self.evaluate_zero_tiles(game)*0.4
        return sum

    def MW(self,game):
        sum = self.evaluate_mono(game) + self.evaluate_weight_matrix(game)
        return sum
    
    def ZMS(self,game):
        sum = self.evaluate_mono(game) + self.evaluate_weight_matrix(game) +self.evaluate_sum(game)
        return sum
    
    def WZ(self,game):
        sum = self.evaluate_weight_matrix(game) + self.evaluate_zero_tiles(game) 
        return sum

    def evaluate_all(self,game):
        sum = self.evaluate_mono(game) + self.evaluate_sum(game) + self.evaluate_uniformity(game) + self.evaluate_weight_matrix(game) + self.evaluate_zero_tiles(game)
        return sum

    def evaluate(self, game, eval_func):
        if eval_func == "sum":
            return self.evaluate_sum(game)
        elif eval_func == "zeroTile":
            return self.evaluate_zero_tiles(game)
        elif eval_func == "ZS":
             return self.ZS(game)
        elif eval_func == "weightMatrix":
             return self.evaluate_weight_matrix(game)
        elif eval_func == "uniform":
             return self.evaluate_uniformity(game)
        elif eval_func == "UZ":
             return self.UZ(game)
        elif eval_func == "mono":
             return self.evaluate_mono(game)
        elif eval_func == "WSZ":
             return self.WSZ(game) 
        elif eval_func == "MW":
             return self.MW(game)
        elif eval_func == "all":
             return self.evaluate_all(game)
        elif eval_func == "WS":
             return self.WS(game)
        elif eval_func == "ZM":
             return self.ZM(game)
        elif eval_func == "ZMS":
             return self.ZMS(game)
        elif eval_func == "WZ":
             return self.WZ(game)
        elif eval_func == "WSZweight":
             return self.WSZweight(game)
        else:
            raise ValueError('Evaluation function doesnt exist')

    def expectimax(self, game, player, depth, eval_func):
        if depth == 0:
            return (None, self.evaluate(game, eval_func))

        if player == 0:  # AI  - MAX
            max_score = -1
            best_move = random.choice(list(directions.values()))
            for direction in directions.values():
                new_game = copy.deepcopy(game)
                new_game.update_move(direction)
                if new_game.board != game.board:
                    _, score = self.expectimax(new_game, 1, depth - 1,eval_func)
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
                            new_game, 0, depth - 1,eval_func )
                        chance_2 += 0.9 * score
                        new_game.board[i][j] = 4
                        _, score = self.expectimax(
                            new_game, 0, depth - 1,eval_func)
                        chance_4 += 0.1 * score

            return (None, (chance_2 + chance_4)/no_0_tiles)
