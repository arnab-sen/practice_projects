def display_intro():
    title = "# Tic-Tac-Toe 10/04/2017 #"
    print("#" * len(title))
    print(title)
    print("#" * len(title))
    print()

def display_menu():
    print("1. Player 1 vs AI")
    print("2. Player 1 vs Player 2\n")
    choice = int(input("Enter your choice: "))
    return choice    
    
def initialise_board():
    board = [[],[],[]]
    board[0] = ["___", "|___", "|___"]
    board[1] = ["___", "|___", "|___"]
    board[2] = ["   ", "|   ", "|   "]
    return board

def clear_screen():
    print("\n" * 100)

def change_board(board, row, col, X_or_O):
    # X_or_O == "" for empty, "X" for X, "O" for O
    if X_or_O != "":
        if (row == 0 or row == 1) and (col == 1 or col == 2):
            board[row][col] = "|_" + X_or_O + "_"
        elif row == 2 and (col == 1 or col == 2):
            board[row][col] = "| " + X_or_O + " "
        elif (row == 0 or row == 1) and col == 0:
            board[row][col] = "_" + X_or_O + "_"
        elif row == 2 and col == 0:
            board[row][col] = " " + X_or_O + " "

    return board
        
def get_coordinates(board, icon, player):
    if player == 1: print("Player 1:")
    elif player == 2: print("Player 2:")
    prompt = "Where do you want to place " + icon + "?(-1 to quit): "
    coordinates = input(prompt).split()
    coordinates = [int(i) for i in coordinates]
    if coordinates[0] == -1: return coordinates
    while out_of_range(coordinates):
        coordinates = input(prompt).split()
        coordinates = [int(i) for i in coordinates]
    if coordinates[0] == -1: return coordinates    
    while not(check_if_empty(board, coordinates, False)):
        coordinates = input(prompt).split()
        coordinates = [int(i) for i in coordinates]
    return coordinates

def out_of_range(coordinates):
    if coordinates[0] == -1: return False
    if coordinates[0] > 2 or coordinates[0] < -1:
        print("Position out of range. Please enter \"0-2 0-2\"\n")
        return True
    if coordinates[1] > 2 or coordinates[1] < 0:
        print("Position out of range. Please enter \"0-2 0-2\"\n")
        return True
    return False

def display_board(board):
    print("         Column")
    print("        0   1   2")
    print("    0  ", end = "")
    for i in board[0]: print(i, end = "")
    print()
    print("Row 1  ", end = "")
    for i in board[1]: print(i, end = "")
    print()
    print("    2  ", end = "")
    for i in board[2]: print(i, end = "")
    print("\n")

def board_to_matrix(board):
    # 0 == empty; 1 == P1; 2 == P2 or CPU
    matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in range(3):
        if board[0][i].find("X") != -1: matrix[0][i]= 1
        if board[1][i].find("X") != -1: matrix[1][i]= 1
        if board[2][i].find("X") != -1: matrix[2][i]= 1
        if board[0][i].find("O") != -1: matrix[0][i]= 2
        if board[1][i].find("O") != -1: matrix[1][i]= 2
        if board[2][i].find("O") != -1: matrix[2][i]= 2
    return matrix

def check_game_state(matrix):
    state = "playing"
    # Check row completion
    for i in range(3):
        if matrix[i] == [1, 1, 1]:
            return "p1"
        if matrix[i] == [2, 2, 2]:
            return "p2" 

    # Check column completion
    for i in range(3):
        if matrix[0][i] == 1 and matrix[1][i] == 1 and matrix[2][i] == 1:
            return "p1"
        if matrix[0][i] == 2 and matrix[1][i] == 2 and matrix[2][i] == 2:
            return "p2"
        
    # Check diagonal completion
    p1_count = 0
    p2_count = 0
    # Forward diagonal
    for i in range(3):
        if matrix[i][i] == 1: p1_count += 1
        if p1_count == 3:
            return "p1"
        if matrix[i][i] == 2: p2_count += 1
        if p2_count == 3:
            return "p2"

    p1_count = 0
    p2_count = 0
    # Anti-diagonal
    for i in range(3):
        if matrix[2 - i][i] == 1: p1_count += 1
        if p1_count == 3:
            return "p1"
        if matrix[2 - i][i] == 2: p2_count += 1
        if p2_count == 3:
            return "p2"

    # Check if not draw
    for i in range(3):
        for j in range(3):
            if matrix[i][j] == 0:
                return "playing"

    return "draw"

def check_if_empty(board, coordinates, is_ai):
    row = coordinates[0]
    if row == -1: return True
    col = coordinates[1]
    if board[row][col].find("X") == -1 and board[row][col].find("O") == -1:
        return True
    if not(is_ai): print("Location already filled.")
    clear_screen()
    display_intro()
    display_board(board)
    return False

def game_vs_p2(p1_icon, p2_icon, board, coordinates):
    while coordinates[0] != -1:
        matrix = board_to_matrix(board)
        game_state = check_game_state(matrix)
        if game_state == "playing":
            clear_screen()
            display_intro()
            display_board(board)
            coordinates = get_coordinates(board, p1_icon, 1)
            if coordinates[0] == -1: return
            change_board(board, coordinates[0], coordinates[1], p1_icon)
        else:
            clear_screen()
            display_intro()
            display_board(board)
            if game_state == "p1": print("Player 1 wins!")
            elif game_state == "p2": print("Player 2 wins!")
            elif game_state == "draw": print("Tied game!")
            return

        matrix = board_to_matrix(board)
        game_state = check_game_state(matrix)
        if game_state == "playing":
            clear_screen()
            display_intro()
            display_board(board)
            coordinates = get_coordinates(board, p2_icon, 2)
            if coordinates[0] == -1: return
            change_board(board, coordinates[0], coordinates[1], p2_icon)
        else:
            clear_screen()
            display_intro()
            display_board(board)
            if game_state == "p1": print("Player 1 wins!")
            elif game_state == "p2": print("Player 2 wins!")
            elif game_state == "draw": print("Tied game!")
            return

def ai_pre_win(board):
    # Completing potential AI triplet given first priority
    # Blocking potential player 1 triplet given secondary priority
    matrix = board_to_matrix(board)
    
    # Check own status
    # Check rows
    for i in range(3):
        count = 0
        for j in range(3):
            if matrix[i][j] == 1: count -= 1
            elif matrix[i][j] == 2: count += 1
        if count == 2:
            for j in range(3):
                if matrix[i][j] == 0: return [i, j]

    # Check columns
    for i in range(3):
        count = 0
        for j in range(3):
            if matrix[j][i] == 1: count -= 1
            elif matrix[j][i] == 2: count += 1
        if count == 2:
            for j in range(3):
                if matrix[j][i] == 0: return [j, i]

    # Check diagonals
    # Forward diagonal
    for i in range(3):
        count = 0
        if matrix[i][i] == 1: count -= 1
        elif matrix[i][j] == 2: count += 1
    if count == 2:
        for i in range(3):
            if matrix[i][i] == 0: return [i, i]

    # Anti-diagonal
    for i in range(3):
        count = 0
        if matrix[2 - i][i] == 1: count -= 1
        elif matrix[2 - i][i] == 2: count += 1
    if count == 2:
        for i in range(3):
            if matrix[2 - i][i] == 0: return [2 - i, i]

    # ---------------------
    # Check player 1 status
    # Check rows
    for i in range(3):
        count = 0
        for j in range(3):
            if matrix[i][j] == 2: count -= 1
            elif matrix[i][j] == 1: count += 1
        if count == 2:
            for j in range(3):
                if matrix[i][j] == 0: return [i, j]

    # Check columns
    for i in range(3):
        count = 0
        for j in range(3):
            if matrix[j][i] == 2: count -= 1
            elif matrix[j][i] == 1: count += 1
        if count == 2:
            for j in range(3):
                if matrix[j][i] == 0: return [j, i]

    # Check diagonals
    # Forward diagonal
    count = 0
    for i in range(3):
        if matrix[i][i] == 2: count -= 1
        elif matrix[i][i] == 1: count += 1
    if count == 2:
        for i in range(3):
            if matrix[i][i] == 0: return [i, i]

    # Anti-diagonal
    count = 0
    for i in range(3):
        if matrix[2 - i][i] == 2: count -= 1
        elif matrix[2 - i][i] == 1: count += 1
    if count == 2:
        for i in range(3):
            if matrix[2 - i][i] == 0: return [2 - i, i]
    return ["", ""]
    

def get_ai_coordinates(board):
    import random
    coordinates = ai_pre_win(board)
    # Get random coordinates if no other tactics in play
    if coordinates == ["", ""]:
        coordinates = [random.randrange(3), random.randrange(3)]
        while not(check_if_empty(board, coordinates, True)):
            coordinates = [random.randrange(3), random.randrange(3)]
    return coordinates

def game_vs_ai(p1_icon, p2_icon, board, coordinates):
    import time
    while coordinates[0] != -1:
        matrix = board_to_matrix(board)
        game_state = check_game_state(matrix)
        if game_state == "playing":
            clear_screen()
            display_intro()
            display_board(board)
            coordinates = get_coordinates(board, p1_icon, 1)
            if coordinates[0] == -1: return
            change_board(board, coordinates[0], coordinates[1], p1_icon)
        else:
            clear_screen()
            display_intro()
            display_board(board)
            if game_state == "p1": print("Player 1 wins!")
            elif game_state == "p2": print("Player 2 wins!")
            elif game_state == "draw": print("Tied game!")
            return

        matrix = board_to_matrix(board)
        game_state = check_game_state(matrix)
        if game_state == "playing":
            clear_screen()
            display_intro()
            display_board(board)
            coordinates = get_ai_coordinates(board)
            print("The computer is thinking...")
            time.sleep(2)
            change_board(board, coordinates[0], coordinates[1], p2_icon)
        else:
            clear_screen()
            display_intro()
            display_board(board)
            if game_state == "p1": print("Player 1 wins!")
            elif game_state == "p2": print("The computer wins!")
            elif game_state == "draw": print("Tied game!")
            return

def main():
    p1_icon = "X"
    p2_icon = "O"
    play_again = "y"
    while play_again == "y":
        clear_screen()
        display_intro()
        choice = display_menu()
        play_again == "n"
        board = initialise_board()
        coordinates = ["", ""]
        if choice == 1: game_vs_ai(p1_icon, p2_icon, board, coordinates)
        elif choice == 2:
            game_vs_p2(p1_icon, p2_icon, board, coordinates)
        play_again = input("Play again? (y/n): ").lower()
    

main()
