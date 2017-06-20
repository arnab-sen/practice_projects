"""Useful tools/utilities to use for pyMario
"""

from PIL import Image
import pygame

def scale_image(scale, image):
    width, height = image.size
    image = image.resize((width * scale, height * scale))

    return image

def image_to_pygame(image):
    """Converts a PIL Image to a pygame Surface,
    useful for when scale_image() is required in
    between loading the image and using it in pygame"""
    
    image_data = image.tobytes(), image.size, image.mode    
    pygame_image =  pygame.image.fromstring(*image_data)

    return pygame_image
