import sys


def create_piece(symbol, piece_type, i, j, team):
    # returns a dict with the piece's info
    # symbol (str): piece's symbol displayed on the board
    # piece_type (str): piece's type
    # i (int): row
    # j (int): column
    # team (str): "white" or "black"

    return {
        "symbol": symbol,
        "piece_type": piece_type,
        "i": i,
        "j": j,
        "active": True,
        "team": team
    }


def is_pos_valid(i, j):
    # checks whether i and j are between 0 and 7, returns a boolean value

    return (i >= 0 and i <= 7) and (j >= 0 and j <= 7)


def initialize_board():
    # returns a list of dicts that contains the pieces

    pieces = []
    pieces.append(create_piece("R1", "rook", 0, 0, "black"))
    pieces.append(create_piece("N1", "knight", 0, 1, "black"))
    pieces.append(create_piece("B1", "bishop", 0, 2, "black"))
    pieces.append(create_piece("QU", "queen", 0, 3, "black"))
    pieces.append(create_piece("KI", "king", 0, 4, "black"))
    pieces.append(create_piece("B2", "bishop", 0, 5, "black"))
    pieces.append(create_piece("N2", "knight", 0, 6, "black"))
    pieces.append(create_piece("R2", "rook", 0, 7, "black"))

    pieces.append(create_piece("r1", "rook", 7, 0, "white"))
    pieces.append(create_piece("n1", "knight", 7, 1, "white"))
    pieces.append(create_piece("b1", "bishop", 7, 2, "white"))
    pieces.append(create_piece("qu", "queen", 7, 3, "white"))
    pieces.append(create_piece("ki", "king", 7, 4, "white"))
    pieces.append(create_piece("b2", "bishop", 7, 5, "white"))
    pieces.append(create_piece("n2", "knight", 7, 6, "white"))
    pieces.append(create_piece("r2", "rook", 7, 7, "white"))

    # create pawns in a loop
    for i in range(8):
        pieces.append(create_piece(f"P{i+1}", "pawn", 1, i, "black"))
        pieces.append(create_piece(f"p{i+1}", "pawn", 6, i, "white"))

    return pieces


def get_block_name(position):
    # returns the block's name as string
    # position (list): coordinates in [i, j] format
    return ["a", "b", "c", "d", "e", "f", "g", "h"][position[1]]+str(8-position[0])


def get_block_position(name):
    # returns two values, the block coordinates in i, j format
    # name (str): block's name

    name = name.strip()
    letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
    return 8 - int(name[1]), letters.index(name[0])


def get_board(pieces):
    # creates and returns a two dimensional list
    # where empty blocks are None and filled blocks contain the pieces
    # pieces (list): list of pieces

    board = [[None for _ in range(8)] for _ in range(8)]
    for piece in pieces:
        if piece["active"]:
            board[piece["i"]][piece["j"]] = piece

    return board


def calculate_rook_moves(piece, pieces):
    # returns possible moves for the given rook piece in a list of [i, j] format
    # piece (dict): piece to be processed
    # pieces (list): list of pieces

    moves = []
    board = get_board(pieces)
    for step in [-1, 1]:
        for direction in ["i", "j"]:
            step_i = step if direction == "i" else 0
            step_j = step if direction == "j" else 0

            i = piece["i"]+step_i
            j = piece["j"]+step_j

            while is_pos_valid(i, j):
                if board[i][j] is not None:
                    if board[i][j]["team"] != piece["team"] and board[i][j]["piece_type"] != "king":
                        moves.append([i, j])
                    break
                else:
                    moves.append([i, j])

                i += step_i
                j += step_j

    return moves


def calculate_knight_moves(piece, pieces):
    # returns possible moves for the given knight piece in a list of [i, j] format
    # piece (dict): piece to be processed
    # pieces (list): list of pieces

    moves = []
    board = get_board(pieces)
    diagonal = [[piece["i"]+step1, piece["j"]+step2]
                for step1 in [-1, 1] for step2 in [-1, 1]]

    moves += [pos for pos in diagonal if is_pos_valid(
        pos[0], pos[1]) and board[pos[0]][pos[1]] is None]

    l_shape = [[piece["i"]+step1, piece["j"]+step2] for step1 in [-2, -1, 1, 2]
               for step2 in [-2, -1, 1, 2] if abs(step1) != abs(step2)]

    for pos in l_shape:
        if is_pos_valid(pos[0], pos[1]):
            p = board[pos[0]][pos[1]]
            if p is None:
                moves.append([pos[0], pos[1]])
            else:
                if p["team"] != piece["team"] and p["piece_type"] != "king":
                    moves.append([pos[0], pos[1]])

    moves = [pos for pos in moves if is_pos_valid(pos[0], pos[1])]

    return moves


def calculate_bishop_moves(piece, pieces):
    # returns possible moves for the given bishop piece in a list of [i, j] format
    # piece (dict): piece to be processed
    # pieces (list): list of pieces

    moves = []
    board = get_board(pieces)
    step = 1 if piece["team"] == "black" else -1

    for k in [-1, 1]:
        i = piece["i"]+step
        j = piece["j"]+k
        while is_pos_valid(i, j):
            if board[i][j] is not None:
                if board[i][j]["team"] != piece["team"] and board[i][j]["piece_type"] != "king":
                    moves.append([i, j])
                break
            else:
                moves.append([i, j])
            i += step
            j += k

    return moves


def calculate_queen_moves(piece, pieces):
    # returns possible moves for the given queen piece in a list of [i, j] format
    # piece (dict): piece to be processed
    # pieces (list): list of pieces

    moves = []
    board = get_board(pieces)

    for k in [-1, 1]:
        for l in [-1,1]:
            i = piece["i"]+l
            j = piece["j"]+k
            while is_pos_valid(i, j):
                if board[i][j] is not None:
                    if board[i][j]["team"] != piece["team"] and board[i][j]["piece_type"] != "king":
                        moves.append([i, j])
                    break
                else:
                    moves.append([i, j])
                i += l
                j += k

    return calculate_rook_moves(piece, pieces) + moves


def calculate_king_moves(piece, pieces):
    # returns possible moves for the given king piece in a list of [i, j] format
    # piece (dict): piece to be processed
    # pieces (list): list of pieces

    moves = []
    board = get_board(pieces)
    for i in range(-1, 2):
        for j in range(-1, 2):
            row = piece["i"]+i
            col = piece["j"]+j
            if is_pos_valid(row, col):
                target = board[row][col]
                if target is None or (target["team"] != piece["team"] and target["piece_type"] != "king"):
                    moves.append([row, col])

    return moves


def calculate_pawn_moves(piece, pieces):
    # returns possible moves for the given pawn piece in a list of [i, j] format
    # piece (dict): piece to be processed
    # pieces (list): list of pieces

    board = get_board(pieces)
    row = piece["i"]+1 if piece["team"] == "black" else piece["i"]-1
    col = piece["j"]
    if is_pos_valid(row, col):
        target = board[row][col]
        if target is None or (target["team"] != piece["team"] and target["piece_type"] != "king"):
            return [[row, col]]

    return []


def calculate_moves(piece, pieces):
    # returns possible moves for the given piece in a list of [i, j] format
    # piece (dict): piece to be processed
    # pieces (list): list of pieces

    if piece["piece_type"] == "rook":
        moves = calculate_rook_moves(piece, pieces)

    elif piece["piece_type"] == "knight":
        moves = calculate_knight_moves(piece, pieces)

    elif piece["piece_type"] == "bishop":
        moves = calculate_bishop_moves(piece, pieces)

    elif piece["piece_type"] == "queen":
        moves = calculate_queen_moves(piece, pieces)

    elif piece["piece_type"] == "king":
        moves = calculate_king_moves(piece, pieces)

    else:
        moves = calculate_pawn_moves(piece, pieces)

    moves.sort(key=lambda p: p[0], reverse=True)
    moves.sort(key=lambda p: p[1])
    return moves


def print_board(pieces):
    # prints the board to the console
    # pieces (list): list of pieces

    blocks = [["  " for _ in range(8)] for _ in range(8)]
    for piece in pieces:
        if piece["active"]:
            blocks[piece["i"]][piece["j"]] = piece["symbol"]

    print("-"*24)
    print("\n".join([" ".join(row) for row in blocks]))
    print("-"*24)


def print_moves(piece, pieces):
    # possible possible moves for the given piece
    # piece (dict): piece to be processed
    # pieces (list): list of pieces

    moves = calculate_moves(piece, pieces)
    print(" ".join(get_block_name(pos)
                   for pos in moves) if len(moves) > 0 else "FAILED")


def move_to_position(piece, pieces, i, j):
    # attempts to move the given piece to the given position
    # and returns a boolean stating the success of the operation
    # piece (dict): piece to be moved
    # pieces (list): list of pieces
    # i (int): target block's row index
    # i (int): target block's column index

    if [i, j] not in calculate_moves(piece, pieces):
        return False

    target = get_board(pieces)[i][j]
    if target is not None:
        target["i"] = None
        target["j"] = None
        target["active"] = False

    piece["i"] = i
    piece["j"] = j
    return True


if __name__ == "__main__":
    pieces = initialize_board()

    f = open(sys.argv[1], "r")
    commands = [line.split() for line in f.readlines()]
    f.close()

    for command in commands:
        print("> "+" ".join(command))

        if command[0] == "initialize":
            pieces = initialize_board()
            print_board(pieces)

        elif command[0] == "showmoves":
            piece = [p for p in pieces if p["symbol"] == command[1]][0]
            print_moves(piece, pieces)

        elif command[0] == "move":
            piece = [p for p in pieces if p["symbol"] == command[1]][0]
            i, j = get_block_position(command[2])
            print("OK" if move_to_position(piece, pieces, i, j) else "FAILED")

        elif command[0] == "print":
            print_board(pieces)

        elif command[0] == "exit":
            break
