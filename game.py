import chess.svg
import numpy as np
import chess
import cProfile
import pstats
import time
from piece_square_tables import (
    piece_square_tables_early_to_midgame,
    piece_square_tables_endgame,
)


explain_color = True
colors = {True: "White", False: "Black"}
pieces = {1: "Pawn", 2: "Knight", 3: "Bishop", 4: "Rook", 5: "Queen", 6: "King"}
piece_values_early_to_midgame = {1: 9, 2: 30, 3: 30, 4: 50, 5: 100, 6: 1000000}
piece_values_endgame = {1: 9, 2: 25, 3: 30, 4: 80, 5: 120, 6: 1000000}
exploration_parameter = np.sqrt(2)  # exploration factor for monte carlo tree search


def is_number(x):
    if isinstance(x, bool):
        return False
    try:
        float(x)
        return True
    except (ValueError, TypeError):
        return False


class FitnessContainer:
    def __init__(self, val, content=None):
        self.val = val
        assert is_number(self.val)
        self.content = content

    def __lt__(self, other):
        return self.val < other.val

    def __eq__(self, other):
        return self.val == other.val

    def __le__(self, other):
        return self.val <= other.val

    def __ge__(self, other):
        return self.val >= other.val

    def __repr__(self):
        return f"Container: fitness={self.val}, moves={self.content}"


def get_material_coefficient(score):
    if score > 70:  # query color is far ahead (inf 70)
        return 0.9
    elif score > 30:  # query color is ahead (70 30)
        return 0.95
    elif score > -30:  # query color is about even (30 -30)
        return 1
    elif score > 0.7:  # query color is behind (-30 -70)
        return 1.05
    else:  # query color is far behind (-70 -inf)
        return 1.1


class Game:
    def __init__(self):
        self.board = chess.Board()
        # self.board = chess.Board("8/8/prR5/1p1p2k1/1P6/P3P3/2R1K3/8 w - - 0 31")
        # self.board = chess.Board("r3k2r/ppp2ppp/4b3/2n1p3/3P4/P3pP2/1PP3PP/RKB2B1R")
        # self.board = chess.Board("rnbqk1nr/ppp2ppp/8/3Pp3/1b1P4/8/PPP2PPP/RNBQKBNR")
        # self.board = chess.Board("r2qr1k1/1ppbbppp/p1np1n2/4p3/4P3/P1N2N1P/1PPPBPP1/1RBQR1K1")
        # self.board = chess.Board("rnb1kb1r/1p2p1pp/2pq1n2/p4P2/B2p4/2N2Q2/PPPPNPPP/R1B1K2R")
        self.set_endgame_flag()

    def get_board_image(self):
        return chess.svg.board(self.board)

    def print_fen(self):
        print(self.board.board_fen())

    def square_number_to_coords(self, square_number):
        return 7 - chess.square_rank(square_number), chess.square_file(square_number)

    def get_move_from_coords(self, origin, target):
        uci = (
            f"{'abcdefgh'[origin[1]]}{8-origin[0]}{'abcdefgh'[target[1]]}{8-target[0]}"
        )
        move = chess.Move.from_uci(uci)
        promotion_move = chess.Move.from_uci(uci + "q")

        if self.board.is_legal(promotion_move):
            return promotion_move
        else:
            return move

    def get_moves_for_field(self, origin):
        possible_moves = []
        possible_coordinates = []
        for possible_move in self.board.legal_moves:
            if self.square_number_to_coords(possible_move.from_square) == origin:
                possible_moves.append(possible_move)
                possible_coordinates.append(
                    self.square_number_to_coords(possible_move.to_square)
                )
        return possible_moves, possible_coordinates

    def set_pieces_left(self):
        self.pieces_left = 0
        for i in range(64):
            if self.board.piece_at(i):
                self.pieces_left += 1

    def set_endgame_flag(self):
        self.set_pieces_left()
        if self.pieces_left <= 8:
            self.endgame_has_started = True
        else:
            self.endgame_has_started = False

    def get_best_move(self, method="auto", log=False):
        self.set_endgame_flag()

        if method == "minimax_auto":
            if self.pieces_left <= 4:
                method = "minimax_6"
            else:
                method = "minimax_5"
        if log:
            print(
                f"   finding best move for {colors[self.board.turn]} with method: {method}"
            )

        if method == "random":
            all_moves = self.get_moves()
            if all_moves:
                return np.random.choice(all_moves)
            else:
                return None

        elif method == "terrible_player":
            if np.random.random() < 0.1:
                return self.get_best_move("random", False)
            else:
                return self.get_best_move("minimax_2", False)
        elif method == "minimax_1":
            return self.alphabeta_search(1)
        elif method == "minimax_2":
            return self.alphabeta_search(2)
        elif method == "minimax_3":
            return self.alphabeta_search(3)
        elif method == "minimax_4":
            return self.alphabeta_search(4)
        elif method == "minimax_5":
            return self.alphabeta_search(5)
        elif method == "minimax_6":
            return self.alphabeta_search(6)
        elif method == "mcts_1s":
            return self.monte_carlo_tree_search(1)
        elif method == "mcts_3s":
            return self.monte_carlo_tree_search(3)
        elif method == "mcts_6s":
            return self.monte_carlo_tree_search(6)
        elif method == "mcts_10s":
            return self.monte_carlo_tree_search(10)
        else:
            raise ValueError(f"Invalid method selected: {method}")

    def monte_carlo_tree_search(self, seconds):
        end_time = time.time() + seconds
        maximizing_for = self.board.turn
        starting_n_turns = len(self.board.move_stack)
        root_node = MCTS_Node(None, [], None)  # create root Node
        while time.time() <= end_time:
            leaf = self.mcts_selection(root_node)
            expanded_leaf = self.mcts_expansion(leaf)
            end_result = self.mcts_simulate(maximizing_for)
            self.mcts_backpropagate(expanded_leaf, end_result)
            while (
                len(self.board.move_stack) != starting_n_turns
            ):  # take back turns to where the algorithm started from
                self.board.pop()
        return root_node.get_most_visited_child().move

    def mcts_selection(self, node):
        while node.children:
            node = node.get_highest_scored_child()
            if node.move is not None:
                self.board.push(node.move)
        return node

    def mcts_expansion(self, node):
        if self.board.outcome():  # game has ended
            return node
        else:
            for move in self.board.legal_moves:
                node.children.append(MCTS_Node(node, [], move))
        random_child = node.get_random_child()
        self.board.push(random_child.move)
        return random_child

    def mcts_simulate(self, maximizing_for):
        while not self.board.outcome():
            self.board.push(np.random.choice(list(self.board.legal_moves)))
        winner = self.board.outcome().winner
        if winner is None:
            return 0  # simulations ends in draw
        elif winner == maximizing_for:
            return 1  # simulation ends in win
        else:
            return -1  # simulation ends in defeat

    def mcts_backpropagate(self, node, result):
        node.utility += result
        node.n_visits += 1
        if node.parent is None:
            return
        else:
            self.mcts_backpropagate(node.parent, result)

    def get_fitness(self, color):
        if self.endgame_has_started:
            piece_value_lookup_table = piece_values_endgame
            piece_square_lookup_table = piece_square_tables_endgame
        else:
            piece_value_lookup_table = piece_values_early_to_midgame
            piece_square_lookup_table = piece_square_tables_early_to_midgame

        material = 0
        positional = 0
        for piece_color in [True, False]:
            for piece in [1, 2, 3, 4, 5, 6]:
                for field in self.board.pieces(piece, piece_color):
                    if piece_color == color:
                        material += piece_value_lookup_table[piece]
                        positional += piece_square_lookup_table[piece_color][piece][
                            field
                        ]
                    else:
                        material -= piece_value_lookup_table[piece]
                        positional -= piece_square_lookup_table[piece_color][piece][
                            field
                        ]
        return material * get_material_coefficient(material) + positional

    def explain_fitness(self, color=explain_color):
        if self.endgame_has_started:
            piece_value_lookup_table = piece_values_endgame
            piece_square_lookup_table = piece_square_tables_endgame
        else:
            piece_value_lookup_table = piece_values_early_to_midgame
            piece_square_lookup_table = piece_square_tables_early_to_midgame

        print(f"\nFitness Overview for {colors[color]}:")
        material = np.zeros((8, 8))
        positional = np.zeros((8, 8))
        for field in range(64):
            row, col = self.square_number_to_coords(field)
            piece = self.board.piece_at(field)
            if piece:
                piece_type = piece.piece_type
                piece_color = piece.color
                if color == piece_color:
                    color_multiplier = 1
                else:
                    color_multiplier = -1

                material[row, col] = (
                    piece_value_lookup_table[piece_type] * color_multiplier
                )
                positional[row, col] = (
                    piece_square_lookup_table[piece_color][piece_type][field]
                    * color_multiplier
                )

        print("Material:")
        self.print_array(material)
        print("Positional:")
        self.print_array(positional)
        material_val = round(sum(sum(material)), 2)
        positional_val = round(sum(sum(positional)), 2)
        print(
            f"\nmaterial: {material_val}, positional: {positional_val}, adjusted sum: {material_val} * {get_material_coefficient(material_val)} + {positional_val} = {round(self.get_fitness(color), 2)}"
        )

    def print_array(self, array):
        for row in array:
            print([round(x, 2) for x in row])

    def alphabeta_search(self, depth):
        # this should only be initialized with an even depth because of the horizon effect
        fitness_container = self.alphabeta(
            depth,
            FitnessContainer(-10000000000000),
            FitnessContainer(1000000000000),
            True,
            self.board.turn,
            depth % 2 == 0,
        )

        if self.board.outcome():  # Game has ended
            return None
        return fitness_container.content[0]

    def alphabeta(self, depth, alpha, beta, is_maximizing, target_color, is_even):
        if depth == 0:  # depth is zero
            return FitnessContainer(self.get_fitness(target_color), ["Frontier"])
        if depth == 1:  # last call
            if is_even:
                moves, non_capture_moves_exist = self.get_capture_moves()
                if not moves and non_capture_moves_exist:
                    return FitnessContainer(
                        self.get_fitness(target_color), ["Frontier"]
                    )
            else:
                moves, capture_moves_exist = self.get_non_capture_moves()
                if not moves and capture_moves_exist:
                    return FitnessContainer(
                        self.get_fitness(target_color), ["Frontier"]
                    )
        else:
            moves = self.get_moves()

        outcome = self.board.outcome()
        if outcome:
            if outcome.winner is None:
                return FitnessContainer(0, ["Draw"])
            elif outcome.winner == target_color:
                return FitnessContainer(
                    1000000 + depth, [colors[outcome.winner] + " wins."]
                )
            else:
                return FitnessContainer(
                    -1000000 - depth, [colors[outcome.winner] + " wins."]
                )

        if is_maximizing:
            value = FitnessContainer(-1000000000)
            for move in moves:
                self.board.push(move)
                new_value = self.alphabeta(
                    depth - 1, alpha, beta, False, target_color, is_even
                )
                if new_value > value:
                    value = new_value
                    best_move = move
                self.board.pop()
                if value > beta:
                    break  # beta cutoff
                alpha = max(alpha, value)
            return FitnessContainer(value.val, [best_move] + value.content)
        else:
            value = FitnessContainer(1000000000)
            for move in moves:
                self.board.push(move)
                new_value = self.alphabeta(
                    depth - 1, alpha, beta, True, target_color, is_even
                )
                if new_value < value:
                    value = new_value
                    best_move = move
                self.board.pop()
                if value <= alpha:
                    break  # alpha cutoff
                beta = min(beta, value)
            return FitnessContainer(value.val, [best_move] + value.content)

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

    def get_non_capture_moves(self):
        non_capture_moves = []
        capture_moves_exist = False
        for move in self.board.legal_moves:
            if not self.board.is_capture(move):
                non_capture_moves.append(move)
            else:
                capture_moves_exist = True
        return non_capture_moves, capture_moves_exist

    def describe_move(self, move):
        if move is None:
            return "Game is over, go outside."

        origin = move.from_square
        target = move.to_square
        promotion = move.promotion
        piece = self.board.piece_at(origin)
        color = colors[piece.color]

        if self.board.is_capture(move):
            victim = self.board.piece_at(target)
            if not victim:
                return f"En Passant with Pawn at {chess.square_name(origin)} to {chess.square_name(target)}"
            else:
                desc = f"{color} captures {pieces[victim.piece_type]} with {pieces[piece.piece_type]} from {chess.square_name(origin)} to {chess.square_name(target)}"
        else:
            desc = f"{color} moves with {pieces[piece.piece_type]} from {chess.square_name(origin)} to {chess.square_name(target)}"

        if promotion:
            desc += f" promotes to {pieces[promotion]}"
        return desc


class MCTS_Node:
    def __init__(self, parent, children, move):
        assert isinstance(parent, MCTS_Node) or parent is None
        assert isinstance(children, list)
        assert isinstance(move, chess.Move) or move is None

        self.parent = parent
        self.children = children
        self.move = move

        self.utility = 0
        self.n_visits = 1

    def get_ucb_score(self):
        return self.utility / self.n_visits + exploration_parameter * np.sqrt(
            np.log(self.parent.n_visits) / self.n_visits
        )

    def __repr__(self):
        return f"{self.utility}/{self.n_visits}"

    def get_random_child(self):
        return np.random.choice(self.children)

    def get_most_visited_child(self):
        n_visits = [x.n_visits for x in self.children]
        indices = [i for i, x in enumerate(n_visits) if x == max(n_visits)]
        return self.children[np.random.choice(indices)]

    def get_highest_scored_child(self):
        scores = [x.get_ucb_score() for x in self.children]
        indices = [i for i, x in enumerate(scores) if x == max(scores)]
        return self.children[np.random.choice(indices)]


def simulate_game():
    game = Game()
    for i in range(10):
        game.board.push(game.get_best_move("minimax_5"))
        print(i)


if __name__ == "__main__":
    profile = cProfile.Profile()
    profile.runcall(simulate_game)
    ps = pstats.Stats(profile)
    ps.print_stats()
