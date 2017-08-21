"""
A chess game made with pygame
Redesigned from the ground up from v1.0 to better use OOP
"""

import pygame, sys, os
from PIL import Image

class Chessboard():
	def __init__(self, bw = False):
		filename = "chessboard_BW.png" if bw else "chessboard.png"
		self.__image = pygame.image.load("Resources/" + filename)

	def show(self):
		screen.blit(self.__image, (0, 0))

class Chesspiece():
	def __init__(self, name):
		self.__name = name
		self.__load_image()

	def __load_image(self):
		filename = self.__name + ".png"
		self.__image = pygame.image.load("Resources/" + filename)

	def show(self, position = (0, 0)):
		screen.blit(self.__image, position)

def initialise():
	global screen
	screen = pygame.display.set_mode((401, 401))
	pygame.init()
	pygame.display.set_caption("Chess")

	chessboard = Chessboard()

	return chessboard

def main():
	chessboard = initialise()
	testpiece = Chesspiece("placeholder_piece")

	while 1:
		keys = pygame.key.get_pressed()
		for event in pygame.event.get():
			if keys[pygame.K_ESCAPE] or event.type == pygame.QUIT:
				pygame.display.quit()
				return

		chessboard.show()
		testpiece.show()
		pygame.display.flip()


if __name__ == "__main__":
	main()

