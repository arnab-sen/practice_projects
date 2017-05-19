"""
This takes a PNG image as input, and for given tile dimensions, converts
that image into a series of tiles, and saves the tiles to a folder.
"""
import os
from PIL import Image
TILE_SIZE_ORIGINAL = (16, 16)
TILE_SIZE = (TILE_SIZE_ORIGINAL[0] * 3, TILE_SIZE_ORIGINAL[1] * 3)
TILE_DIM = TILE_SIZE[0]
TEST_OPEN_PATH = "Resources\\Overworld\\Tiles\\Input\\"
TEST_SAVE_PATH = "Resources\\Overworld\\Tiles\\Saved\\"

def scale_image(scale, image):
    width, height = image.size
    image = image.resize((width * scale, height * scale))

    return image

def get_map(filename):
    filename += ".png"
    image = Image.open(TEST_OPEN_PATH + filename)

    return scale_image(3, image)

def make_tiles(image):
    tiles = []
    tile_pos = [0, 0]
    tiles_per_row = round(image.size[0] / TILE_SIZE[0])
    crop_pos = [0, 0, *TILE_SIZE]
    # Get the first row
    for tile in range(tiles_per_row):
        crop_pos[0] = (TILE_DIM * tile)
        crop_pos[2] = crop_pos[0] + TILE_DIM
        print(tuple(crop_pos))
        tiles.append(image.crop(crop_pos))

    return tiles

def save_tiles(tiles, filename):
    
    #for tile in tiles:
    #    tile.save(TEST_SAVE_PATH + filename)
    for i, tile in enumerate(tiles):
        tile.save(TEST_SAVE_PATH + filename + " " + str(i) + ".png")
    #tiles[0].save(TEST_SAVE_PATH + filename + " " + str(i) + ".png")

def main():
    filename = "pallet town"
    image = get_map(filename)
    tiles = make_tiles(image)
    save_tiles(tiles, filename)

if __name__ == "__main__":
    main()
    
