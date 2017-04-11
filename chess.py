import copy

def initialise_board():
    # Initialise the 8x8 board matrix
    # Extra top layer to make it same in dimension to the display board
    # doing board = [["_"] * 8] * 9 creates 9 sets of the same list,
    # so altering any element changes that element for each list;
    # need board = [["_"] * 8 for i in range(9)] so that each of those
    # 9 lists are independent
    board = [["_"] * 8 for i in range(9)]
    pieces = [[], []]
    pieces[0] = ["Rb", "Kb", "Bb", "Qb", "+b", "Bb", "Kb", "Rb", "Pb"]
    pieces[1] = ["Rw", "Kw", "Bw", "Qw", "+w", "Bw", "Kw", "Rw", "Pw"]
    # Black side (top)
    board[1] = pieces[0][:-1]
    board[2] = [pieces[0][-1]] * 8

    # White side (bottom)
    board[8] = pieces[1][:-1]
    board[7] = [pieces[1][-1]] * 8

    #print(board[0])
    #print(board[1])
    #print(board[2])
    #print(board[6])
    #print(board[7])

    return board

def display_board(board_):
    board = copy.deepcopy(board_)
    board[0] = [" ____"] * 8
    for i in range(1, 9):
        for j in range(8):
            if board[i][j].find("b") == -1 and \
               board[i][j].find("w") == -1:
               board[i][j] = "|____"
            elif board[i][j].find("b") != -1:
                s = board[i][j]
                if len(s) == 2:
                    board[i][j] = "|_" + s + "_"
                else:
                    board[i][j] = "|_" + s[s.find("b") - 1: s.find("b") + 1]
            elif board[i][j].find("w") != -1:
                s = board[i][j]
                if len(s) == 2:
                    board[i][j] = "|_" + s + "_"
                else:
                    board[i][j] = "|_" + s[s.find("w") - 1: s.find("w") + 1]
        board[i][7] += "|"

    print("   ", end = "")
    for i in range(8): print(board[0][i], end = "")
    print()
    for i in range(1, 9):
        print(9 - i, " ", end = "")
        for j in range(8):
            print(board[i][j], end = "")
        print()
    print("      a    b    c    d    e    f    g    h")
    print()

def get_move(board):
    print("Move example: a2 to a4")
    letters = "abcdefgh"
    move = input("Enter move (-1 to exit): ")
    move = move.split()
    if move[0] == "-1": return [-1]
    position = ["row 1", "col 1", "row 2", "col 2"]
    # Rows are numbers (9 - i), cols are letters (a - h)
    position[0] = 9 - int(move[0][1])
    position[1] = letters.find(move[0][0])
    position[2] = 9 - int(move[2][1])
    position[3] = letters.find(move[2][0])
    while not(move_is_valid(board, position)):
        print("Invalid move.")
        move = input("Enter move (-1 to exit): ")
        move = move.split()
        if move[0] == "-1": return [-1]
        position = ["row 1", "col 1", "row 2", "col 2"]
        # Rows are numbers (9 - i), cols are letters (a - h)
        position[0] = 9 - int(move[0][1])
        position[1] = letters.find(move[0][0])
        position[2] = 9 - int(move[2][1])
        position[3] = letters.find(move[2][0])
        
    print(position)
    return position

def move_piece(board, move):
    board[move[2]][move[3]] = board[move[0]][move[1]]
    board[move[0]][move[1]] = "_"
    return board

def print_board_matrix(board):
    for i in range(9):
        print(board[i])

def remove_overlap(board, move):
    # move current piece to "graveyard"
    # replace current piece with new piece
    # (so long as the move was valid)
    pass

def move_is_valid(board, move):
    # Invalid when:
    # - Out of bounds
    # - No piece chosen
    # - Piece movement doesn't match
    #   piece movement pattern (e.g.
    #   a bishop moving straight up is
    #   invalid)
    # - The pattern is obstructed by
    #   another piece (exceptions:
    #   knight, king + castle swap
    #   (castling))
    # - The destination contains a
    #   piece from the same team
    b = board
    m = move
    piece = b[m[0]][m[1]]
    pos_i = m[0:2]
    pos_f = m[2:4]
    # Forward movement of a white piece is
    # the reverse of a black piece, but
    # horizontal movement is the same
    # i.e. forward: b 1 -> 8/ w 8 -> 1,
    #      horizontal: b 0 -> 7/ w 0 -> 7

    if out_of_bounds(m): return False
    if piece == "_": return False

    # right_movement > 0 means pos_f is to
    # the right of pos_i, and
    # right_movement < 0 means pos_f is to
    # the left of pos_i
    if piece[1] == "w":
        forward_movement = pos_i[0] - pos_f[0]
        right_movement = pos_f[1] - pos_i[1]
    elif piece[1] == "b":
        forward_movement = pos_f[0] - pos_i[0]
        right_movement = pos_f[1] - pos_i[1]

    # - Check piece patterns in the order:
    #   pawn, rook, knight, bishop, queen, king
    # - Remember that moving forward is 1 -> 8
    #   for black pieces and 8 -> 1 for white
    #   pieces
    if piece[0] == "P":
        if pos_f[1] != pos_i[1]:
            # Diagonal movement only allowed
            # if taking an opponent's piece
            if not((pos_f[1] == pos_i[1] + 1 or\
                   pos_f[1] == pos_i[1] - 1) and\
                   forward_movement == 1):
                return False           
        if forward_movement > 2: return False
        if forward_movement < -1: return False
        # - Two steps forward is only valid if the
        #   pawn is currently in its initial position
        if forward_movement == 2:            
            if piece[1] == "w" and pos_i[0] != 7: return False
            if piece[1] == "b" and pos_i[0] != 2: return False
                
    elif piece[0] == "R":
        # Invalid if it moves diagonally
        if pos_f[1] != pos_i[1]: return False

    elif piece[0] == "K": pass

    elif piece[0] == "B":
        # Invalid if it moves vertically
        # without moving horizontally an
        # equal amount
        if abs(forward_movement) != abs(right_movement):
            return False

    elif piece[0] == "Q":
        # The queen can either move like a rook
        # or like a bishop, but not both
        if forward_movement != 0 and right_movement != 0:
            if abs(forward_movement) != abs(right_movement):
                return False

    elif piece[0] == "+": pass
    

    return True

def out_of_bounds(move):
    if move[0] < 1 or move[0] > 8: return True
    if move[1] < 0 or move[1] > 7: return True
    if move[2] < 1 or move[0] > 8: return True
    if move[3] < 0 or move[1] > 7: return True
    return False

def clear_screen():
    print("\n" * 50)

def get_removed_pieces(board, move):
    pass

def main():
    # TODO:
    # - Tidy up positional comparisons
    #   with helper functions,
    #   e.g. is_diagonal_to() instead of
    #   comparing coordinates

    board = initialise_board()
    moves_left = 5
    for i in range(5):
        clear_screen()      
        display_board(board)
        print("Moves left:", moves_left)
        move = get_move(board)
        if move[0] == -1: break
        board = move_piece(board, move)
        moves_left -= 1
        
main()
 
