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

def create_pokemon(pokemon_numbers):
    pokemon = []
    numbered_pokemon = get_pokemon_info.get_dict("numbered_pokemon.txt")
    # TODO:
    # - Get the following placeholder stats from a dict instead
    placeholder_hp = 150
    placeholder_atk = 50
    for num in pokemon_numbers:
        name = numbered_pokemon[get_pokemon_info.pokemon_number(num)]
        pokemon += [battle.Pokemon(name, placeholder_hp, placeholder_atk)]

    return pokemon

def mouse_in_quadrant(mouse_position, move_quadrants):
    for i in range(4):
        if move_quadrants[i].collidepoint(mouse_position):
            return i
    return -1

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
    pokemon_names = get_pokemon_names(pokemon_numbers)
    pokemon_1 = pokemon_numbers[0]
    pokemon_2 = pokemon_numbers[1]
    pokemon_position = (420, 50)
    pokemon = create_pokemon(pokemon_numbers)
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

    # Positions are in (width, height) or (x, y) rather than (row, col)
    move_surfaces = []
    # Get user's pokemon's moveset
    print(pokemon_names)
    moves = get_moves(pokemon_names[0])
    for move in moves:
        move_surfaces += [get_move_surface(move, anti_alias, text_colour)]
        
    move_power = myfont.render('Move Power', anti_alias, text_colour)
    quadrants = initialise_display()

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
                if i > -1:
                    current_move = moves[i]
                    print(pokemon_names[0] + " used " + current_move + "!")
                    battle.attack(pokemon[0], pokemon[1])

        screen.fill(black)
        screen.blit(bg, (0, 0))
        screen.blit(f1, (60, 150))
        screen.blit(f2, pokemon_position)
        screen.blit(moves_bar, (0, 337))
        # Show move quadrants
        #screen.fill(yellow, quadrant_1)
        #screen.fill(red, quadrant_2)
        #screen.fill(green, quadrant_3)
        #screen.fill(blue, quadrant_4)
        screen.blit(move_surfaces[0],(quadrants[0][0] + 30, quadrants[0][1] + 15))
        screen.blit(move_surfaces[1],(quadrants[1][0] + 10, quadrants[1][1] + 15))
        screen.blit(move_surfaces[2],(quadrants[2][0] + 30, quadrants[2][1] + 10))
        screen.blit(move_surfaces[3],(quadrants[3][0] + 10, quadrants[3][1] + 10))
        screen.blit(move_power,(525, 395))
        
        
        # update whole screen (use display.update(rectangle) to update
        # chosen rectangle portions of the screen to update
        pygame.display.flip()
