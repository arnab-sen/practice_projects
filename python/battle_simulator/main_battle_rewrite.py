"""
    
"""

import sys, pygame, time, random
import battle, get_pokemon_info
from PIL import Image

def load_resources():
    res["font"] = pygame.font.Font("Resources\\Pokemon Fonts\\pkmnrs.ttf", 30)
    res["black"] = (0, 0, 0)
    res["red"] = (255, 0, 0)
    res["green"] = (0, 255, 0)
    res["yellow"] = (255, 255, 0)
    res["blue"] = (0, 0, 255)
    res["text_colour"] = res["black"]
    res["anti_alias"] = True
    res["size"] = 720, 480
    res["screen"] = pygame.display.set_mode(res["size"])
    number_of_pokemon = 2
    pokemon_numbers = get_random_pokemon(number_of_pokemon)
    pokemon_names = get_pokemon_names(pokemon_numbers)
    pokemon_1 = pokemon_numbers[0]
    pokemon_2 = pokemon_numbers[1]
    res["my moves"] = get_moves(pokemon_names[0])
    res["opp moves"] = get_moves(pokemon_names[1])
    all_moves = get_pokemon_info.get_dict("all_moves.txt")
    res["pokemon"] = create_pokemon(pokemon_numbers, [res["my moves"], res["opp moves"]])
    
    # Original size: 96 x 96, scaled size = 288, 288
    f2 = pygame.image.load("Resources\\bw-001n\\" + pokemon_2 + ".png")
    pokemon_position = get_opponent_position(pokemon_2)
    f2 = pygame.transform.scale(f2, (192, 192))
    f1 = pygame.image.load("Resources\\bwback-001n\\" + pokemon_1 + ".png")
    f1 = pygame.transform.scale(f1, (288, 288))
    res["opp pokemon sprite"] = f2
    res["my pokemon sprite"] = f1
    res["bg"] = pygame.image.load("Resources\\battle_screen_with_moves_blank.png")
    res["type icons"] = load_pokemon_type_icons()
    res["moves bar"] = pygame.image.load("Resources\\moves_bar.png")
    res["move selection"] = pygame.image.load("Resources\\move_selection.png")
    res["text bar"] = pygame.image.load("Resources\\text_bar.png")
    res["my hp bar"] = pygame.image.load("Resources\\hp_bar_01.png")
    res["opp hp bar"] = pygame.image.load("Resources\\hp_bar_02.png")
    res["my green hp"] = pygame.image.load("Resources\\hp_bars\\green.png")
    res["opp green hp"] = pygame.image.load("Resources\\hp_bars\\green.png")
    res["my yellow hp"] = pygame.image.load("Resources\\hp_bars\\yellow.png")
    res["opp yellow hp"] = pygame.image.load("Resources\\hp_bars\\yellow.png")
    res["my red hp"] = pygame.image.load("Resources\\hp_bars\\red.png")
    res["opp red hp"] = pygame.image.load("Resources\\hp_bars\\red.png")
    res["my empty hp"] = pygame.image.load("Resources\\hp_bars\\empty.png")
    res["opp empty hp"] = pygame.image.load("Resources\\hp_bars\\empty.png")
    res["hp bars pos"] = [(380, 225), (30, 43)]
    res["hp colour pos"] = [(res["hp bars pos"][1][0] + 95, res["hp bars pos"][1][0] + 61)]
    res["hp colour pos"] += [(res["hp bars pos"][1][0] + 459, res["hp bars pos"][1][0] + 242)]
    res["hp max colour width"] = 144
    res["hp widths"] = [144, 144]
    res["hp percent"] = [p0.stats["HP"] / p0.original_stats["HP"]]
    res["hp percent"] += [p1.stats["HP"] / p1.original_stats["HP"]]
    res["my hp bar"] = {"colour" : "green", "width" : 144 * res["hp percent"][0]}
    res["opp hp bar"] = {"colour" : "green", "width" : 144 * res["hp percent"][1]}
    res["hp bars"] = [{
                        "green" : res["my green hp"], "yellow" : res["my yellow hp"],
                        "red" : res["my red hp"], "empty" : res["my empty hp"]
                        }]
    res["hp bars"] += [{
                        "green" : res["opp green hp"], "yellow" : res["opp yellow hp"],
                        "red" : res["opp red hp"], "empty" : res["opp empty hp"]
                        }]
    
    res["prev hp"] = [p1.original_stats["HP"], p0.original_stats["HP"]]

    res["move surfaces"] = []
    for move in res["my moves"]:
        res["move surfaces"] += [get_move_surface(move, anti_alias, res["text colour"])]

    res["quadrants"] = initialise_display()
    res["move selection pos"] = []
    for quadrant in res["quadrants"]:
        res["move selection pos"] += [(quadrant[0] + 3, quadrant[1] + 3)]

def get_random_pokemon(number_of_pokemon):
    # Returns a list of n random pokemon from
    # 001 - 649 (Bulbasaur to Genesect)    
    pokemon_numbers = []
    for i in range(number_of_pokemon):
        num = random.randrange(1, 650)
        num = get_pokemon_info.pokemon_number(num)
        pokemon_numbers += [num]

    return pokemon_numbers

def get_pokemon_names(pokemon_numbers):
    numbered_pokemon = get_pokemon_info.get_dict("numbered_pokemon.txt")
    names = []
    for num in pokemon_numbers:
        names += [numbered_pokemon[num]]

    return names

def get_moves(pokemon_name):
    moves = get_pokemon_info.get_random_moves(pokemon_name)
    return moves

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

def get_opponent_position(opponent_number):
    # Find the bottom-most pixel in the middle column, and align
    # that with the center of the opponent stage
    image = Image.open("Resources\\bw-001n\\" + opponent_number + ".png")
    image = image.resize((192, 192), Image.ANTIALIAS)
    image = image.convert("RGBA")
    pixel_data = list(image.getdata())
    pixel_data = split_list(192, pixel_data)
    middle = 96
    stage_middle = (520, 195)
    
    for i in range(96, len(pixel_data)):
            if pixel_data[i][middle][3] != 0:
                    bottom = i
                    
    return (stage_middle[0] - middle, stage_middle[1] - bottom)

def load_pokemon_type_icons():
    type_icons = {}
    move_types = ["bug", "dark", "dragon", "electric", "fighting", "fire",
                  "flying", "ghost", "grass", "ground", "ice", "normal",
                  "other", "physical", "poison", "psychic", "rock",
                  "special", "steel", "water"]
    
    for i in move_types:
        icon = pygame.image.load("Resources\\Move Icons\\" + i + ".png")
        if i != "physical" and i != "special" and i != "other":
            icon = pygame.transform.scale(icon, (64, 32))
        else:
            icon = pygame.transform.scale(icon, (56, 28))
        type_icons[i] = icon
    return type_icons

def get_move_surface(move, anti_alias, text_colour):
    return res["font"].render(move, True, text_colour)

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

def mouse_in_quadrant(mouse_position, move_quadrants):
    for i in range(4):
        if move_quadrants[i].collidepoint(mouse_position):
            return i
    return -1

def state_machine():
    """
    Game states:
    State progression via mouse click (or specifically, mouse up)
    show moves -> highlight move -> attack1 if able -> attack2 if able -> game over if able
    States to be worked on include healing pokemon/using item, show current party,
    switching pokemon out, running from battle
    Can call game state functions via the res dict, e.g.:
    res["game over"] = game_over
    res["game over"]()
    """
    current = res["game state"]
    if current == "start":
        next_state = "show moves"
    elif current == "show moves" and res["current quadrant"] != -1:
        next_state = "first attack"
    elif current == "first attack":
        next_state = "second attack"
    elif current == "second attack":
        if res["fainted"]:
            next_state = "game over"
        else:
            next_state = "show moves"

    res["next state"] = next_state

def show_moves():
    pass

def attack():
    pass

def game_over():
    pass

def main(resources):
    # Initialise
    res = resources # Dict of all resource variables
    pygame.init()
    pygame.font.init()
    load_resources()
    p0 = res["pokemon"][0]
    p1 = res["pokemon"][1]
    res["game state"] = "start"
    #res["game state"] = "show_moves"
    res["game over"] = False
    res["my turn"] = True
    res["exit game"] = False
    res["move selected"] = -1 # [-1, 0, 1] = [not selected, selected, confirmed]
    res["selected index"] = -2 # random value that isn't a possible index and not -1

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_position = pygame.mouse.get_pos()
                res["current quadrant"] = mouse_in_quadrant(mouse_position, res["quadrants"])
  
if __name__ == "__main__":
    res = {} # Resources dict kept as a global variable for easy access
    main(res)
