import time
from game import Game
from flask import (
    Flask,
    render_template,
    request,
    session,
    jsonify,
)
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session management

# Initialize the game
games = {}

strategy_name_mapping = {
    "random": "Random Strategy",
    "terrible_player": "Beginner",
    "minimax_2": "Minimax (2 Turns)",
    "minimax_3": "Minimax (3 Turns)",
    "minimax_4": "Minimax (4 Turns)",
    "minimax_5": "Minimax (5 Turns)",
    "minimax_auto": "Minimax Auto",
    "mcts_1s": "MCTS (1 second)",
    "mcts_3s": "MCTS (3 seconds)",
    "mcts_6s": "MCTS (6 seconds)",
    "mcts_10s": "MCTS (10 seconds)",
}


def get_game():
    return games[session["identifier"]]


def init_session():
    if "selected_file" not in session:
        session["selected_file"] = None
    if "selected_rank" not in session:
        session["selected_rank"] = None
    if "possible_targets" not in session:
        session["possible_targets"] = []
    if "ai_method" not in session:
        session["ai_method"] = "minimax_4"

    if not "identifier" in session:
        session["identifier"] = f"{time.time()}_{request.remote_addr}"
    if not session["identifier"] in games:
        games[session["identifier"]] = Game()


@app.route("/session/")
def show_session():
    return jsonify(session)


@app.route("/", methods=["GET", "POST"])
def index():
    init_session()
    game = get_game()
    if request.method == "POST":
        if "undo" in request.form:
            if len(game.board.move_stack) >= 2:
                game.board.pop()
                game.board.pop()
        elif "reset" in request.form:
            session["selected_rank"] = None
            session["selected_file"] = None
            games[session["identifier"]] = Game()
            game = get_game()
        elif "ai_method" in request.form:
            session["ai_method"] = request.form.get("ai_method")
        elif (
            "row" in request.form
            and "col" in request.form
            and not game.board.is_game_over()
        ):
            selected_rank = int(request.form.get("row"))
            selected_file = int(request.form.get("col"))

            if (selected_rank, selected_file) in session["possible_targets"]:
                # the user moved here
                move = game.get_move_from_coords(
                    (session["selected_rank"], session["selected_file"]),
                    (selected_rank, selected_file),
                )
                game.board.push(move)
                session["selected_rank"] = None
                session["selected_file"] = None
            elif (selected_rank == session["selected_rank"]) and (
                selected_file == session["selected_file"]
            ):
                # the user deselected his selection
                session["selected_rank"] = None
                session["selected_file"] = None
            else:
                # the user made a new selection
                session["selected_rank"] = selected_rank
                session["selected_file"] = selected_file

    if not game.board.turn and not game.board.is_game_over():
        move = game.get_best_move(session["ai_method"])
        game.board.push(move)

    if not session["selected_rank"] is None:
        selected_square = session["selected_rank"], session["selected_file"]
        _, session["possible_targets"] = game.get_moves_for_field(selected_square)
    else:
        session["possible_targets"] = []

    return render_template(
        "index.html",
        fen=game.board.fen(),
        board_image=get_board_image(),
        possible_targets=session["possible_targets"],
        selected_square=(session["selected_rank"], session["selected_file"]),
        ai_method=strategy_name_mapping[session["ai_method"]],
    )


def get_board_image():
    game = get_game()
    img = game.get_board_image()
    return img.encode().decode()


if __name__ == "__main__":
    app.run(debug=False)
