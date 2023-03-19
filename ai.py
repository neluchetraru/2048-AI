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

    def evaluate_zero_plus_sum(self, game):
        zero_tiles = 0
        sum = 0

        for row in game.board:
            zero_tiles += row.count(0)
        
        
        for row in game.board:
            for elem in row:
                sum += elem
        
        avg_eval = (zero_tiles + sum)/2
        return avg_eval
    
    def evaluate_uniformity(self,game):
        tiles = [0]*2049
        same_tiles = 0
        for row in game.board:
            for elem in row:
                tiles[elem] += 1
        
        same_tiles = sum(tiles)
        return same_tiles
       
    
    def evaluate_uniform_plus_zero(self,game):
        tiles = [0]*2049
        same_tiles = 0
        for row in game.board:
            for elem in row:
                tiles[elem] += 1
        
        same_tiles = sum(tiles)
        
        zero_tiles = 0
        for row in game.board:
            zero_tiles += row.count(0)
        
        total = same_tiles + zero_tiles
        return total

    def evaluate_weigh_matrix(self,game):
        weight_matrix1 = [[100,25,25,100],
                         [25,5,5,25],
                         [25,5,5,25],
                         [100,25,25,100]]
        
        weight_matrix2 = [[100,50,25,14],
                         [25,14,7,3],
                         [14,7,3,2],
                         [7,3,2,1]]

        sum = 0

        for i in range(4):
            for j in range(4):
                if game.board[i][j] != 0:
                    sum += game.board[i][j] * weight_matrix2[i][j] 
        
        return sum
    
    def row_monotonicity(self, game):
        count = 0
        for row in game.board:
            if sorted(row) == row or sorted(row, reverse=True) == row:
                count += 1
        return count
    
    def row_monotonicity2(self,game):
        best = -1
        for _ in range(4):
            current = 0
            # Check monotonicity in rows
            for row in range(4):
                for col in range(3):
                    if game.board[row][col] >= game.board[row][col + 1]:
                        current += 1
            # Check monotonicity in columns
            for col in range(4):
                for row in range(3):
                    if game.board[row][col] >= game.board[row + 1][col]:
                        current += 1
            if current > best:
                best = current
            # Rotate the board 90 degrees clockwise
            game.board = list(zip(*game.board[::-1]))
        return best

    def evaluate(self, game, eval_func):
        if eval_func == "sum":
            return self.evaluate_sum(game)
        elif eval_func == "zeroTile":
            return self.evaluate_zero_tiles(game)
        elif eval_func == "zeroPlusSum":
             return self.evaluate_zero_plus_sum(game)
        elif eval_func == "weightMatrix":
             return self.evaluate_weigh_matrix(game)
        elif eval_func == "uniform":
             return self.evaluate_uniformity(game)
        elif eval_func == "uniformZero":
             return self.evaluate_uniform_plus_zero(game)
        elif eval_func == "mono":
             return self.row_monotonicity2(game)
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
