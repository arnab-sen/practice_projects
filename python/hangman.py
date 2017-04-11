def display_banner():
    title = "## Hangman 9/04/2017 ##"
    print("#" * len(title))
    print(title)
    print("#" * len(title))
    print()

def hangman_state(state):
    state0 = ["---------\n", "|\n", "|\n", "|\n", "|\n", "|\n", "TTTTTTTTTT\n"]
    state1 = [state0[0]] + ["|    |\n"] + state0[2:]
    state2 = state1[:2] + ["|    O\n"] + state0[3:]
    state3 = state2[:3] + ["|   /\n"] + state2[4:]
    state4 = state2[:3] + ["|   /|\n"] + state2[4:]
    state5 = state2[:3] + ["|   /|\\\n"] + state2[4:]
    state6 = state5[0:4] + ["|  _/ \n"] + state5[5:]
    state7 = state5[0:4] + ["|  _/ \_\n"] + state5[5:]
    
    if state == 0: return state0
    elif state == 1: return state1
    elif state == 2: return state2
    elif state == 3: return state3
    elif state == 4: return state4
    elif state == 5: return state5
    elif state == 6: return state6
    elif state == 7: return state7

def update_hangman(current_state):
    if current_state == 7: current_state -= 1
    hangman = hangman_state(current_state + 1)
    for row in hangman: print(row, end = "") 

def get_command():
    letter = input("\nEnter a letter (0 to exit): ")
    while letter == "":
        letter = input()
    return letter[0].lower()

def clear_screen():
    print("\n" * 100)

def get_word():
    import random
    #return input("\nEnter your word: ").lower() # hardcode a word for debugging
    with open("word_list.txt") as file:
        words = file.read().split("\n")
    return words[random.randrange(len(words))]

def hide_word(word):
    return "-" * len(word)

def update_word(answer, word, letter):
    new_word = [i for i in word]
    answer = [i for i in answer]
    if not(letter in answer): return word
    for i in range(len(word)):
        if new_word[i] == "-":
            if letter == answer[i]: new_word[i] = letter
        
    return ''.join(new_word)

def alphabet():
    return "abcdefghijklmnopqrstuvwxyz"

def remove_letter(word, letter):
    while letter in word:
        index = word.find(letter)
        word = word[:index] + "-" + word[index + 1:]
    return word

def letters_left(used_words):
    current_alphabet = alphabet()
    for i in used_words:
        current_alphabet = remove_letter(current_alphabet, i)
    return current_alphabet

def number_of_letters_left(letters_left):
    count = 0
    for i in letters_left:
        if i != "-": count += 1
    return count

def update_display(current_state, chances, current_word, used_words, guesses, word, game_state):
    clear_screen()
    display_banner()
    update_hangman(current_state)
    print("\nChances left:", chances)
    print("\nWord:", current_word, "\n")
    print("Available letters: " + letters_left(used_words) + " (" \
          + str(number_of_letters_left(letters_left(used_words))) + " letters)")
    print("\nUsed letters: ", end = "")
    for i in used_words: print(i, "", end = "")
    if game_state == "won":
        print("\nCongratulations! You win.")
        print("Guessed the correct word in " + str(guesses) + " tries.")
    elif game_state == "lost":
        print("\nGame over. Word was: " + str(word))

def main():
    play_again = "y"
    while(play_again == "y"):
        play_again = ""
        display_banner()
        word = get_word()
        current_word = "-" * len(word)
        letter = "5"
        max_chances = 7
        chances = max_chances
        guesses = 0
        used_words = []
        current_state = -1    
        while(1):
            current_word = update_word(word, current_word, letter)
            update_display(current_state, chances, current_word, used_words, guesses, word, "playing")
            if current_word == word:
                update_display(current_state, chances, current_word, used_words, guesses, word, "won")
                break
            letter = get_command()
            if not(letter in word) and not(letter in used_words):
                chances -= 1
                current_state += 1
                used_words += [letter]
            if not(letter in current_word) and not(letter in used_words):
                used_words += [letter]
            guesses = len(used_words)
            if letter == "0": break
            if chances < 1:
                update_display(current_state, chances, current_word, used_words, guesses, word, "lost")
                break
        play_again = input("Play again? (y/n): ").lower()      
    print("Thank you for playing (press Enter to exit).")
    input()    

main()
