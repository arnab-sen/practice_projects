"""
Defines the interactive objects in Pokemon World (e.g. NPCs, signs, doors)

## NPC ##
* Sprites are filenames (e.g. "Professor Oak L 0.png" or just
  "Professor Oak L 0" for the first left-facing frame of the sprite),
  and are loaded into pygame within the class

"""

import pygame

class Interactive:

    def __init__(self, name, text):
        self.name = name
        self.text = text

class NPC(Interactive):

    def __init__(self, name, text):
        super().__init__(self, name, text)
        sprites = self.load_sprites()

    def load_sprites(self, sprites):
        loaded_sprites = {}
        frames = []        
        folder = "Resources/Overworld/NPCs/" + str(self.name) + "/"

        directions = ["U", "D", "L", "R"]
        num_frames = 4
        for direction in directions:
            for i in range(num_frames):
                filename = "{} {} {}.png".format(self.name, direction, i)
                frames.append(pygame.image.load(folder + filename))
            loaded_sprites[direction] = frames
            frames = []
            

        return loaded_sprites
            
