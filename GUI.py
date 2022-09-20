from tkinter import *
import tkinter as tk
import chess
from PIL import Image, ImageTk
import numpy as np
from game import Game


size_of_board = 600
# valid methods: random, weakest, min_max_2_turns, min_max_3_turns, min_max_3_turns_horizon_safe
method = "terrible_player"
repeat_ai_game = True
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
        self.canvas.pack()
        frame = tk.Frame(self.root)
        frame.pack()

        tk.Button(frame, text="Take back 2 Moves", command=self.take_back_turn).grid(row=0, column=0)
        tk.Button(frame, text="Toggle Hints", command=self.toggle_hints).grid(row=0, column=1)
        tk.Button(frame, text="Explain Heuristic", command=self.game.explain_fitness).grid(row=0, column=2)
        tk.Button(frame, text="Print FEN", command=self.game.print_fen).grid(row=0, column=3)
        self.show_recommendation = True
        self.selected_piece = None
        if self.show_recommendation:
            recommendation = self.game.get_best_move(method=method)
            self.recommendation = self.game.square_number_to_coords(recommendation.from_square), self.game.square_number_to_coords(recommendation.to_square)
        else:
            self.recommendation = None

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
        frame = tk.Frame(self.root)
        frame.pack()
        tk.Button(frame, text="Make 2 Moves", command=self.simulate_turn).grid(row=0, column=0)
        tk.Button(frame, text="Run Entire Game", command=self.simulate_game).grid(row=0, column=1)
        tk.Button(frame, text="Take back 2 Moves", command=self.take_back_turn).grid(row=0, column=2)

        self.selected_piece = None
        self.possible_moves = []
        self.possible_coordinates = []
        self.draw_board()
        self.root.mainloop()

    def toggle_hints(self):
        self.show_recommendation = not self.show_recommendation
        if self.show_recommendation:
            recommendation = self.game.get_best_move(method=method)
            self.recommendation = self.game.square_number_to_coords(recommendation.from_square), self.game.square_number_to_coords(recommendation.to_square)
        else:
            self.recommendation = None
        self.draw_board()


    def take_back_turn(self):
        try:
            self.game.board.pop()
            self.game.board.pop()
            self.recommendation = None
        except IndexError:
            print("cant take back further than origin")
        self.draw_board()

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
                #self.canvas.create_text(col * size_of_square + size_of_square * 0.85, row * size_of_square + size_of_square * 0.85, text=str(abs(7-col+(row)*8-63)))

        if self.recommendation:
            row_1, col_1 = self.recommendation[0]
            row_2, col_2 = self.recommendation[1]
            self.canvas.create_line(col_1 * size_of_board / 8 + size_of_board * 1/16, row_1 * size_of_board / 8 + size_of_board * 1/16, col_2 * size_of_board / 8 + size_of_board * 1/16, row_2 * size_of_board / 8 + size_of_board * 1/16, arrow=tk.LAST, fill="red", width=5)

        for color in [True, False]:
            for piece in [1, 2, 3, 4, 5, 6]:
                for field in self.game.board.pieces(piece, color):
                    row, col = self.game.square_number_to_coords(field)
                    self.canvas.create_image(col * size_of_board / 8, row * size_of_board / 8, image=self.images[(colors[color], pieces[piece])], anchor="nw")

        if self.last_moved:
            row, col = self.last_moved
            self.canvas.create_oval(col * size_of_board / 8, row * size_of_board / 8, (col + 1) * size_of_board / 8,
                                    (row + 1) * size_of_board / 8, outline="grey", width=2)

        for (row, col) in self.possible_coordinates:
            self.canvas.create_oval(col * size_of_board / 8, row * size_of_board / 8, (col+1) * size_of_board / 8, (row+1) * size_of_board / 8, outline="white")

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array([grid_position[1], grid_position[0]])
        return np.array(grid_position // (size_of_board / 8), dtype=int)

    def simulate_move(self):
        enemy_move = self.game.get_best_move(method="random")
        self.game.board.push(enemy_move)
        self.last_moved = self.game.square_number_to_coords(enemy_move.from_square)

        print(f"  Black´s Fitness: {self.game.get_fitness(False)}")

        self.whites_turn = bool(not self.whites_turn)
        self.draw_board()

    def simulate_turn(self):
        # valid methods: random, weakest, terrible_player, min_max_2, min_max_3.5, min_max_4.5
        method = {True: "ab_5", False: "terrible_player"}[self.game.board.turn]

        move = self.game.get_best_move(method)
        if move:
            self.game.board.push(move)


        self.draw_board()

        outcome = self.game.board.outcome()
        if outcome:
            if outcome.winner is None:
                print(f"Game over, draw. Reason: {outcome.termination}")
            else:
                print(f"Game over {colors[outcome.winner]} won.")
            if not repeat_ai_game:
                return
            else:
                self.game = Game()

        if not self.game.board.turn:
            self.root.after(1, self.simulate_turn)
            return

    def simulate_game(self):
        self.simulate_turn()
        outcome = self.game.board.outcome()
        if outcome:
            if repeat_ai_game:
                self.root.after(1, self.simulate_game)
        else:
            self.root.after(1, self.simulate_game)

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
            self.recommendation = None
            self.last_moved = (row, col)
            self.draw_board()
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

        self.draw_board()

    def finish_human_turn(self):
        #print(f"White´s Fitness: {self.game.get_fitness(True)}")
        enemy_move, recommendation = self.game.get_best_move(method=method, get_recommendation=True)
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

        if self.show_recommendation:
            if type(recommendation) == str or recommendation is None:
                self.recommendation = None
            else:
                self.recommendation = self.game.square_number_to_coords(recommendation.from_square), self.game.square_number_to_coords(recommendation.to_square)
        self.draw_board()

if __name__ == "__main__":
    GUI().start_human_game()

