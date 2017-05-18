"""
"""

import sys, pygame
from PIL import Image

res = {}
BLACK = 0, 0, 0
ANTI_ALIAS = True
SIZE = 720, 480
screen = pygame.display.set_mode(SIZE)

def location(filename):
    return "Resources\\Overworld\\" + filename

def scale_image(scale, image):
    width, height = image.size
    image = image.resize((width * scale, height * scale))#, Image.ANTIALIAS)
    # including Image.ANTIALIAS makes a blurry scaled image

    return image

def load_image(name):
    image = Image.open(location(name + ".png"))
    image = scale_image(3, image)
    image_data = image.tobytes(), image.size, image.mode
    res[name] = pygame.image.fromstring(*image_data)

def load_character(character_name):
    pass

def load_resources():
    #res["pallet town"] = pygame.image.load(location("pallet town.png"))
    image = Image.open(location("pallet town.png"))
    image = scale_image(3, image)
    image_data = image.tobytes(), image.size, image.mode
    load_image("pallet town")
    load_image("mc fw neutral")

def update_screen():
    screen.fill(BLACK)
    screen.blit(res["pallet town"], (0, 0))
    screen.blit(res["mc fw neutral"], (200, 100))

def advance_frame():
    pygame.display.flip()

def play():
    load_resources()
    update_screen()
    advance_frame()
    
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()

play()
    
