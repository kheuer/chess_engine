import numpy as np

positional_scaling_factor = 0.3 # 0.8
positional_scaling_factor_early_to_midgame_itself = 1
positional_scaling_factor_endgame_itself = 1.2


raw_positions_white_early_to_midgame = {
    6: 1 * np.array([2, 3, 1, 0, 0, 1, 3, 2, 2, 2, 0, 0, 0, 0, 2, 2, -1, -2, -2, -2, -2, -2, -2, -1, -2, -3, -3, -4, -4, -3, -3, -2, -3, -3, -4, -5, -5, -4, -4, -3, -3, -3, -4, -5, -5, -4, -4, -3, -3, -3, -4, -5, -5, -4, -4, -3, -3, -3, -4, -5, -5, -4, -4, -3]),
    5: 8 * np.array([-2, -1, -1, -0.5, -0.5, -1, -1, 2, -1, 0, 0.5, 0, 0, 0, 0, -1, -1, 0.5, 0.5, 0.5, 0.5, 0.5, 0, -1, 0, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5, -0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5, -1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1, -1, 0, 0, 0, 0, 0, 0, -1, -2, -1, -1, -0.5, -0.5, -1, -1, -2]),
    4: 15 * np.array([0, 0, 0, 0.5, 0.5, 0, 0, 0, -0.5, 0, 0, 0, 0, 0, 0, -0.5, -0.5, 0, 0, 0, 0, 0, 0, -0.5, -0.5, 0, 0, 0, 0, 0, 0, -0.5, -0.5, 0, 0, 0, 0, 0, 0, -0.5, -0.5, 0, 0, 0, 0, 0, 0, -0.5, 0.5, 1, 1, 1, 1, 1, 1, 0.5, 0, 0, 0, 0, 0, 0, 0, 0]),
    3: 8 * np.array([-2, -1, -1, -1, -1, -1, -1, -2, -1, 0.5, 0, 0, 0, 0, 0.5, -1, -1, 1, 1, 1, 1, 1, 1, -1, -1, 0, 1, 1, 1, 1, 0, -1, -1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1, -1, 0, 0.5, 1, 1, 0.5, 0, -1, -1, 0, 0, 0, 0, 0, 0, -1, -2, -1, -1, -1, -1, -1, -1, -2]),
    2: 4 * np.array([-5, -4, -3, -3, -3, -3, -4, -5, -4, -2, 0, 0.5, 0.5, 0, -2, -4, -3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3, -3, 0, 1.5, 2, 2, 1.5, 0, -3, -3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3, -3, 0, 1, 1.5, 1.5, 1, 0, -3, -4, -2, 0, 0, 0, 0, -2, -4, -5, -4, -3, -3, -3, -3, -4, -5]),
    1: 3 * np.array([0, 0, 0, 0, 0, 0, 0, 0, 0.5, 1, 1, -0.5, -0.5, 1, 1, 0.5, 0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5, 0, 0, 0, 2, 2, 0, 0, 0, 0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5, 1, 1, 2, 3, 3, 2, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0])
}



piece_square_tables_white_early_to_midgame = {
    6: list(positional_scaling_factor * positional_scaling_factor_early_to_midgame_itself * raw_positions_white_early_to_midgame[6]),
    5: list(positional_scaling_factor * positional_scaling_factor_early_to_midgame_itself * raw_positions_white_early_to_midgame[5]),
    4: list(positional_scaling_factor * positional_scaling_factor_early_to_midgame_itself * raw_positions_white_early_to_midgame[4]),
    3: list(positional_scaling_factor * positional_scaling_factor_early_to_midgame_itself * raw_positions_white_early_to_midgame[3]),
    2: list(positional_scaling_factor * positional_scaling_factor_early_to_midgame_itself * raw_positions_white_early_to_midgame[2]),
    1: list(positional_scaling_factor * positional_scaling_factor_early_to_midgame_itself * raw_positions_white_early_to_midgame[1])
}

piece_square_tables_black_early_to_midgame = {
    6: list(reversed(piece_square_tables_white_early_to_midgame[6])),
    5: list(reversed(piece_square_tables_white_early_to_midgame[5])),
    4: list(reversed(piece_square_tables_white_early_to_midgame[4])),
    3: list(reversed(piece_square_tables_white_early_to_midgame[3])),
    2: list(reversed(piece_square_tables_white_early_to_midgame[2])),
    1: list(reversed(piece_square_tables_white_early_to_midgame[1]))
}

piece_square_tables_early_to_midgame = {
    True: piece_square_tables_white_early_to_midgame,
    False: piece_square_tables_black_early_to_midgame
}

raw_positions_white_endgame = {
    1: 10 * np.array([0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.5000000, 1.0000000, 1.0000000, -2.0000000, -2.0000000, 1.0000000, 1.0000000, 0.5000000, 0.5000000, -0.5000000, -1.0000000, 0.0000000, 0.0000000, -1.0000000, -0.5000000, 0.5000000, 0.0000000, 0.0000000, 0.0000000, 2.0000000, 2.0000000, 0.0000000, 0.0000000, 0.0000000, 0.5000000, 0.5000000, 1.0000000, 2.5000000, 2.5000000, 1.0000000, 0.5000000, 0.5000000, 1.0000000, 1.0000000, 2.0000000, 3.0000000, 3.0000000, 2.0000000, 1.0000000, 1.0000000, 5.0000000, 5.0000000, 5.0000000, 5.0000000, 5.0000000, 5.0000000, 5.0000000, 5.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000]),
    2: 1 * np.array([-24.0000000, -21.0000000, -18.0000000, -18.0000000, -18.0000000, -18.0000000, -21.0000000, -24.0000000, -21.0000000, -18.0000000, 0.0000000, 3.0000000, 3.0000000, 0.0000000, -18.0000000, -21.0000000, -18.0000000, 0.0000000, 9.0000000, 6.0000000, 6.0000000, 9.0000000, 0.0000000, -18.0000000, -18.0000000, 8.0000000, 12.0000000, 15.0000000, 15.0000000, 12.0000000, 8.0000000, -18.0000000, -18.0000000, 6.0000000, 16.5000000, 18.0000000, 18.0000000, 16.5000000, 6.0000000, -18.0000000, -18.0000000, 3.0000000, 18.0000000, 16.5000000, 16.5000000, 18.0000000, 3.0000000, -18.0000000, -21.0000000, -18.0000000, 6.0000000, 9.0000000, 9.0000000, 6.0000000, -18.0000000, -21.0000000, -24.0000000, -21.0000000, -18.0000000, -18.0000000, -18.0000000, -18.0000000, -21.0000000, -24.0000000]),
    3: 1 * np.array([-12.0000000, -9.0000000, -6.0000000, -6.0000000, -6.0000000, -6.0000000, -9.0000000, -12.0000000, -11.0000000, 12.0000000, 9.0000000, 6.0000000, 6.0000000, 9.0000000, 12.0000000, -11.0000000, -9.0000000, 9.0000000, 15.0000000, 12.0000000, 12.0000000, 15.0000000, 9.0000000, -9.0000000, 6.0000000, 6.0000000, 15.0000000, 18.0000000, 18.0000000, 15.0000000, 6.0000000, 6.0000000, 6.0000000, 18.0000000, 18.0000000, 21.0000000, 21.0000000, 18.0000000, 18.0000000, 6.0000000, 6.0000000, 12.0000000, 18.0000000, 21.0000000, 21.0000000, 18.0000000, 12.0000000, 6.0000000, 0.0000000, 12.0000000, 6.0000000, 6.0000000, 6.0000000, 6.0000000, 12.0000000, 0.0000000, -6.0000000, -4.8000000, -4.6000000, -2.4000000, -2.4000000, -4.6000000, -4.8000000, -6.0000000]),
    4: 1 * np.array([0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000]),
    5: 0.4 * np.array([-30.0000000, -25.0000000, -15.0000000, -10.0000000, -10.0000000, -15.0000000, -25.0000000, -30.0000000, -15.0000000, -10.0000000, 0.0000000, 10.0000000, 10.0000000, 0.0000000, -10.0000000, -15.0000000, 0.0000000, 15.0000000, 30.0000000, 40.0000000, 40.0000000, 30.0000000, 15.0000000, 0.0000000, 10.0000000, 25.0000000, 40.0000000, 50.0000000, 50.0000000, 40.0000000, 25.0000000, 10.0000000, 10.0000000, 25.0000000, 40.0000000, 50.0000000, 50.0000000, 40.0000000, 25.0000000, 10.0000000, 10.0000000, 25.0000000, 40.0000000, 50.0000000, 50.0000000, 40.0000000, 25.0000000, 10.0000000, 0.0000000, 20.0000000, 35.0000000, 45.0000000, 45.0000000, 35.0000000, 20.0000000, 0.0000000, -10.0000000, 10.0000000, 15.0000000, 20.0000000, 20.0000000, 15.0000000, 10.0000000, -10.0000000]),
    6: 0.25 * np.array([-20.0000000, 0.0000000, 0.0000000, -10.0000000, -10.0000000, 0.0000000, 0.0000000, -20.0000000, -30.0000000, -30.0000000, -30.0000000, -35.0000000, -35.0000000, -30.0000000, -30.0000000, -30.0000000, -40.0000000, -40.0000000, -45.0000000, -50.0000000, -50.0000000, -45.0000000, -40.0000000, -40.0000000, -50.0000000, -50.0000000, -55.0000000, -60.0000000, -60.0000000, -55.0000000, -50.0000000, -50.0000000, -55.0000000, -55.0000000, -60.0000000, -70.0000000, -70.0000000, -60.0000000, -55.0000000, -55.0000000, -55.0000000, -55.0000000, -60.0000000, -70.0000000, -70.0000000, -60.0000000, -55.0000000, -55.0000000, -55.0000000, -55.0000000, -60.0000000, -70.0000000, -70.0000000, -60.0000000, -55.0000000, -55.0000000, -55.0000000, -55.0000000, -60.0000000, -70.0000000, -70.0000000, -60.0000000, -55.0000000, -55.0000000])
}


piece_square_tables_white_endgame = {
    6: list(positional_scaling_factor * positional_scaling_factor_endgame_itself * raw_positions_white_endgame[6]),
    5: list(positional_scaling_factor * positional_scaling_factor_endgame_itself * raw_positions_white_endgame[5]),
    4: list(positional_scaling_factor * positional_scaling_factor_endgame_itself * raw_positions_white_endgame[4]),
    3: list(positional_scaling_factor * positional_scaling_factor_endgame_itself * raw_positions_white_endgame[3]),
    2: list(positional_scaling_factor * positional_scaling_factor_endgame_itself * raw_positions_white_endgame[2]),
    1: list(positional_scaling_factor * positional_scaling_factor_endgame_itself * raw_positions_white_endgame[1])
}

piece_square_tables_black_endgame = {
    6: list(reversed(piece_square_tables_white_endgame[6])),
    5: list(reversed(piece_square_tables_white_endgame[5])),
    4: list(reversed(piece_square_tables_white_endgame[4])),
    3: list(reversed(piece_square_tables_white_endgame[3])),
    2: list(reversed(piece_square_tables_white_endgame[2])),
    1: list(reversed(piece_square_tables_white_endgame[1]))
}

piece_square_tables_endgame = {
    True: piece_square_tables_white_endgame,
    False: piece_square_tables_black_endgame
}



pieces = {1: "Pawn", 2: "Knight", 3: "Bishop", 4: "Rook", 5: "Queen", 6: "King"}



if __name__ == "__main__":
    for piece, table in piece_square_tables_early_to_midgame[True].items():
        print(pieces[piece])
        t = np.array(table)

        for row in reversed(t.reshape((8, 8))):
            print(list([round(x) for x in row]))
        print()




