import sys, pygame, time, random
import battle, get_pokemon_info

def initialise_display():
    moves_top_left = (18, 356)
    moves_center = (240, 410)
    quadrant_width = moves_center[0] - 18
    quadrant_height = moves_center[1] - 356
    quadrant_1 = pygame.Rect(18, 356, quadrant_width, quadrant_height)
    quadrant_2 = pygame.Rect(241, 356, quadrant_width, quadrant_height)
    quadrant_3 = pygame.Rect(18, 410, quadrant_width, quadrant_height)
    quadrant_4 = pygame.Rect(241, 410, quadrant_width, quadrant_height) 
    
    return [quadrant_1, quadrant_2, quadrant_3, quadrant_4]

def get_pokemon_names(pokemon_numbers):
    numbered_pokemon = get_pokemon_info.get_dict("numbered_pokemon.txt")
    names = []
    for num in pokemon_numbers:
        names += [numbered_pokemon[num]]

    return names

def get_moves(pokemon_name):
    moves = get_pokemon_info.get_random_moves(pokemon_name)
    return moves

def get_move_surface(move, anti_alias, text_colour):
    return myfont.render(move, True, text_colour)

def get_random_pokemon(number_of_pokemon):
    # Returns a list of n random pokemon from
    # 001 - 649 (Bulbasaur to Genesect)    
    pokemon_numbers = []
    for i in range(number_of_pokemon):
        num = random.randrange(1, 650)
        num = get_pokemon_info.pokemon_number(num)
        pokemon_numbers += [num]

    return pokemon_numbers 

def create_pokemon(pokemon_numbers, moves):
    pokemon = []
    numbered_pokemon = get_pokemon_info.get_dict("numbered_pokemon.txt")
    # TODO:
    # - Get the following placeholder stats from a dict instead
    i = 0
    all_stats = get_pokemon_info.get_dict("pokemon_stats.txt")
    
    for num in pokemon_numbers:
        name = numbered_pokemon[get_pokemon_info.pokemon_number(num)]
        pokemon += [battle.Pokemon(name, moves[i], all_stats[name])]
        i += 1

    return pokemon

def mouse_in_quadrant(mouse_position, move_quadrants):
    for i in range(4):
        if move_quadrants[i].collidepoint(mouse_position):
            return i
    return -1

def show_attack(attacker, defender, current_move):
    a = attacker
    d = defender
    battle_over = False
    temp_HP = defender.stats["HP"]
    battle_text_message = []
    battle_text = []
    battle.attack(attacker, defender, current_move)
    battle_text_message += [attacker.name + " used " + current_move + "!"]
    battle_text_message += [defender.name + "'s HP fell from " + str(temp_HP)]
    battle_text_message += ["to " + str(defender.stats["HP"])]
        
    #print(attacker.name + " used " + current_move + "!")
    #print(defender.name + "'s HP fell from " + \
    #      str(temp_HP) + \
    #      " to " + str(defender.stats["HP"]))
    #print()
    if defender.stats["HP"] == 0:
        battle_text_message += [defender.name + " fainted... " + attacker.name + " wins!"]
        battle_over = True

    for i in range(len(battle_text_message)):
        battle_text += [myfont.render(battle_text_message[i] , True , (0, 0, 0))]

    return battle_over, battle_text

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    #myfont = pygame.font.SysFont('Verdana', 25)
    myfont = pygame.font.Font("Resources\\Pokemon Fonts\\pkmnrs.ttf", 30)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    yellow = (255, 255, 0)
    blue = (0, 0, 255)
    text_colour = black
    anti_alias = True

    size = width, height = 720, 480

    screen = pygame.display.set_mode(size)

    number_of_pokemon = 2
    pokemon_numbers = get_random_pokemon(number_of_pokemon)
    pokemon_numbers[0] = "006"
    pokemon_names = get_pokemon_names(pokemon_numbers)
    pokemon_1 = pokemon_numbers[0]
    pokemon_2 = pokemon_numbers[1]
    pokemon_position = (420, 50)
    moves = get_moves(pokemon_names[0])
    opponent_moves = get_moves(pokemon_names[1])
    pokemon = create_pokemon(pokemon_numbers, [moves, opponent_moves])
    if pokemon_1 == "632": pokemon_position = (380, 20)
    # Test pokemon
    # Original size: 96 x 96, scaled size = 288, 288
    f2 = pygame.image.load("Resources\\bw-001n\\" + pokemon_2 + ".png")
    #f2 = pygame.transform.scale(f2, (288, 288))
    f2 = pygame.transform.scale(f2, (192, 192))
    f1 = pygame.image.load("Resources\\bwback-001n\\" + pokemon_1 + ".png")
    f1 = pygame.transform.scale(f1, (288, 288))
    bg = pygame.image.load("Resources\\battle_screen_with_moves_blank.png")
    moves_bar = pygame.image.load("Resources\\moves_bar.png")
    text_bar = pygame.image.load("Resources\\text_bar.png")

    # Positions are in (width, height) or (x, y) rather than (row, col)
    move_surfaces = []
    # Get user's pokemon's moveset
    #print(pokemon_names)
    
    for move in moves:
        move_surfaces += [get_move_surface(move, anti_alias, text_colour)]
        
    quadrants = initialise_display()

    # DEBUG printing:
    print(pokemon[0].stats)
    print(pokemon[1].stats)
    p0 = pokemon[0]
    p1 = pokemon[1]
    game_state = "show_moves"
    game_over = False
    my_turn = True
    exit_game = False
    
    while 1:
        #time.sleep(0.01) # To slow down the animation
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Close the window
                pygame.display.quit()
                # Exit the program
                sys.exit()
            # If the mouse button is (pressed and) released
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_position = pygame.mouse.get_pos()
                i = mouse_in_quadrant(mouse_position, quadrants)
                if game_state == "show_moves":
                    if i > -1 and pokemon[0].stats["HP"] * \
                                  pokemon[1].stats["HP"] != 0:
                        current_move = moves[i]
                        opponent_move = opponent_moves[random.randrange(3)]
                        if game_over:
                            game_state = "game_over"
                        else:
                            game_state = "battle_text_1"
                        if not game_over:
                            game_over, battle_text_1 = show_attack(p0, p1, current_move)
                            last_move = battle_text_1
                        if not game_over:
                            game_over, battle_text_2 = show_attack(p1, p0, opponent_move)
                            last_move = battle_text_2
                        battle_text = last_move
                elif game_state == "battle_text_1":
                    if i > -1:
                        if game_over:
                            game_state = "game_over"
                            if p0.stats["HP"] == 0:
                                winner = p0.name
                            elif p1.stats["HP"] == 0:
                                winner = p1.name
                        else:
                            game_state = "battle_text_2"
                elif game_state == "battle_text_2":
                    if i > -1:
                        if game_over:
                            game_state = "game_over"
                            if p0.stats["HP"] == 0:
                                winner = p0.name
                            elif p1.stats["HP"] == 0:
                                winner = p1.name
                        else:
                            game_state = "show_moves"
                elif game_state == "game_over":
                    print("Battle over!")
                    game_state = "exit_game"
            if game_state == "exit_game":
                pygame.display.quit()
                # Exit the program
                sys.exit()
                    
        screen.fill(black)
        screen.blit(bg, (0, 0))
        screen.blit(f1, (60, 150))
        screen.blit(f2, pokemon_position)
        if game_state == "show_moves":
            screen.blit(moves_bar, (0, 337))
            screen.blit(move_surfaces[0],(quadrants[0][0] + 30, quadrants[0][1] + 15))
            screen.blit(move_surfaces[1],(quadrants[1][0] + 10, quadrants[1][1] + 15))
            screen.blit(move_surfaces[2],(quadrants[2][0] + 30, quadrants[2][1] + 10))
            screen.blit(move_surfaces[3],(quadrants[3][0] + 10, quadrants[3][1] + 10))
            right_box_message = "HP: " + str(pokemon[0].stats["HP"]) + "/" + \
                                str(pokemon[0].original_stats["HP"])        
            right_box = myfont.render(right_box_message , anti_alias, text_colour)
            screen.blit(right_box,(525, 395))
        elif game_state == "battle_text_1":
            screen.blit(text_bar, (0, 337))
            screen.blit(battle_text_1[0], (25, 360))
            screen.blit(battle_text_1[1], (25, 398))
            screen.blit(battle_text_1[2], (25, 435))
        elif game_state == "battle_text_2":
            screen.blit(text_bar, (0, 337))
            screen.blit(battle_text_2[0], (25, 360))
            screen.blit(battle_text_2[1], (25, 398))
            screen.blit(battle_text_2[2], (25, 435))
        elif game_state == "game_over":
            screen.blit(text_bar, (0, 337))
            screen.blit(battle_text[3], (25, 398))
            exit_game = True
            #break
        
        # update whole screen (use display.update(rectangle) to update
        # chosen rectangle portions of the screen to update
        pygame.display.flip()
