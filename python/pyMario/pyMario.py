"""This is recreation of Super Mario Bros. for the NES

"""
import pygame
import map_editor
from PIL import Image

# GLOBALS
res = {} # A resource dictionary

def set_current_map():
    map_name = "1_1"

    return map_name

def load_map(map_name):
    pass

def main():
    pass

def test_main():
    image_scale = 2
    test_map = map_editor.Map(scale = image_scale)
    pygame.init()
    #screen_size = (1280, 720)
    screen_size = (1000, test_map.image_png.size[1])
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("pyMario")
    window_icon = pygame.image.load("Resources/Images/Other/pyMario_icon.png")
    pygame.display.set_icon(window_icon)
    map_position = [0, 0]
    move_pixels = round(2.5 * image_scale)
    while 1:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if keys[pygame.K_ESCAPE] or event.type == pygame.QUIT:
                pygame.display.quit()
                return
        if keys[pygame.K_RIGHT]:
            map_position[0] -= move_pixels
        elif keys[pygame.K_LEFT]:
            map_position[0] += move_pixels
            
        
        screen.blit(test_map.image_pygame, map_position)
        pygame.display.flip()

if __name__ == "__main__":
    main()
    test_main()
