import sys, pygame, time, random
# Get a random pokemon with random moves selected from that
# Pokemon's moveset (will need multiple dicts for pokemon
# and their movesets --> use webscraping from serebii
# or bulbapedia to get stats and movesets) -->
# use web scraping to get all info required just once,
# and store that info in txt files

# Make moves into buttons using mouse.get_pos() and
# having a button rectangle set around each move
# (perform an action if the mouse click is within
# that rectangle)

#move_1 = input("Enter move 1: ")
move_1 = "Scratch"
move_2 = "Water Gun"
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Verdana', 25)
text_colour = (0, 0, 0) # black
anti_alias = True

# Note that positions are in (width, height) or (x, y) rather than (row, col)
move_1_surface = myfont.render(move_1, anti_alias, text_colour)
move_2_surface = myfont.render(move_2, anti_alias, text_colour)
move_3_surface = myfont.render('Move 3', anti_alias, text_colour)
move_4_surface = myfont.render('Move 4', anti_alias, text_colour)
move_power = myfont.render('Move Power', anti_alias, text_colour)
#screen.blit(textsurface,(0,0))

size = width, height = 720, 480

screen = pygame.display.set_mode(size)
pokemon_1 = str(random.randrange(650))
if len(pokemon_1) == 1: pokemon_1 = "00" + pokemon_1
elif len(pokemon_1) == 2: pokemon_1 = "0" + pokemon_1
pokemon_2 = str(random.randrange(650))
if len(pokemon_2) == 1: pokemon_2 = "00" + pokemon_2
elif len(pokemon_2) == 2: pokemon_2 = "0" + pokemon_2
#pokemon = "632"
pokemon_position = (380, -20)
if pokemon_1 == "632": pokemon_position = (380, 20)
# Test pokemon
# Original size: 96 x 96, scaled size = 288, 288
f2 = pygame.image.load("bw-001n\\" + pokemon_2 + ".png")
f2 = pygame.transform.scale(f2, (288, 288))
f1 = pygame.image.load("bwback-001n\\" + pokemon_1 + ".png")
f1 = pygame.transform.scale(f1, (288, 288))
bg = pygame.image.load("battle_screen_with_moves_blank.png")
moves_bar = pygame.image.load("moves_bar.png")


while 1:
    #time.sleep(0.01) # To slow down the animation
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Close the window
            pygame.display.quit()
            # Exit the program
            sys.exit()

    screen.fill(black)
    screen.blit(bg, (0, 0))
    screen.blit(f1, (60, 150))
    screen.blit(f2, pokemon_position)
    screen.blit(moves_bar, (0, 337))
    screen.blit(move_1_surface,(30, 370))
    screen.blit(move_2_surface,(230, 370))
    screen.blit(move_3_surface,(30, 425))
    screen.blit(move_4_surface,(230, 425))
    screen.blit(move_power,(525, 395))
    
    # update whole screen (use display.update(rectangle) to update
    # chosen rectangle portions of the screen to update
    pygame.display.flip()


