"""
This takes an input folder of PNG tiles, displays them, and allows
the user to determine the status of each tile (can_collide, cannot_collide,
NPC, etc.) by clicking on it. Different colours surrounding the tiles
indicate different statuses.
"""
import pygame, sys
from PIL import Image
BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
SIZE = 1000, 750
screen = pygame.display.set_mode(SIZE)
TILE_DIM = 48
GRID_SEP = 10
PATH = "Resources\\Overworld\\Tiles\\Saved\\"
map_info = {}

def scale_image(scale, image):
    width, height = image.size
    image = image.resize((width * scale, height * scale))

    return image

def get_base(filename):
    filename = PATH + "\\" + filename + "\\" + filename
    filename += ".png"
    image = Image.open(filename)
    image = scale_image(3, image)
    row, col = round(image.size[0] / TILE_DIM), round(image.size[1] / TILE_DIM)

    return row, col  

def load_tiles(tiles_folder):
    tiles = []
    path = PATH + tiles_folder + "\\"
    file_base = path + tiles_folder + " [{}, {}].png"
    tiles_per_row = map_info[tiles_folder][1]
    tiles_per_col = map_info[tiles_folder][2]
    tiles = [[""] * tiles_per_row] * tiles_per_col

    for i in range(tiles_per_col):
        for j in range(tiles_per_row):
            tile = Image.open(file_base.format(i, j))
            print(tile.size)
            tile = image_to_pygame(tile)
            tiles[i][j] = tile

    return tiles

def update_screen(tiles):
    screen.fill(WHITE)
    screen.blit(tiles[0][0], (0, 0))
    screen.blit(tiles[0][1], (TILE_DIM + GRID_SEP, 0))

def advance_frame():
    pygame.display.flip()

def image_to_pygame(image):
    image_data = image.tobytes(), image.size, image.mode

    return pygame.image.fromstring(*image_data)
    
def play():
    #tiles_folder = input("Enter your tiles folder name: ")
    tiles_folder = "pallet town"
    tiles_per_row, tiles_per_col = get_base(tiles_folder)
    tile_info = [tiles_folder, tiles_per_row, tiles_per_col]
    map_info["current"] = tiles_folder
    map_info[tiles_folder] = tile_info
    tiles = load_tiles(tiles_folder)
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
                
        #update_screen(tiles)
        screen.blit(tiles[0][0], (0, 0))
        advance_frame()

play()
