"""Generic map editor to use with any pygame program
"""

import pygame
import utils # local utils.py file
from PIL import Image

class Map:

    def __init__(self, filename = None, path = None, scale = None):
        self.name = filename if filename else "dummy_map"
        self.path = path if path else "Test"
        self.scale = scale if scale else 1
        self.load_map_info()

    def load_map_info(self):
        image = Image.open(self.path + "/" + self.name + ".png")
        image = utils.scale_image(self.scale, image)
        with open(self.path + "/" + self.name + "_info.txt") as file:
            map_info = file.read()

        self.image_png = image
        self.image_pygame = utils.image_to_pygame(image)
        self.map_info = map_info

def test_main():
    test_map = Map(scale = 2)
    pygame.init()
    #screen_size = (1280, 720)
    screen_size = (1000, test_map.image_png.size[1])
    screen = pygame.display.set_mode(screen_size)
    map_position = [0, 0]
    move_pixels = 5
    while 1:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if keys[pygame.K_ESCAPE]:
                pygame.display.quit()
                return
        if keys[pygame.K_RIGHT]:
            map_position[0] -= move_pixels
        elif keys[pygame.K_LEFT]:
            map_position[0] += move_pixels
            
        
        screen.blit(test_map.image_pygame, map_position)
        pygame.display.flip()
    



if __name__ == "__main__":
    test_main()
