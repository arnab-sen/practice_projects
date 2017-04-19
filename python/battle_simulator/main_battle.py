import sys, pygame, time, random
import battle_logic, get_pokemon_info

def initialise_display():
    moves_top_left = (18, 356)
    moves_center = (240, 410)
    quadrant_width = moves_center[0] - 18
    quadrant_height = moves_center[1] - 356
    quadrant_1 = pygame.Rect(18, 356, quadrant_width, quadrant_height)
    quadrant_2 = pygame.Rect(241, 356, quadrant_width, quadrant_height)
    quadrant_3 = pygame.Rect(18, 410, quadrant_width, quadrant_height)
    quadrant_4 = pygame.Rect(241, 410, quadrant_width, quadrant_height)
    move_quadrants = [quadrant_1, quadrant_2, quadrant_3, quadrant_4]

def get_moves(pokemon_num):
    num = str(pokemon_num)
    all_moves = get_pokemon_info.get_dict("pokemon_movesets")
    pokemon_moveset = all_moves[num]
    move_list = []
    for i in range(len(pokemon_moveset[0]), 3)
        move_list += []
        # Need to have a dict of moves from attackdex
