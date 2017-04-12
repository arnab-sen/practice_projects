import copy
import random

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

def display_board_old(board_):
    # This version has the original notation for
    # the pieces (e.g. white pawn = Pw)
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

def get_piece_image(piece):
    # Return a fancy unicode version of
    # a piece
    # e.g. "Kb" --> "♞" (black knight)
    new_piece = "!"
    if piece[0] == "P":
        if piece[1] == "w": return "♙"
        elif piece[1] == "b": return "♟"
    if piece[0] == "R":
        if piece[1] == "w": return "♖"
        elif piece[1] == "b": return "♜"
    if piece[0] == "K":
        if piece[1] == "w": return "♘"
        elif piece[1] == "b": return "♞"
    if piece[0] == "B":
        if piece[1] == "w": return "♗"
        elif piece[1] == "b": return "♝"
    if piece[0] == "Q":
        if piece[1] == "w": return "♕"
        elif piece[1] == "b": return "♛"
    if piece[0] == "+":
        if piece[1] == "w": return "♔"
        elif piece[1] == "b": return "♚"
    return new_piece

def display_board(board_):
    # This version has the new unicode versions
    # of the pieces (e.g. white pawn = ♙)
    board = copy.deepcopy(board_)
    board[0] = ["____"] * 7 + ["___"]
    for i in range(1, 9):
        for j in range(8):
            if board[i][j].find("b") == -1 and \
               board[i][j].find("w") == -1:
                board[i][j] = "|___"
            else:
                s = get_piece_image(board[i][j])
                if j <= 2: board[i][j] = "|_" + s
                elif j >= 5: board[i][j] = "|" + s + "_"
                else: board[i][j] = "|_" + s + "_"
        board[i][7] += "|"

    print("   ", end = "")
    for i in range(8): print(board[0][i], end = "")
    print()
    for i in range(1, 9):
        print(9 - i, "", end = "")
        for j in range(8):
            print(board[i][j], end = "")
        print()
    print("    a   b   c   d   e   f   g   h")
    print()

def get_cpu_move(board, player):
    cpu = True
    position = ["", "", "", ""]
    position[0] = random.randrange(1, 9)
    position[1] = random.randrange(8)
    position[2] = random.randrange(1, 9)
    position[3] = random.randrange(8)
    
    while not(move_is_valid(board, position, player, cpu)):
        position[0] = random.randrange(1, 9)
        position[1] = random.randrange(8)
        position[2] = random.randrange(1, 9)
        position[3] = random.randrange(8)
        
    #print(position)
    return position

def get_move(board, player):
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
    while not(move_is_valid(board, position, player, False)):
        print("Invalid move")
        move = input("Enter move (-1 to exit): ")
        move = move.split()
        if move[0] == "-1": return [-1]
        position = ["row 1", "col 1", "row 2", "col 2"]
        # Rows are numbers (9 - i), cols are letters (a - h)
        position[0] = 9 - int(move[0][1])
        position[1] = letters.find(move[0][0])
        position[2] = 9 - int(move[2][1])
        position[3] = letters.find(move[2][0])
        
    #print(position)
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

def get_forward_movement(piece, move):
    # Forward movement of a white piece is
    # the reverse of a black piece, but
    # horizontal movement is the same
    # i.e. forward: b 1 -> 8/ w 8 -> 1,
    #      horizontal: b 0 -> 7/ w 0 -> 7
    # right_movement > 0 means pos_f is to
    # the right of pos_i, and
    # right_movement < 0 means pos_f is to
    # the left of pos_i
    pos_i = move[0:2]
    pos_f = move[2:4]
    forward_movement = 0
    if piece[1] == "w":
        forward_movement = pos_i[0] - pos_f[0]
    elif piece[1] == "b":
        forward_movement = pos_f[0] - pos_i[0]
    return forward_movement

def get_right_movement(piece, move):
    pos_i = move[0:2]
    pos_f = move[2:4]
    right_movement = 0
    if piece[1] == "w" or piece[1] == "b":
        right_movement = pos_f[1] - pos_i[1]
    return right_movement

def valid_movement_pattern(board, piece, move):
    pos_i = move[0:2]
    pos_f = move[2:4]
    forward_movement = get_forward_movement(piece, move)
    right_movement= get_right_movement(piece, move)
    
    # - Check piece patterns in the order:
    #   pawn, rook, knight, bishop, queen, king
    # - Remember that moving forward is 1 -> 8
    #   for black pieces and 8 -> 1 for white
    #   pieces
    if piece[0] == "P":      
        if pos_f[1] != pos_i[1]:
            # Diagonal movement only allowed
            # if taking an opponent's piece
            if not(overlap_with_enemy(board, move)): return False
            if forward_movement == 0: return False
            if forward_movement == 1 and abs(right_movement) > 1: return False
            if forward_movement == -1 and abs(right_movement) > 0: return False
        if forward_movement > 2: return False
        if forward_movement < -1: return False
        # - Two steps forward is only valid if the
        #   pawn is currently in its initial position
        if forward_movement == 2:            
            if piece[1] == "w" and pos_i[0] != 7: return False
            if piece[1] == "b" and pos_i[0] != 2: return False
                
    elif piece[0] == "R":
        # Invalid if it moves diagonally
        if abs(forward_movement) != 0 and\
           abs(right_movement) != 0: return False

    elif piece[0] == "K":
        # Can only move in an L shape variant,
        # i.e. vertically 2, horizontally 1 or
        #      vertically 1, horizontally 2
        if not(abs(forward_movement) * abs(right_movement)) == 2:
            return False

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

    elif piece[0] == "+":
        # Moves exactly like a queen except
        # neither its vertical nor horizontal
        # movement can exceed one square
        if abs(forward_movement) > 1 or abs(right_movement) > 1:
            return False

    return True

def moving_opponent_piece(board, move, player):
    b = board
    m = move
    piece = b[m[0]][m[1]]
    
    if player == 1:
        if piece[1] == "b": return True
    if player == 2:
        if piece[1] == "w": return True

    return False

def move_is_valid(board, move, player, cpu):
    b = board
    m = move
    piece = b[m[0]][m[1]]
    
    # Invalid when:
    # - Out of bounds
    if out_of_bounds(m):
        if not(cpu): print("Out of bounds")
        return False
    
    # - No piece chosen
    if piece == "_":
        if not(cpu): print("No piece chosen")
        return False

    # - Player is trying to move
    #   the opponent's piece
    if moving_opponent_piece(board, move, player):
        if not(cpu): print("You cannot move an opponent's piece!")
        return False
    
    # - Piece movement doesn't match
    #   piece movement pattern (e.g.
    #   a rook moving diagonally is
    #   invalid)
    if not(valid_movement_pattern(b, piece, m)):
        if not(cpu): print("Invalid movement pattern")
        return False
    
    # - The destination contains a
    #   piece from the same team
    if overlap_with_team(b, m):
        if not(cpu): print("One of your pieces is already in that position")
        return False

    # - The pattern is obstructed by
    #   another piece (exceptions:
    #   knight, king + castle swap
    #   (castling))
    if path_obstructed(b, m):
        if not(cpu): print("Path obstructed")
        return False

    return True

def path_obstructed(board, move):
    # - This returns True if there is a piece
    #   in the path of the piece's movement;
    #   this excludes the destination and
    #   the movement of knights
    # - This assumes that the movement pattern
    #   of the piece is valid (which should be
    #   checked prior to this call in
    #   move_is_valid())
    b = board
    m = move
    piece = b[m[0]][m[1]]
    destination = b[m[2]][m[3]]
    forward_movement = get_forward_movement(piece, move)
    right_movement = get_right_movement(piece, move)
    
    if piece[0] == "P":
        if right_movement == 0:
            if destination != "_": return True
        if abs(forward_movement) == 2:
            if piece[1] == "w":
                if b[m[2] + 1][m[3]] != "_": return True
            elif piece[1] == "b":
                if b[m[2] - 1][m[3]] != "_": return True
                
    if piece[0] == "R":
        if forward_movement != 0:
            if piece[1] == "w":
                for i in range(1, abs(forward_movement) + 1):
                    if b[8 - i][m[3]] != "_": return True
            elif piece[1] == "b":
                for i in range(m[0] + 1, m[0] + abs(forward_movement)):
                    if b[i][m[3]] != "_": return True
        elif right_movement != 0:
            if right_movement > 0:
                for i in range(m[1] + 1, m[1] + right_movement):
                    if b[m[2]][i] != "_": return True
            if right_movement < 0:
                for i in range(abs(right_movement)):
                    if b[m[2]][7 - i] != "_": return True
                    
    if piece[0] == "B":
        # Use m[0 or 1] + 1 as the starting check position
        # so that it doesn't check itself and see an
        # obstruction

        # Moving right: right_check > 0
        # Moving left: right_check < 0
        
        # Moving up and right
        if piece[1] == "w": forward_check = forward_movement > 0
        if piece[1] == "b": forward_check = forward_movement < 0
        right_check = right_movement > 0
        if forward_check and right_check:
            for i in range(1, abs(forward_movement)):
                #print("Moving up and right")
                if b[m[0] - i][m[1] + i] != "_": return True
                    
        # Moving up and left
        if piece[1] == "w": forward_check = forward_movement > 0
        if piece[1] == "b": forward_check = forward_movement < 0
        right_check = right_movement < 0
        if forward_check and right_check:
            for i in range(1, abs(forward_movement)):
                #print("Moving up and left")
                if b[m[0] - i][m[1] - i] != "_": return True

        # Moving down and right
        if piece[1] == "w": downward_check = forward_movement < 0
        if piece[1] == "b": downward_check = forward_movement > 0
        right_check = right_movement > 0
        if downward_check and right_check:
            for i in range(1, abs(forward_movement)):
                #print("Moving down and right")
                if b[m[0] + i][m[1] + i] != "_": return True
        
        # Moving down and left
        if piece[1] == "w": downward_check = forward_movement < 0
        if piece[1] == "b": downward_check = forward_movement > 0
        right_check = right_movement < 0
        if downward_check and right_check:
            for i in range(1, abs(forward_movement)):
                #print("Moving down and left")
                if b[m[0] + i][m[1] - i] != "_": return True

    if piece[0] == "Q":
        # Behaves as a rook if the movement is in one dimension,
        # and as a rook otherwise  
        if forward_movement * right_movement == 0:
            # Rook
            if forward_movement != 0:
                if piece[1] == "w":
                    for i in range(1, abs(forward_movement) + 1):
                        if b[8 - i][m[3]] != "_": return True
                elif piece[1] == "b":
                    for i in range(m[0] + 1, m[0] + abs(forward_movement)):
                        if b[i][m[3]] != "_": return True
            elif right_movement != 0:
                if right_movement > 0:
                    for i in range(m[1] + 1, m[1] + right_movement):
                        if b[m[2]][i] != "_": return True
                if right_movement < 0:
                    for i in range(abs(right_movement)):
                        if b[m[2]][7 - i] != "_": return True
        else:
            # Bishop
            # Moving up and right
            if piece[1] == "w": forward_check = forward_movement > 0
            if piece[1] == "b": forward_check = forward_movement < 0
            right_check = right_movement > 0
            if forward_check and right_check:
                for i in range(1, abs(forward_movement)):
                    #print("Moving up and right")
                    if b[m[0] - i][m[1] + i] != "_": return True
                        
            # Moving up and left
            if piece[1] == "w": forward_check = forward_movement > 0
            if piece[1] == "b": forward_check = forward_movement < 0
            right_check = right_movement < 0
            if forward_check and right_check:
                for i in range(1, abs(forward_movement)):
                    #print("Moving up and left")
                    if b[m[0] - i][m[1] - i] != "_": return True

            # Moving down and right
            if piece[1] == "w": downward_check = forward_movement < 0
            if piece[1] == "b": downward_check = forward_movement > 0
            right_check = right_movement > 0
            if downward_check and right_check:
                for i in range(1, abs(forward_movement)):
                    #print("Moving down and right")
                    if b[m[0] + i][m[1] + i] != "_": return True
            
            # Moving down and left
            if piece[1] == "w": downward_check = forward_movement < 0
            if piece[1] == "b": downward_check = forward_movement > 0
            right_check = right_movement < 0
            if downward_check and right_check:
                for i in range(1, abs(forward_movement)):
                    #print("Moving down and left")
                    if b[m[0] + i][m[1] - i] != "_": return True
                    
    return False

def overlap_with_team(board, move):
    b = board
    m = move
    piece = b[m[0]][m[1]]
    destination = b[m[2]][m[3]]
    if destination == "_": return False
    if piece[1] == destination[1]: return True
    else: return False

def overlap_with_enemy(board, move):
    b = board
    m = move
    piece = b[m[0]][m[1]]
    destination = b[m[2]][m[3]]
    if destination == "_": return False
    if piece[1] != destination[1]: return True
    else: return False

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

def check_game_state(board):
    # Check if either king is not in play,
    # in which case the player with a king
    # in play wins
    white_wins = False
    black_wins = False
    for i in range(len(board)):
        for piece in board[i]:
            if piece == "+w": white_wins = True
            if piece == "+b": black_wins = True

    if white_wins and not(black_wins): return "Player 1 wins!"
    elif black_wins and not(white_wins): return "Player 2 wins!"
    else: return ""

def display_menu():
    print("Welcome to chess!")
    print("1. Player 1 vs Player 2 (CPU)")
    print("2. Player 1 vs Player 2 (Human)")
    print("3. Exit")
    choice = input("Enter your choice: ")
    return choice

def play_vs_cpu(board):
    turn = 1
    while(1):
        if turn % 2 == 1: player = 1
        elif turn % 2 == 0: player = 2
        else: break
        if player == 1:
            clear_screen()      
            display_board(board)
            game_over = check_game_state(board)
        if game_over != "":
            print(game_over)
            break
        print("Player " + str(player) + "'s turn")
        print("Turn", turn)
        if player == 1:
            move = get_move(board, player)
        else: move = get_cpu_move(board, player)
        if move[0] == -1: break
        board = move_piece(board, move)
        turn += 1

def play_vs_player_2(board):
    turn = 1
    while(1):
        if turn % 2 == 1: player = 1
        elif turn % 2 == 0: player = 2
        else: break
        clear_screen()      
        display_board(board)
        game_over = check_game_state(board)
        if game_over != "":
            print(game_over)
            break
        print("Player " + str(player) + "'s turn")
        print("Turn", turn)
        move = get_move(board, player)
        if move[0] == -1: break
        board = move_piece(board, move)
        turn += 1

def play_debug(board):
    while(1):
        player = 1
        clear_screen()      
        display_board(board)
        game_over = check_game_state(board)
        if game_over != "":
            print(game_over)
            break
        move = get_move(board, player)
        if move[0] == -1: break
        board = move_piece(board, move)

def main():
    # TODO:
    # - Tidy up positional comparisons
    #   with helper functions,
    #   e.g. is_diagonal_to() instead of
    #   comparing coordinates

    board = initialise_board()
    choice = display_menu()
    if choice == "1": play_vs_cpu(board)
    elif choice == "2": play_vs_player_2(board)
    elif choice == "Q": play_debug(board)
    print("Exiting...")
        
main()

"""
ISSUES:
 - Queen path obstructed when moving up
   even though nothing is in its way;
   there is a pawn to its right and
   a pawn below it
"""
