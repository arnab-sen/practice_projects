"""
Defines the pokemon class and battle logic between two pokemon

TODO:
- Change class functions to get stats from get_pokemon_info
- Import two pokemon from a dict in a txt file
- Begin with pokemon having two stats: HP and attack power
- Pokemon have up to four moves each and take turns attacking
- First one to 0 HP loses the battle
"""

import ast
import get_pokemon_info
import random

class Pokemon:

    def __init__(self, name, HP, ATK, moves):
        self._name = name
        self._max_HP = HP
        self._HP = HP
        self._ATK = ATK
        self._moves = moves

    def set_name(self, value):
        self._name = value

    def get_name(self):
        return self._name

    def set_HP(self, value):
        self._HP = value

    def get_max_HP(self):
        return self._max_HP
    
    def get_HP(self):
        return self._HP

    def set_ATK(self, value):
        self._name = value

    def get_ATK(self):
        return self._ATK

    def set_moves(self, value):
        self._moves = values

    def get_moves(self, index):
        return self._moves[index]
    

    name = property(get_name, set_name)
    max_HP = property(get_max_HP, None)
    HP = property(get_HP, set_HP)
    ATK = property(get_ATK, set_ATK)
    moves = property(get_moves, set_moves)

def get_pokemon_names():
    return get_pokemon_info.get_dict("numbered_pokemon.txt")

def calculate_damage(attacker, defender):
    placeholder_damage = 50
    return placeholder_damage

def initialise_battle(names, HPs, ATKs):
    pokemon1 = Pokemon(names[0], HPs[0], ATKs[0])
    pokemon2 = Pokemon(names[1], HPs[1], ATKs[1])
    #print(pokemon1.name, pokemon1.HP, pokemon1.ATK)
    #print(pokemon2.name, pokemon2.HP, pokemon2.ATK)
    pokemon = [pokemon1, pokemon2]
    return pokemon

def attack(attacker, defender):
    a = attacker
    d = defender
    damage = calculate_damage(a, d)
    #print(a.name + " attacks " + d.name)
    #print(d.name + "'s HP fell from " + str(d.HP), end = "")
    d.HP = d.HP - a.ATK
    if d.HP < 0: d.HP = 0
    #print(" to " + str(d.HP))

if __name__ == "__main__":
    pokemon = get_pokemon_names()
    #names = get_battle_data()
    nums = [random.randrange(1, 650), random.randrange(1, 650)]
    nums[0] = get_pokemon_info.pokemon_number(nums[0])
    nums[1] = get_pokemon_info.pokemon_number(nums[1])
    names = [pokemon[nums[0]], pokemon[nums[1]]]
    HPs = [100, 150]
    ATKs = [50, 25]
    pokemon = initialise_battle(names, HPs, ATKs)
    f1 = pokemon[0]
    f2 = pokemon[1]
    print(f1.name + "'s HP: " + str(f1.max_HP))
    attack(f1, f2)
    attack(f2, f1)
