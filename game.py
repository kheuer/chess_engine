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
piece_values = {1: 9, 2: 30, 3: 30, 4: 50, 5: 100, 6: 1000000}

piece_square_tables = {True:
                           {6: [2, 3, 1, 0, 0, 1, 3, 2, 2, 2, 0, 0, 0, 0, 2, 2, -1, -2, -2, -2, -2, -2, -2, -1, -2, -3, -3, -4, -4, -3, -3, -2, -3, -3, -4, -5, -5, -4, -4, -3, -3, -3, -4, -5, -5, -4, -4, -3, -3, -3, -4, -5, -5, -4, -4, -3, -3, -3, -4, -5, -5, -4, -4, -3],
                            5: [-2, -1, -1, -0.5, -0.5, -1, -1, 2, -1, 0, 0.5, 0, 0, 0, 0, -1, -1, 0.5, 0.5, 0.5, 0.5, 0.5, 0, -1, 0, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5, -0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5, -1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1, -1, 0, 0, 0, 0, 0, 0, -1, -2, -1, -1, -0.5, -0.5, -1, -1, -2],
                            4: [0, 0, 0, 0.5, 0.5, 0, 0, 0, -0.5, 0, 0, 0, 0, 0, 0, -0.5, -0.5, 0, 0, 0, 0, 0, 0, -0.5, -0.5, 0, 0, 0, 0, 0, 0, -0.5, -0.5, 0, 0, 0, 0, 0, 0, -0.5, -0.5, 0, 0, 0, 0, 0, 0, -0.5, 0.5, 1, 1, 1, 1, 1, 1, 0.5, 0, 0, 0, 0, 0, 0, 0, 0],
                            3: [-2, -1, -1, -1, -1, -1, -1, -2, -1, 0.5, 0, 0, 0, 0, 0.5, -1, -1, 1, 1, 1, 1, 1, 1, -1, -1, 0, 1, 1, 1, 1, 0, -1, -1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1, -1, 0, 0.5, 1, 1, 0.5, 0, -1, -1, 0, 0, 0, 0, 0, 0, -1, -2, -1, -1, -1, -1, -1, -1, -2],
                            2: [-5, -4, -3, -3, -3, -3, -4, -5, -4, -2, 0, 0.5, 0.5, 0, -2, -4, -3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3, -3, 0, 1.5, 2, 2, 1.5, 0, -3, -3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3, -3, 0, 1, 1.5, 1.5, 1, 0, -3, -4, -2, 0, 0, 0, 0, -2, -4, -5, -4, -3, -3, -3, -3, -4, -5],
                            1: [0, 0, 0, 0, 0, 0, 0, 0, 0.5, 1, 1, -2, -2, 1, 1, 0.5, 0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5, 0, 0, 0, 2, 2, 0, 0, 0, 0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5, 1, 1, 2, 3, 3, 2, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0],
                            },
                       False:
                            {6: [-3, -4, -4, -5, -5, -4, -3, -3, -3, -4, -4, -5, -5, -4, -3, -3, -3, -4, -4, -5, -5, -4, -3, -3, -3, -4, -4, -5, -5, -4, -3, -3, -2, -3, -3, -4, -4, -3, -3, -2, -1, -2, -2, -2, -2, -2, -2, -1, 2,  2,  0,  0,  0,  0,  2,  2, 2,  3,  1,  0,  0,  1,  3,  2],
                            5: [-2, -1, -1. , -0.5, -0.5, -1. , -1. , -2. , -1. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. , -1. , -1. ,  0. ,  0.5,  0.5,  0.5,  0.5,  0. , -1. , -0.5,  0. ,  0.5,  0.5,  0.5,  0.5,  0. , -0.5, -0.5,  0. ,  0.5,  0.5,  0.5,  0.5,  0. ,  0. , -1. ,  0. ,  0.5,  0.5,  0.5,  0.5,  0.5, -1. , -1. ,  0. ,  0. ,  0. ,  0. ,  0.5,  0. , -1. , 2. , -1. , -1. , -0.5, -0.5, -1. , -1. , -2.],
                            4: [0,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. , 0.5,  1. ,  1. ,  1. ,  1. ,  1. ,  1. ,  0.5, -0.5,  0. ,  0. ,  0. ,  0. ,  0. ,  0. , -0.5, -0.5,  0. ,  0. ,  0. ,  0. ,  0. ,  0. , -0.5,-0.5,  0. ,  0. ,  0. ,  0. ,  0. ,  0. , -0.5,-0.5,  0. ,  0. ,  0. ,  0. ,  0. ,  0. , -0.5,-0.5,  0. ,  0. ,  0. ,  0. ,  0. ,  0. , -0.5,0. ,  0. ,  0. ,  0.5,  0.5,  0. ,  0. ,  0.],
                            3: [-2, -1. , -1. , -1. , -1. , -1. , -1. , -2. ,-1. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. , -1. ,-1. ,  0. ,  0.5,  1. ,  1. ,  0.5,  0. , -1. ,-1. ,  0.5,  0.5,  1. ,  1. ,  0.5,  0.5, -1. ,-1. ,  0. ,  1. ,  1. ,  1. ,  1. ,  0. , -1. ,-1. ,  1. ,  1. ,  1. ,  1. ,  1. ,  1. , -1. ,-1. ,  0.5,  0. ,  0. ,  0. ,  0. ,  0.5, -1. ,-2. , -1. , -1. , -1. , -1. , -1. , -1. , -2.],
                            2: [-5. , -4. , -3. , -3. , -3. , -3. , -4. , -0.5,-4. , -2. ,  0. ,  0. ,  0. ,  0. , -2. , -4. ,-3. ,  0. ,  1. ,  1.5,  1.5,  1. ,  0. , -3. ,-3. ,  0.5,  1.5,  2. ,  2. ,  1.5,  0.5, -3. ,-3. ,  0. ,  1.5,  2. ,  2. ,  1.5,  0. , -3. ,-3. ,  0.5,  1. ,  1.5,  1.5,  1. ,  0.5, -3. ,-4. , -2. ,  0. ,  0.5,  0.5,  0. , -2. , -4. ,-5. , -4. , -3. , -3. , -3. , -3. , -4. , -5.],
                            1: [0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0.0,5. ,  5. ,  5. ,  5. ,  5. ,  5. ,  5. ,  5. ,1. ,  1. ,  2. ,  3. ,  3. ,  2. ,  1. ,  1. ,0.5,  0.5,  1. ,  2.5,  2.5,  1. ,  0.5,  0.5, 0. ,  0. ,  0. ,  2. ,  2. ,  0. ,  0. ,  0. , 0.5, -0.5, -1. ,  0. ,  0. , -1. , -0.5,  0.5, -5. ,  1. ,  1. , -2. , -2. ,  1. ,  1. ,  0.5, 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0.],
                            }
                       }


class Game:
    def __init__(self):
        self.board = chess.Board()

    def square_number_to_coords(self, square_number):
        return 7-chess.square_rank(square_number), chess.square_file(square_number)

    def get_moves_for_field(self, origin):
        possible_moves = []
        possible_coordinates = []
        for possible_move in self.board.legal_moves:
            if self.square_number_to_coords(possible_move.from_square) == origin:
                possible_moves.append(possible_move)
                possible_coordinates.append(self.square_number_to_coords(possible_move.to_square))
        return possible_moves, possible_coordinates

    def get_best_move(self, method="min_max_3_turns"):
        all_moves = list(self.board.legal_moves)
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
                return self.get_best_move("random")
            else:
                return self.get_best_move("min_max_2_turns")

        elif method == "min_max_2_turns":
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

        elif method == "min_max_3_turns":
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
        elif method == "min_max_3_turns_horizon_safe":
            fitnesses_0 = []
            for possible_move_1 in all_moves:   # home move
                self.board.push(possible_move_1)
                min_fitness_1 = 1000000
                for possible_move_2 in self.board.legal_moves:      # enemy move
                    self.board.push(possible_move_2)
                    max_fitness_2 = -1000000
                    for possible_move_3 in self.board.legal_moves:      # home move
                        self.board.push(possible_move_3)
                        min_fitness_3 = 1000000
                        for possible_move_4 in self.board.legal_moves:      # enemy move
                            if self.board.is_capture(possible_move_4):
                                self.board.push(possible_move_4)
                                fitness = self.get_fitness(own_color)
                                if fitness < min_fitness_3:                 # enemy is minimizing
                                    min_fitness_3 = fitness
                                self.board.pop()
                        if min_fitness_3 == 1000000:    # no capture moves were available default to turn 3 fitness
                            min_fitness_3 = self.get_fitness(own_color)
                        if min_fitness_3 > max_fitness_2:               # home is maximizing
                            max_fitness_2 = min_fitness_3
                        self.board.pop()
                    if max_fitness_2 < min_fitness_1:               # enemy is minimizing
                        min_fitness_1 = max_fitness_2
                    self.board.pop()
                fitnesses_0.append(min_fitness_1)
                self.board.pop()
            best_move_index = max_index_or_None(fitnesses_0)        # home is maximizing
        elif method == "min_max_3_turns_horizon_safe_ab":
            fitnesses_0 = []
            for possible_move_1 in all_moves:   # home move
                self.board.push(possible_move_1)
                min_fitness_1 = 1000000
                for possible_move_2 in self.board.legal_moves:      # enemy move
                    self.board.push(possible_move_2)
                    max_fitness_2 = -1000000
                    for possible_move_3 in self.board.legal_moves:      # home move
                        self.board.push(possible_move_3)
                        min_fitness_3 = 1000000
                        for possible_move_4 in self.board.legal_moves:      # enemy move
                            if self.board.is_capture(possible_move_4):
                                self.board.push(possible_move_4)
                                fitness = self.get_fitness(own_color)
                                if fitness < min_fitness_3:                 # enemy is minimizing
                                    min_fitness_3 = fitness
                                    if min_fitness_3 < max_fitness_2:       # evaluated fitness is lower than home would allow, pruning
                                        self.board.pop()
                                        break
                                self.board.pop()
                        if min_fitness_3 == 1000000:    # no capture moves were available default to turn 3 fitness
                            min_fitness_3 = self.get_fitness(own_color)
                        if min_fitness_3 > max_fitness_2:               # home is maximizing
                            max_fitness_2 = min_fitness_3
                            if max_fitness_2 > min_fitness_1:   # evaluated fitness is higher than enemy would allow, pruning
                                self.board.pop()
                                break
                        self.board.pop()
                    if max_fitness_2 < min_fitness_1:               # enemy is minimizing
                        min_fitness_1 = max_fitness_2
                        if min_fitness_1 < max_or(fitnesses_0, -100000000000):
                            self.board.pop()    # evaluated fitness is lower than home would allow, pruning
                            break
                    self.board.pop()
                fitnesses_0.append(min_fitness_1)
                self.board.pop()
            best_move_index = max_index_or_None(fitnesses_0)        # home is maximizing
        else:
            raise ValueError(f"Invalid method selected: {method}")

        if best_move_index is None:
            return None
        else:
            return all_moves[best_move_index]

    def get_best_move_ab(self, depth):
        best_move = chess.Move.null()
        best_value = -99999
        alpha = -100000
        beta = 100000
        for move in self.board.legal_moves:
            self.board.push(move)
            board_value = -self.alpha_beta_search(-beta, -alpha, depth - 1)
            if board_value > best_value:
                best_value = board_value
                best_move = move
            if board_value > alpha:
                alpha = board_value
            self.board.pop()
        return best_move

    def alpha_beta_search(self, alpha, beta, remaining_depth):
        best_score = -1000000
        if remaining_depth == 0:    # check capturing move to prevent last move suicides
            return self.alpha_beta_search_last_move(alpha, beta)
        for move in self.board.legal_moves:
            self.board.push(move)
            score = -self.alpha_beta_search(-beta, -alpha, remaining_depth - 1)
            self.board.pop()
            if score >= beta:
                return score
            if score > best_score:
                best_score = score
            if score > alpha:
                alpha = score
        return best_score

    def alpha_beta_search_last_move(self, alpha, beta):
        stand_pat = self.get_fitness(self.board.turn)
        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat

        for move in self.board.legal_moves:
            if self.board.is_capture(move):
                self.board.push(move)
                score = -self.alpha_beta_search_last_move(-beta, -alpha)
                self.board.pop()

                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score
        return alpha

    def get_fitness(self, color):
        assert type(color) == bool
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


def simulate_game():
    game = Game()
    for i in range(10):
        game.board.push(game.get_best_move("min_max_3_turns_horizon_safe_ab"))
        print(i)



if __name__ == "__main__":
    profile = cProfile.Profile()
    profile.runcall(simulate_game)
    ps = pstats.Stats(profile)
    ps.print_stats()

