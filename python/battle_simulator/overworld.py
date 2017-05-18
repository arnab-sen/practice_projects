"""
"""

import sys, pygame
from PIL import Image

res = {}
BLACK = 0, 0, 0
ANTI_ALIAS = True
SIZE = 720, 480
screen = pygame.display.set_mode(SIZE)
TILE_MOVEMENT = 15

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
    return pygame.image.fromstring(*image_data)

def load_character(character_name):
    pass

def load_resources():
    #res["pallet town"] = pygame.image.load(location("pallet town.png"))
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
    res["mc pos"] = [SIZE[0] / 2 - 21, SIZE[1] / 2 - 28]
    res["mc current"] = res["mc"]["down"]
    res["mc frame"] = 0
    
def update_screen():
    screen.fill(BLACK)
    screen.blit(res["map"], res["map pos"])
    screen.blit(res["mc current"][res["mc frame"]], res["mc pos"])

def advance_frame():
    pygame.display.flip()

def play():
    load_resources()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                res["mc current"] = res["mc"]["down"]
                res["mc frame"] = (res["mc frame"] + 1) % len(res["mc current"])
                res["map pos"][1] -= TILE_MOVEMENT
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                res["mc current"] = res["mc"]["left"]
                res["mc frame"] = (res["mc frame"] + 1) % len(res["mc current"])
                res["map pos"][0] += TILE_MOVEMENT
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                res["mc current"] = res["mc"]["right"]
                res["mc frame"] = (res["mc frame"] + 1) % len(res["mc current"])
                res["map pos"][0] -= TILE_MOVEMENT
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                res["mc current"] = res["mc"]["up"]
                res["mc frame"] = (res["mc frame"] + 1) % len(res["mc current"])
                res["map pos"][1] += TILE_MOVEMENT

        update_screen()
        advance_frame()
        pygame.time.Clock().tick(10)

play()
    
