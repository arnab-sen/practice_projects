"""
Defines the pokemon class and battle logic between two pokemon
"""

import ast
import get_pokemon_info
import random

class Pokemon:

    def __init__(self, name, HP, ATK):
        self._name = name
        self._HP = HP
        self._ATK = ATK

    def set_name(self, value):
        self._name = value

    def get_name(self):
        return self._name

    def set_HP(self, value):
        self._HP = value

    def get_HP(self):
        return self._HP

    def set_ATK(self, value):
        self._name = value

    def get_ATK(self):
        return self._ATK

    name = property(get_name, set_name)
    HP = property(get_HP, set_HP)
    ATK = property(get_ATK, set_ATK)

def get_pokemon_names():
    pokemon = get_pokemon_info.get_dict("numbered_pokemon.txt")
    return pokemon

def calculate_damage(attacker, defender):
    pass

def attack(attacker, defender):
    a = attacker
    d = defender
    damage = calculate_damage(a, d)
    print(a.name + " attacks " + d.name)
    print(d.name + "'s HP fell from " + str(d.HP), end = "")
    d.HP = d.HP - a.ATK
    print(" to " + str(d.HP))
