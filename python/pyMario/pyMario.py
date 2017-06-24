"""This is recreation of Super Mario Bros. for the NES

"""
import pygame
import map_editor, utils
from PIL import Image

# GLOBALS
res = {} # A resource dictionary

class Entity:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.load_sprites()
        self.postion = [0, 0]

    def load_sprites(self):
        self.sprite_png = Image.open(self.path + "/" + self.name + ".png")
        self.sprite_png = utils.scale_image(res["scale"], self.sprite_png)
        self.sprite_pygame = utils.image_to_pygame(self.sprite_png)

class Mario(Entity):
    def __init__(self, name, path):
        super().__init__(name, path)

    def jump(self):
        self.position[1] -= 1
    

def set_current_map():
    map_name = "1_1"

    return map_name

def load_map(map_name):
    pass

def load_character():
    path = "Resources/Images/Playable"
    name = "mario"
    res["mario"] = Mario(name, path)

    return res["mario"]

def main():
    pass

def test_main():
    image_scale = 2
    res["scale"] = image_scale
    test_map = map_editor.Map(scale = image_scale)
    pygame.init()
    #screen_size = (1280, 720)
    screen_size = (1000, test_map.image_png.size[1])
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("pyMario")
    window_icon = pygame.image.load("Resources/Images/Other/pyMario_icon.png")
    pygame.display.set_icon(window_icon)
    map_position = [0, 0] #[-5000, 0] for near the end
    move_pixels = round(2.5 * image_scale)
    mario = load_character()
    mario.position = [screen_size[0] // 2, screen_size[1] - 80]
    
    while 1:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if keys[pygame.K_ESCAPE] or event.type == pygame.QUIT:
                pygame.display.quit()
                return
        if keys[pygame.K_RIGHT]:
            at_right_border = map_position[0] <= -5750
            if not at_right_border:
                map_position[0] -= move_pixels
        elif keys[pygame.K_LEFT]:
            at_left_border = -1 * map_position[0] < 0
            if not at_left_border:
                map_position[0] += move_pixels
        elif keys[pygame.K_UP]:
            mario.jump()
            
        
        screen.blit(test_map.image_pygame, map_position)
        screen.blit(mario.sprite_pygame, mario.position)
        pygame.display.flip()

def TODO():
    """
    * Stop map movement at the left and right edges of the map
    * 
    """
    pass

if __name__ == "__main__":
    main()
    test_main()
