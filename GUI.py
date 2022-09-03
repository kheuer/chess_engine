from tkinter import *
import tkinter as tk
import chess
from PIL import Image, ImageTk
import numpy as np
from game import Game


size_of_board = 600
# valid methods: random, weakest, min_max_2_turns, min_max_3_turns, min_max_3_turns_horizon_safe
method = "min_max_3.5"

colors = {True: "White", False: "Black"}
pieces = {1: "Pawn", 2: "Knight", 3: "Bishop", 4: "Rook", 5: "Queen", 6: "King"}

def coordinates_to_square(row, col):
    return (7-row)*8 + col

class GUI:
    def __init__(self):
        self.game = Game()
        self.last_moved = None
        self.whites_turn = True
        self.game_over = False

    def level_editor(self):
        self.root = Tk()
        self.images = {
            ("White", "King"): ImageTk.PhotoImage(
                Image.open("images/White_King.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("Black", "King"): ImageTk.PhotoImage(
                Image.open("images/Black_King.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("White", "Queen"): ImageTk.PhotoImage(
                Image.open("images/White_Queen.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("Black", "Queen"): ImageTk.PhotoImage(
                Image.open("images/Black_Queen.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("White", "Bishop"): ImageTk.PhotoImage(
                Image.open("images/White_Bishop.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("Black", "Bishop"): ImageTk.PhotoImage(
                Image.open("images/Black_Bishop.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("White", "Knight"): ImageTk.PhotoImage(
                Image.open("images/White_Knight.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("Black", "Knight"): ImageTk.PhotoImage(
                Image.open("images/Black_Knight.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("White", "Rook"): ImageTk.PhotoImage(
                Image.open("images/White_Rook.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("Black", "Rook"): ImageTk.PhotoImage(
                Image.open("images/Black_Rook.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("White", "Pawn"): ImageTk.PhotoImage(
                Image.open("images/White_Pawn.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("Black", "Pawn"): ImageTk.PhotoImage(
                Image.open("images/Black_Pawn.png").resize((int(size_of_board / 8), int(size_of_board / 8))))
        }
        self.root.title("Chess")
        self.canvas = Canvas(self.root, width=size_of_board, height=size_of_board)
        self.canvas.grid(row=0, column=0)
        self.selected_piece = None
        self.possible_moves = []
        self.possible_coordinates = []
        self.draw_board()
        self.root.bind("<Button-1>", self.move_free)
        self.root.mainloop()

    def start_human_game(self):
        self.root = Tk()
        self.images = {
            ("White", "King"): ImageTk.PhotoImage(
                Image.open("images/White_King.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("Black", "King"): ImageTk.PhotoImage(
                Image.open("images/Black_King.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("White", "Queen"): ImageTk.PhotoImage(
                Image.open("images/White_Queen.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("Black", "Queen"): ImageTk.PhotoImage(
                Image.open("images/Black_Queen.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("White", "Bishop"): ImageTk.PhotoImage(
                Image.open("images/White_Bishop.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("Black", "Bishop"): ImageTk.PhotoImage(
                Image.open("images/Black_Bishop.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("White", "Knight"): ImageTk.PhotoImage(
                Image.open("images/White_Knight.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("Black", "Knight"): ImageTk.PhotoImage(
                Image.open("images/Black_Knight.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("White", "Rook"): ImageTk.PhotoImage(
                Image.open("images/White_Rook.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("Black", "Rook"): ImageTk.PhotoImage(
                Image.open("images/Black_Rook.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("White", "Pawn"): ImageTk.PhotoImage(
                Image.open("images/White_Pawn.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("Black", "Pawn"): ImageTk.PhotoImage(
                Image.open("images/Black_Pawn.png").resize((int(size_of_board / 8), int(size_of_board / 8))))
        }
        self.root.title("Chess")
        self.canvas = Canvas(self.root, width=size_of_board, height=size_of_board)
        self.canvas.grid(row=0, column=0)
        self.selected_piece = None
        self.possible_moves = []
        self.possible_coordinates = []
        self.draw_board()
        self.root.bind("<Button-1>", self.click)
        self.root.mainloop()

    def start_ai_game(self):
        self.root = Tk()
        self.images = {
            ("White", "King"): ImageTk.PhotoImage(
                Image.open("images/White_King.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("Black", "King"): ImageTk.PhotoImage(
                Image.open("images/Black_King.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("White", "Queen"): ImageTk.PhotoImage(
                Image.open("images/White_Queen.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("Black", "Queen"): ImageTk.PhotoImage(
                Image.open("images/Black_Queen.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("White", "Bishop"): ImageTk.PhotoImage(
                Image.open("images/White_Bishop.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("Black", "Bishop"): ImageTk.PhotoImage(
                Image.open("images/Black_Bishop.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("White", "Knight"): ImageTk.PhotoImage(
                Image.open("images/White_Knight.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("Black", "Knight"): ImageTk.PhotoImage(
                Image.open("images/Black_Knight.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("White", "Rook"): ImageTk.PhotoImage(
                Image.open("images/White_Rook.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("Black", "Rook"): ImageTk.PhotoImage(
                Image.open("images/Black_Rook.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("White", "Pawn"): ImageTk.PhotoImage(
                Image.open("images/White_Pawn.png").resize((int(size_of_board / 8), int(size_of_board / 8)))),
            ("Black", "Pawn"): ImageTk.PhotoImage(
                Image.open("images/Black_Pawn.png").resize((int(size_of_board / 8), int(size_of_board / 8))))
        }
        self.root.title("Chess")
        self.canvas = Canvas(self.root, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        self.selected_piece = None
        self.possible_moves = []
        self.possible_coordinates = []
        self.draw_board()
        self.root.bind("<Button-1>", self.simulate_game)
        self.root.mainloop()


    def draw_board(self):
        size_of_square = size_of_board / 8
        self.canvas.delete("all")
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    c = "#563a12"
                else:
                    c = "#9f9362"
                self.canvas.create_rectangle(col * size_of_square, row * size_of_square, (col+1) * size_of_square, (row+1) * size_of_square, fill=c, tags=f"tile{col + 1}{row + 1}")
                self.canvas.create_text(col * size_of_square + size_of_square*0.85, row * size_of_square + size_of_square*0.85, text="abcdefgh"[col] + str(8 - row))

        for color in [True, False]:
            for piece in [1, 2, 3, 4, 5, 6]:
                for field in self.game.board.pieces(piece, color):
                    row, col = self.game.square_number_to_coords(field)
                    self.canvas.create_image(col * size_of_board / 8, row * size_of_board / 8, image=self.images[(colors[color], pieces[piece])], anchor="nw")

        for (row, col) in self.possible_coordinates:
            self.canvas.create_oval(col * size_of_board / 8, row * size_of_board / 8, (col+1) * size_of_board / 8, (row+1) * size_of_board / 8, outline="white")

        if self.last_moved:
            row, col = self.last_moved
            self.canvas.create_oval(col * size_of_board / 8, row * size_of_board / 8, (col + 1) * size_of_board / 8,
                                    (row + 1) * size_of_board / 8, outline="grey", width=2)

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array([grid_position[1], grid_position[0]])
        return np.array(grid_position // (size_of_board / 8), dtype=int)

    def simulate_move(self):
        enemy_move = self.game.get_best_move(method="random")
        self.game.board.push(enemy_move)
        self.last_moved = self.game.square_number_to_coords(enemy_move.from_square)

        print(f"White´s Fitness: {self.game.get_fitness(True)}")

        self.whites_turn = bool(not self.whites_turn)
        self.draw_board()

    def simulate_game(self, click_event=None):
        # valid methods: random, weakest, terrible_player, min_max_2, min_max_3.5, min_max_4.5
        method = {True: "min_max_3.5", False: "min_max_3.5"}[self.game.board.turn]
        end_after_1_game = False

        move = self.game.get_best_move(method)
        try:
            self.game.board.push(move)
        except AttributeError:
            pass
            # this is a weird bug in the chess engine where it checks a captured piece and throws an error
        self.draw_board()


        outcome = self.game.board.outcome()
        if outcome:
            if outcome.winner is None:
                print(f"Game over, draw. Reason: {outcome.termination}")
            else:
                print(f"Game over {colors[outcome.winner]} wins.")
            if end_after_1_game:
                return
            else:
                self.game = Game()

        self.root.after(100, self.simulate_game)

    def click(self, event):
        outcome = self.game.board.outcome()
        if outcome:
            if outcome.winner is None:
                print(f"Game over, draw. Reason: {outcome.termination}")
            else:
                print(f"Game over {colors[outcome.winner]} wins.")
            return

        grid_position = [event.x, event.y]
        row, col = self.convert_grid_to_logical_position(grid_position)

        piece = self.game.board.piece_at(coordinates_to_square(row, col))
        if (row, col) == self.selected_piece:   # deselect the current piece
            self.selected_piece = None
            self.possible_moves = []
            self.possible_coordinates = []
        elif (row, col) in self.possible_coordinates:
            normal_move = chess.Move(from_square=coordinates_to_square(self.selected_piece[0], self.selected_piece[1]),
                                     to_square=coordinates_to_square(row, col))
            promotion_move = chess.Move(from_square=coordinates_to_square(self.selected_piece[0], self.selected_piece[1]),
                                     to_square=coordinates_to_square(row, col),
                                     promotion=chess.QUEEN)
            if self.game.board.is_legal(promotion_move):
                self.game.board.push(promotion_move)
            else:
                self.game.board.push(normal_move)

            self.draw_board()
            self.last_moved = (row, col)
            self.selected_piece = None
            self.possible_moves = []
            self.possible_coordinates = []
            self.root.after(100, self.finish_human_turn)
        elif piece:
            if piece.color:     # piece is white
                self.selected_piece = (row, col)
                self.possible_moves, self.possible_coordinates = self.game.get_moves_for_field(self.selected_piece)
            else:
                print("cant move enemy piece")
        else:
            print("invalid field selected")

        self.draw_board()

    def finish_human_turn(self):
        enemy_move = self.game.get_best_move(method=method)
        if enemy_move is None:
            self.draw_board()
            self.selected_piece = None
            self.possible_moves = []
            self.possible_coordinates = []
            self.last_moved = None
            self.game_over = True
            print("Could not find an enemy move.")
            return

        origin = self.game.square_number_to_coords(enemy_move.from_square)
        self.game.board.push(enemy_move)
        self.last_moved = origin
        self.draw_board()
        print(f"White´s Fitness: {self.game.get_fitness(True)}")

    def move_free(self, event):

        grid_position = [event.x, event.y]
        row, col = self.convert_grid_to_logical_position(grid_position)

        piece = self.game.board.piece_at(coordinates_to_square(row, col))
        if (row, col) == self.selected_piece:   # deselect the current piece
            self.selected_piece = None

        elif self.selected_piece:
            if self.game.board.piece_at(self.game.coords_to_square_number(self.selected_piece[0], self.selected_piece[1])).color != self.game.board.turn:
                self.game.board.push(chess.Move.null())


            normal_move = chess.Move(from_square=coordinates_to_square(self.selected_piece[0], self.selected_piece[1]),
                                     to_square=coordinates_to_square(row, col))
            self.game.board.push(normal_move)

            self.draw_board()
            self.selected_piece = None
        elif piece:
            self.selected_piece = (row, col)
        else:
            print("invalid field selected")
        print(self.game.board.fen())

        self.draw_board()
if __name__ == "__main__":
    GUI().start_ai_game()
