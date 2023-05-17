from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
import chess
from PIL import Image, ImageTk
from game import Game
from functools import partial
import time


size_of_board = 600
size_of_square = int(size_of_board / 8)
size_of_piece = 60
width_of_square = 60
height_of_square = 60

ai_methods = ["random", "terrible_player", "minimax_2", "minimax_3", "minimax_4", "minimax_5", "minimax_auto", "mcts_1s", "mcts_3s", "mcts_6s", "mcts_10s"]

colors = {True: "White", False: "Black"}


def coordinates_to_square(row, col):
    return (7-row)*8 + col

def square_number_to_coords(square_number):
    return 7-chess.square_rank(square_number), chess.square_file(square_number)

def coords_to_square_number(row, col):
    return 8 * (7-row) + col

class GUI:
    def __init__(self):
        self.game = Game()
        self.last_moved = None
        self.whites_turn = True
        self.game_over = False
        self.selected_origin = None     # refers to a field from where a move can be made
        self.selected_ai_black = "mcts_10s"
        self.selected_ai_white = "minimax_2"
        self.move_descs = []

        self.root = Tk()
        self.images = {
            (True, 6): ImageTk.PhotoImage(
                Image.open("images/White_King.png").resize((size_of_piece, size_of_piece))),
            (False, 6): ImageTk.PhotoImage(
                Image.open("images/Black_King.png").resize((size_of_piece, size_of_piece))),
            (True, 5): ImageTk.PhotoImage(
                Image.open("images/White_Queen.png").resize((size_of_piece, size_of_piece))),
            (False, 5): ImageTk.PhotoImage(
                Image.open("images/Black_Queen.png").resize((size_of_piece, size_of_piece))),
            (True, 3): ImageTk.PhotoImage(
                Image.open("images/White_Bishop.png").resize((size_of_piece, size_of_piece))),
            (False, 3): ImageTk.PhotoImage(
                Image.open("images/Black_Bishop.png").resize((size_of_piece, size_of_piece))),
            (True, 2): ImageTk.PhotoImage(
                Image.open("images/White_Knight.png").resize((size_of_piece, size_of_piece))),
            (False, 2): ImageTk.PhotoImage(
                Image.open("images/Black_Knight.png").resize((size_of_piece, size_of_piece))),
            (True, 4): ImageTk.PhotoImage(
                Image.open("images/White_Rook.png").resize((size_of_piece, size_of_piece))),
            (False, 4): ImageTk.PhotoImage(
                Image.open("images/Black_Rook.png").resize((size_of_piece, size_of_piece))),
            (True, 1): ImageTk.PhotoImage(
                Image.open("images/White_Pawn.png").resize((size_of_piece, size_of_piece))),
            (False, 1): ImageTk.PhotoImage(
                Image.open("images/Black_Pawn.png").resize((size_of_piece, size_of_piece)))
        }

        self.root.title("Chess")

        self.board_outer_frame = Frame(self.root, width=size_of_board, height=size_of_board)
        self.board_outer_frame.grid(row=0, column=0)

        control_frame = tk.Frame(self.root)
        control_frame.grid(row=0, column=1)

        explain_frame = Frame(control_frame)
        explain_frame.pack()
        Label(explain_frame, text="Fitness Overview", width=20, font=10).pack()
        self.white_fitness_var = StringVar()
        self.black_fitness_var = StringVar()
        self.game_state_var = StringVar()

        Label(explain_frame, textvariable=self.white_fitness_var).pack()
        Label(explain_frame, textvariable=self.black_fitness_var).pack()
        ttk.Separator(explain_frame, orient="horizontal").pack()
        Label(explain_frame, textvariable=self.game_state_var).pack()

        Label(control_frame, text="Controls", font=10).pack()
        Button(control_frame, text="Make AI Move", command=self.simulate_ai_move, width=20).pack()
        Button(control_frame, text="Take back 2 Moves", command=self.take_back_turn, width=20).pack()
        Button(control_frame, text="Reset Board", command=self.reset_board, width=20).pack()
        Button(control_frame, text="Explain Position", command=self.game.explain_fitness, width=20).pack()
        Button(control_frame, text="Print FEN", command=self.game.print_fen, width=20).pack()
        Button(control_frame, text="Simulate full Game", command=self.simulate_game, width=20).pack()

        self.white_ai_var = StringVar()
        self.black_ai_var = StringVar()

        ai_frame = Frame(control_frame)
        ai_frame.pack()

        Label(ai_frame, text="AI Selection", font=10).grid(row=0, column=0, columnspan=2)
        Label(ai_frame, textvariable=self.white_ai_var).grid(row=1, column=0)
        Button(ai_frame, text="Next", command=partial(self.increment_ai, True)).grid(row=1, column=1)
        Label(ai_frame, textvariable=self.black_ai_var).grid(row=2, column=0)
        Button(ai_frame, text="Next", command=partial(self.increment_ai, False)).grid(row=2, column=1)

        Label(control_frame, text="Analysis", font=10).pack()

        Label(control_frame, text="Recommended move:").pack()
        self.recommended_move_var = StringVar()
        Label(control_frame, textvariable=self.recommended_move_var).pack()

        self.last_moves_var = StringVar()
        Label(control_frame, textvariable=self.last_moves_var).pack()

        self.refresh_gui()
        self.game_state_var.set("Game is not running.")
        self.white_fitness_var.set("white_fitness: N/A")
        self.black_fitness_var.set("black_fitness: N/A")
        self.root.mainloop()

    def reset_board(self):
        self.game = Game()
        self.move_descs = []
        self.refresh_gui()

    def simulate_game(self):
        while not self.game.board.outcome():
            self.make_ai_move()
            self.refresh_gui()
            self.root.update()
            time.sleep(1)

    def increment_ai(self, color):
        if color:
            ai = self.selected_ai_white
        else:
            ai = self.selected_ai_black
        new_index = ai_methods.index(ai) + 1
        if new_index == len(ai_methods):
            new_index = 0
        if color:
            self.selected_ai_white = ai_methods[new_index]
        else:
            self.selected_ai_black = ai_methods[new_index]
        self.refresh_gui()

    def simulate_ai_move(self):
        self.make_ai_move()
        self.refresh_gui()

    def refresh_gui(self):
        self.white_fitness_var.set(f"white_fitness: {round(self.game.get_fitness(True), 3)}")
        self.black_fitness_var.set(f"black_fitness: {round(self.game.get_fitness(False), 3)}")
        outcome = self.game.board.outcome()
        if outcome:
            if outcome.winner is None:
                self.game_state_var.set(f"Game is over, draw.\nReason: {outcome.termination}")
            else:
                self.game_state_var.set(f"Game is over,\n{colors[outcome.winner]} won.")
        else:
            self.game_state_var.set(f"Game is running.")

        self.white_ai_var.set(f"white_ai: {self.selected_ai_white}")
        self.black_ai_var.set(f"black_ai: {self.selected_ai_black}")

        moves_desc_readable = ""
        for i, move_desc in enumerate(self.move_descs):
            if i == 6:
                break
            else:
                moves_desc_readable += move_desc + "\n"

        self.last_moves_var.set(f"Last Moves: \n" + moves_desc_readable)

        best_move = self.get_ai_move()
        self.recommended_move_var.set(self.game.describe_move(best_move))
        self.draw_board()

    def take_back_turn(self):
        try:
            self.game.board.pop()
            self.game.board.pop()
            self.move_descs.pop(0)
            self.move_descs.pop(0)
        except IndexError:
            return
        self.refresh_gui()

    def draw_board(self):
        for widget in self.board_outer_frame.winfo_children():
            widget.destroy()
        board_frame = self.get_board_frame(self.board_outer_frame, self.game.board)
        board_frame.pack()

    def get_board_frame(self, master, board):
        board_frame = Frame(master)
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    c = "#563a12"
                else:
                    c = "#9f9362"

                square = coordinates_to_square(row, col)
                piece = board.piece_at(square)
                if piece:
                    img = self.images[(piece.color, piece.piece_type)]
                    btn = Button(board_frame, bg=c, height=height_of_square, width=width_of_square, image=img, command=partial(self.handle_click, square))
                else:
                    btn = Button(board_frame, bg=c, height=4, width=8, command=partial(self.handle_click, square))

                btn.grid(row=row, column=col)
        return board_frame

    def handle_click(self, square):
        if self.selected_origin is None:
            self.selected_origin = square
            return

        requested_move_normal = chess.Move(self.selected_origin, square)
        requested_move_promotion = chess.Move(self.selected_origin, square, chess.QUEEN)

        if self.game.board.is_legal(requested_move_promotion):
            self.make_manual_move(requested_move_promotion)
        elif self.game.board.is_legal(requested_move_normal):
            self.make_manual_move(requested_move_normal)
        else:
            self.selected_origin = square

    def make_manual_move(self, move):
        self.move_descs.insert(0, self.game.describe_move(move))
        self.game.board.push(move)
        self.refresh_gui()
        self.selected_origin = None

        if not self.game.board.outcome():
            self.make_ai_move()
        self.refresh_gui()

    def get_ai_move(self):
        if self.game.board.turn:    # determines if its whites or blacks turn
            method = self.selected_ai_white
        else:
            method = self.selected_ai_black
        return self.game.get_best_move(method)

    def make_ai_move(self):
        move = self.get_ai_move()
        self.move_descs.insert(0, self.game.describe_move(move))
        self.game.board.push(move)


if __name__ == "__main__":
    GUI()

