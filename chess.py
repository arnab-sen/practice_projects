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

def get_move():
    print("Move example: a2 to a4")
    letters = "abcdefgh"
    move = input("Enter move: ")
    move = move.split()
    position = ["row 1", "col 1", "row 2", "col 2"]
    # Rows are numbers (9 - i), cols are letters (a - h)
    position[0] = 9 - int(move[0][1])
    position[1] = letters.find(move[0][0])
    position[2] = 9 - int(move[2][1])
    position[3] = letters.find(move[2][0])
    print(position)
    return position

def move_piece(board, move):
    board[5][0] = board[move[0]][move[1]]
    board[move[0]][move[1]] = "_"
    return board

def print_board_matrix(board):
    for i in range(9):
        print(board[i])

def remove_overlap(board, position):
    # move current piece to "graveyard"
    # replace current piece with new piece
    # (so long as the move was valid)
    pass

def is_move_valid(board, position, piece):
    # return True if the move is valid
    # return False if the move is invalid
    pass

def main():
    board = initialise_board()
    display_board(board)
    move = get_move()
    board = move_piece(board, move)
    display_board(board)

main()
 