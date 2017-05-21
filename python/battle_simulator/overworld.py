"""
"""

import sys, pygame, time
from PIL import Image
import tile_viewer

res = {}
BLACK = 0, 0, 0
ANTI_ALIAS = True
SIZE = 720, 480
screen = pygame.display.set_mode(SIZE)
SCALE = 3
TILE_DIM = 16 * SCALE
TILE_MOVEMENT = TILE_DIM // 2

def location(filename):
    #return "Resources\\Overworld\\" + filename
    return "Resources/Overworld/" + filename

def scale_image(scale, image):
    width, height = image.size
    image = image.resize((width * scale, height * scale))#, Image.ANTIALIAS)
    # including Image.ANTIALIAS makes a blurry scaled image

    return image

def load_image(name):
    image = Image.open(location(name + ".png"))
    image = scale_image(3, image)
    image_data = image.tobytes(), image.size, image.mode
    
    return pygame.image.fromstring(*image_data)

def load_character(character_name):
    pass

def place_at(tile_row, tile_col):
    """
    Player/NPC sprite offset from the tile it's on:
    * Let tile top left be 0, 0
    * Offset = -1 * SCALE, -4 * SCALE
    """
    i, j = tile_row, tile_col
    tile_pos = i * TILE_DIM - res["map pos"][0], j * TILE_DIM - res["map pos"][1]
    offset = -1 * SCALE, -4 * SCALE

    res["mc pos"] = [tile_pos[0] + offset[0], tile_pos[1] + offset[1]]

def move_sprite(direction):
    if direction == "down":
        map_index = 1
        map_movement = -1
    elif direction == "up":
        map_index = 1
        map_movement = 1
    elif direction == "right":
        map_index = 0
        map_movement = -1
    elif direction == "left":
        map_index = 0
        map_movement = 1
    
    #res["moving"] = not(res["moving"])
    move_to_tile = res["mc tile"][:]
    current_tile = res["mc tile"][:]
    
    move_to_tile[map_index] -= map_movement
    y, x = current_tile
    j, i = move_to_tile
    
    """
    print("\nCurrent tile: {}\nMove to: {}".format((x, y), (i, j)))   
    print("Current tile state:", res["tile states"][x][y])
    print("Move to tile state:", res["tile states"][i][j])
    """
    
    if res["tile states"][move_to_tile[1]][move_to_tile[0]] == 0:
        #print("Currently at tile {}".format(res["mc tile"]))
        res["mc tile"][map_index] -= map_movement
        res["mc frame"] = (res["mc frame"] + 1) % len(res["mc current"])
        res["map pos"][map_index] += map_movement * TILE_MOVEMENT  
        if res["animate"]:
            update_screen()
            advance_frame()
        pygame.time.Clock().tick(10)
        res["map pos"][map_index] += map_movement * TILE_MOVEMENT 
        res["mc frame"] = (res["mc frame"] + 1) % len(res["mc current"])

    #print(res["map pos"])

def load_resources():
    #res["pallet town"] = pygame.image.load(location("pallet town.png"))
    res["current map name"] = "pallet town"
    image = Image.open(location("pallet town.png"))
    image = scale_image(3, image)
    image_data = image.tobytes(), image.size, image.mode
    res["pallet town"] = load_image("pallet town")
    res["map"] = res["pallet town"]
    res["map pos"] = [0, 0]
    mc = {}
    mc["down"], mc["up"], mc["left"], mc["right"] = [], [], [], []
    res["mc"] = mc
    for i in range(4):
        res["mc"]["down"].append(load_image("mc down " + str(i)))
        res["mc"]["up"].append(load_image("mc up " + str(i)))
        res["mc"]["left"].append(load_image("mc left " + str(i)))
        res["mc"]["right"].append(load_image("mc right " + str(i)))
    #res["mc pos"] = [SIZE[0] / 2 - 21, SIZE[1] / 2 - 28]
    #place_at(7, 5)
    res["mc tile"] = [SIZE[0] // 2 // TILE_DIM, SIZE[1] // 2 // TILE_DIM]
    place_at(*res["mc tile"])
    #place_at(3, 3)
    res["mc current"] = res["mc"]["down"]
    res["mc frame"] = 0
    tile_viewer.initialise(res["current map name"])
    rows, cols = tile_viewer.get_base(res["current map name"])
    res["tile states"] = tile_viewer.get_tile_states(rows, cols)
    
def update_screen():
    screen.fill(BLACK)
    screen.blit(res["map"], res["map pos"])
    screen.blit(res["mc current"][res["mc frame"]], res["mc pos"])

def advance_frame():
    pygame.display.flip()

def reposition(movement_sequence):
    directions = {
                    "l" : "left",
                    "r" : "right",
                    "u" : "up",
                    "d" : "down"
                    }
    
    for direction in movement_sequence:
            move_sprite(directions[direction])
            
    res["animate"] = True

def play():
    load_resources()
    #res["moving"] = False
    res["animate"] = False
    reposition("lddd")

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
                
        

        button_press = (event.type == pygame.KEYDOWN)
        if button_press and event.key == pygame.K_DOWN:
            direction = "down"
            res["mc current"] = res["mc"][direction]
            move_sprite(direction)
        elif button_press and event.key == pygame.K_LEFT:
            direction = "left"
            res["mc current"] = res["mc"][direction]
            move_sprite(direction)
        elif button_press and event.key == pygame.K_RIGHT:
            direction = "right"
            res["mc current"] = res["mc"][direction]
            move_sprite(direction)
        elif button_press and event.key == pygame.K_UP:
            direction = "up"
            res["mc current"] = res["mc"][direction]
            move_sprite(direction)

        update_screen()
        advance_frame()
        
        # Restrict framerate
        pygame.time.Clock().tick(10)

play()
    
