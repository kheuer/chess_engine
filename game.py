import numpy as np
import chess
import cProfile
import pstats


class Piece:
    def __init__(self, name, color, value):
        self.name = name
        self.value = value
        self.color = color

    def __repr__(self):
        return self.color + " " + self.name



def min_or(lst, val):
    if lst:
        return min(lst)
    else:
        return val

def max_or(lst, val):
    if lst:
        return max(lst)
    else:
        return val

def min_index_or_None(lst):
    if lst:
        return lst.index(min(lst))
    else:
        return None

def max_index_or_None(lst):
    if lst:
        return lst.index(max(lst))
    else:
        return None


colors = {True: "White", False: "Black"}
piece_values = {1: 9, 2: 30, 3: 30, 4: 50, 5: 100, 6: 10000}

positional_scaling_factor = 5
piece_square_tables = {True:
                           {6: positional_scaling_factor * [2, 3, 1, 0, 0, 1, 3, 2, 2, 2, 0, 0, 0, 0, 2, 2, -1, -2, -2, -2, -2, -2, -2, -1, -2, -3, -3, -4, -4, -3, -3, -2, -3, -3, -4, -5, -5, -4, -4, -3, -3, -3, -4, -5, -5, -4, -4, -3, -3, -3, -4, -5, -5, -4, -4, -3, -3, -3, -4, -5, -5, -4, -4, -3],
                            5: positional_scaling_factor * [-2, -1, -1, -0.5, -0.5, -1, -1, 2, -1, 0, 0.5, 0, 0, 0, 0, -1, -1, 0.5, 0.5, 0.5, 0.5, 0.5, 0, -1, 0, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5, -0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5, -1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1, -1, 0, 0, 0, 0, 0, 0, -1, -2, -1, -1, -0.5, -0.5, -1, -1, -2],
                            4: positional_scaling_factor * [0, 0, 0, 0.5, 0.5, 0, 0, 0, -0.5, 0, 0, 0, 0, 0, 0, -0.5, -0.5, 0, 0, 0, 0, 0, 0, -0.5, -0.5, 0, 0, 0, 0, 0, 0, -0.5, -0.5, 0, 0, 0, 0, 0, 0, -0.5, -0.5, 0, 0, 0, 0, 0, 0, -0.5, 0.5, 1, 1, 1, 1, 1, 1, 0.5, 0, 0, 0, 0, 0, 0, 0, 0],
                            3: positional_scaling_factor * [-2, -1, -1, -1, -1, -1, -1, -2, -1, 0.5, 0, 0, 0, 0, 0.5, -1, -1, 1, 1, 1, 1, 1, 1, -1, -1, 0, 1, 1, 1, 1, 0, -1, -1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1, -1, 0, 0.5, 1, 1, 0.5, 0, -1, -1, 0, 0, 0, 0, 0, 0, -1, -2, -1, -1, -1, -1, -1, -1, -2],
                            2: positional_scaling_factor * [-5, -4, -3, -3, -3, -3, -4, -5, -4, -2, 0, 0.5, 0.5, 0, -2, -4, -3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3, -3, 0, 1.5, 2, 2, 1.5, 0, -3, -3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3, -3, 0, 1, 1.5, 1.5, 1, 0, -3, -4, -2, 0, 0, 0, 0, -2, -4, -5, -4, -3, -3, -3, -3, -4, -5],
                            1: positional_scaling_factor * [0, 0, 0, 0, 0, 0, 0, 0, 0.5, 1, 1, -2, -2, 1, 1, 0.5, 0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5, 0, 0, 0, 2, 2, 0, 0, 0, 0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5, 1, 1, 2, 3, 3, 2, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0],
                            },
                       False:
                           {6: positional_scaling_factor * [-3, -4, -4, -5, -5, -4, -3, -3, -3, -4, -4, -5, -5, -4, -3, -3, -3, -4, -4, -5, -5, -4, -3, -3, -3, -4, -4, -5, -5, -4, -3, -3, -2, -3, -3, -4, -4, -3, -3, -2, -1, -2, -2, -2, -2, -2, -2, -1, 2,  2,  0,  0,  0,  0,  2,  2, 2,  3,  1,  0,  0,  1,  3,  2],
                            5: positional_scaling_factor * [-2, -1, -1. , -0.5, -0.5, -1. , -1. , -2. , -1. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. , -1. , -1. ,  0. ,  0.5,  0.5,  0.5,  0.5,  0. , -1. , -0.5,  0. ,  0.5,  0.5,  0.5,  0.5,  0. , -0.5, -0.5,  0. ,  0.5,  0.5,  0.5,  0.5,  0. ,  0. , -1. ,  0. ,  0.5,  0.5,  0.5,  0.5,  0.5, -1. , -1. ,  0. ,  0. ,  0. ,  0. ,  0.5,  0. , -1. , 2. , -1. , -1. , -0.5, -0.5, -1. , -1. , -2.],
                            4: positional_scaling_factor * [0,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. , 0.5,  1. ,  1. ,  1. ,  1. ,  1. ,  1. ,  0.5, -0.5,  0. ,  0. ,  0. ,  0. ,  0. ,  0. , -0.5, -0.5,  0. ,  0. ,  0. ,  0. ,  0. ,  0. , -0.5,-0.5,  0. ,  0. ,  0. ,  0. ,  0. ,  0. , -0.5,-0.5,  0. ,  0. ,  0. ,  0. ,  0. ,  0. , -0.5,-0.5,  0. ,  0. ,  0. ,  0. ,  0. ,  0. , -0.5,0. ,  0. ,  0. ,  0.5,  0.5,  0. ,  0. ,  0.],
                            3: positional_scaling_factor * [-2, -1. , -1. , -1. , -1. , -1. , -1. , -2. ,-1. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. , -1. ,-1. ,  0. ,  0.5,  1. ,  1. ,  0.5,  0. , -1. ,-1. ,  0.5,  0.5,  1. ,  1. ,  0.5,  0.5, -1. ,-1. ,  0. ,  1. ,  1. ,  1. ,  1. ,  0. , -1. ,-1. ,  1. ,  1. ,  1. ,  1. ,  1. ,  1. , -1. ,-1. ,  0.5,  0. ,  0. ,  0. ,  0. ,  0.5, -1. ,-2. , -1. , -1. , -1. , -1. , -1. , -1. , -2.],
                            2: positional_scaling_factor * [-5. , -4. , -3. , -3. , -3. , -3. , -4. , -0.5,-4. , -2. ,  0. ,  0. ,  0. ,  0. , -2. , -4. ,-3. ,  0. ,  1. ,  1.5,  1.5,  1. ,  0. , -3. ,-3. ,  0.5,  1.5,  2. ,  2. ,  1.5,  0.5, -3. ,-3. ,  0. ,  1.5,  2. ,  2. ,  1.5,  0. , -3. ,-3. ,  0.5,  1. ,  1.5,  1.5,  1. ,  0.5, -3. ,-4. , -2. ,  0. ,  0.5,  0.5,  0. , -2. , -4. ,-5. , -4. , -3. , -3. , -3. , -3. , -4. , -5.],
                            1: positional_scaling_factor * [0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0.0,5. ,  5. ,  5. ,  5. ,  5. ,  5. ,  5. ,  5. ,1. ,  1. ,  2. ,  3. ,  3. ,  2. ,  1. ,  1. ,0.5,  0.5,  1. ,  2.5,  2.5,  1. ,  0.5,  0.5, 0. ,  0. ,  0. ,  2. ,  2. ,  0. ,  0. ,  0. , 0.5, -0.5, -1. ,  0. ,  0. , -1. , -0.5,  0.5, -5. ,  1. ,  1. , -2. , -2. ,  1. ,  1. ,  0.5, 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0.],
                            }
                       }


class Game:
    def __init__(self):
        self.board = chess.Board()
        #self.board = chess.Board("8/3r4/p2r4/1p1p2k1/1P6/P3P3/2R1K3/3R4 b - - 0 31")
        #self.board.push(chess.Move.null())

    def square_number_to_coords(self, square_number):
        return 7-chess.square_rank(square_number), chess.square_file(square_number)

    def coords_to_square_number(self, row, col):
        return 8 * (7-row) + col

    def get_moves_for_field(self, origin):
        possible_moves = []
        possible_coordinates = []
        for possible_move in self.board.legal_moves:
            if self.square_number_to_coords(possible_move.from_square) == origin:
                possible_moves.append(possible_move)
                possible_coordinates.append(self.square_number_to_coords(possible_move.to_square))
        return possible_moves, possible_coordinates

    def get_best_move(self, method="auto", log=True):
        if method == "auto":
            pieces_left = 0
            for i in range(64):
                if self.board.piece_at(i):
                    pieces_left += 1
            if pieces_left < 4:
                method = "min_max_6.5"
            elif pieces_left < 7:
                method = "min_max_5.5"
            else:
                method = "min_max_4.5"
        if log:
            print(f"   finding best move for {colors[self.board.turn]} with method: {method}")

        all_moves = self.get_moves()
        best_move_index = None
        if not all_moves:
            if self.board.is_game_over():
                return None
            else:
                print("weird bug, no options but not game over")
                return None
        own_color = self.board.turn

        if method == "random":
            best_move_index = np.random.choice(len(all_moves))
        elif method == "terrible_player":
            if np.random.random() < 0.35:
                return self.get_best_move("random", False)
            else:
                return self.get_best_move("min_max_3.5", False)

        elif method == "min_max_2":
            fitnesses = []
            for possible_move_1 in all_moves:   # home move
                fitnesses_1 = [1000000]
                self.board.push(possible_move_1)
                for possible_move_2 in self.board.legal_moves:      # enemy move
                    self.board.push(possible_move_2)
                    fitnesses_1.append(self.get_fitness(own_color))
                    self.board.pop()
                self.board.pop()
                fitnesses.append(min(fitnesses_1))
            best_move_index = max_index_or_None(fitnesses)
        elif method == "weakest":
            fitnesses = []
            for possible_move_1 in all_moves:       # home move
                fitnesses_1 = [1000000]
                self.board.push(possible_move_1)
                for possible_move_2 in self.board.legal_moves:      # enemy move
                    self.board.push(possible_move_2)
                    fitnesses_1.append(self.get_fitness(own_color))
                    self.board.pop()
                self.board.pop()
                fitnesses.append(min(fitnesses_1))
            best_move_index = min_index_or_None(fitnesses)

        elif method == "min_max_3":
            fitnesses_0 = []
            for possible_move_1 in all_moves:   # home move
                fitnesses_1 = [1000000]
                self.board.push(possible_move_1)
                for possible_move_2 in self.board.legal_moves:      # enemy move
                    fitnesses_2 = [-1000000]
                    self.board.push(possible_move_2)
                    for possible_move_3 in self.board.legal_moves:      # home move
                        self.board.push(possible_move_3)
                        fitness = self.get_fitness(own_color)
                        fitnesses_2.append(fitness)
                        self.board.pop()
                    fitnesses_1.append(max(fitnesses_2))                   # home is maximizing
                    self.board.pop()
                fitnesses_0.append(min(fitnesses_1))                     # enemy is minimizing
                self.board.pop()
            best_move_index = max_index_or_None(fitnesses_0)
        elif method == "ab_4":
            return self.alphabeta_search(4)

        elif method == "min_max_3.5":
            max_fitness_0 = -1000000
            for i, possible_move_0 in enumerate(all_moves):  # home move
                self.board.push(possible_move_0)
                min_fitness_1 = 1000000
                for possible_move_1 in self.get_moves():  # enemy move
                    self.board.push(possible_move_1)
                    max_fitness_2 = -1000000
                    for possible_move_2 in self.get_moves():  # home move
                        self.board.push(possible_move_2)
                        min_fitness_3 = 1000000

                        for possible_move_3 in self.get_capture_moves()[0]:  # enemy move
                            self.board.push(possible_move_3)
                            fitness = self.get_fitness(own_color)
                            self.board.pop()
                            if fitness < min_fitness_3:
                                # just evaluated move is the best continuation move so far
                                # enemy is minimizing
                                min_fitness_3 = fitness
                                if min_fitness_3 < max_fitness_2:
                                    # evaluated fitness is lower than home would allow, pruning branch
                                    break
                        if min_fitness_3 == 1000000:
                            # no capture moves were available default to turn 2 fitness
                            min_fitness_3 = self.get_fitness(own_color)
                        self.board.pop()
                        if min_fitness_3 > max_fitness_2:
                            # home is maximizing
                            max_fitness_2 = min_fitness_3
                            if max_fitness_2 > min_fitness_1:
                                break
                    self.board.pop()
                    if max_fitness_2 < min_fitness_1:
                        min_fitness_1 = max_fitness_2
                        if min_fitness_1 < max_fitness_0:
                            break
                self.board.pop()
                if min_fitness_1 > max_fitness_0:
                    max_fitness_0 = min_fitness_1
                    best_move_index = i

        else:
            raise ValueError(f"Invalid method selected: {method}")

        if best_move_index is None:
            return None
        else:
            return all_moves[best_move_index]


    def get_fitness(self, color):
        fitness = 0
        for piece_color in [True, False]:
            for piece in [1, 2, 3, 4, 5, 6]:
                for field in self.board.pieces(piece, piece_color):
                    if piece_color == color:
                        fitness += piece_values[piece]
                        fitness += piece_square_tables[piece_color][piece][field]
                    else:
                        fitness -= piece_values[piece]
                        fitness -= piece_square_tables[piece_color][piece][field]
        return fitness

    def alphabeta_search(self, depth):
        own_color = self.board.turn
        moves = self.get_moves()
        if not moves:
            print(f"found no moves for {colors[self.board.turn]}")
            return None
        best_fitness = -1000000
        best_move = None
        for move in moves:
            self.board.push(move)
            fitness = self.alphabeta(depth - 1, -1000000000, 1000000000, False, own_color)#
            self.board.pop()
            if fitness >= best_fitness:
                best_fitness = fitness
                best_move = move
        return best_move

    def alphabeta(self, depth, alpha, beta, is_maximizing, target_color):
        if not depth:       # depth is zero
            return self.get_fitness(target_color)
        if depth == 1:      # last call
            moves, non_capture_moves_exist = self.get_capture_moves()
            if not moves:
                if non_capture_moves_exist:
                    return self.get_fitness(target_color)
                else:
                    if is_maximizing:
                        return -1000000
                    else:
                        return 1000000
        else:
            moves = self.get_moves()
            if not moves:
                if is_maximizing:
                    return -1000000
                else:
                    return 1000000
        if is_maximizing:
            value = -1000000
            for move in moves:
                self.board.push(move)
                value = max(value, self.alphabeta(depth-1, alpha, beta, False, target_color))
                self.board.pop()
                if value >= beta:
                    break       # beta cutoff
                alpha = max(alpha, value)
            return value
        else:
            value = 1000000
            for move in moves:
                self.board.push(move)
                value = min(value, self.alphabeta(depth-1, alpha, beta, True, target_color))
                self.board.pop()
                if value <= alpha:
                    break       # alpha cutoff
                beta = min(beta, value)
            return value




    def get_moves(self):
        custom_order = []
        for move in self.board.legal_moves:
            if self.board.is_capture(move):
                custom_order.insert(0, move)
            else:
                custom_order.append(move)
        return custom_order

    def get_capture_moves(self):
        capture_moves = []
        non_capture_moves_exist = False
        for move in self.board.legal_moves:
            if self.board.is_capture(move):
                capture_moves.append(move)
            else:
                non_capture_moves_exist = True
        return capture_moves, non_capture_moves_exist


def simulate_game():
    game = Game()
    for i in range(10):
        game.board.push(game.get_best_move("min_max_4.5"))
        print(i)



if __name__ == "__main__":
    profile = cProfile.Profile()
    profile.runcall(simulate_game)
    ps = pstats.Stats(profile)
    ps.print_stats()

