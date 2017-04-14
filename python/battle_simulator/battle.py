"""
TODO:
- Import two fighters from a dict in a txt file
- Begin with fighters having two stats: HP and attack power
- Fighters have up to four moves each and take turns attacking
- First one to 0 HP loses the battle
"""

class Fighter:
    "Has HP and ATK"

    def __init__(self, name, HP, ATK):
        self._name = name
        self._HP = HP
        self._ATK = ATK

    @property
    def name(self):
        "name getter"
        return self._name

    @name.setter
    def name(self, value):
        "name setter"
        self.name = value
    
    @property
    def HP(self):
        "HP getter"
        return self._HP

    @HP.setter
    def HP(self, value):
        "HP setter"
        self.HP = value
    
    @property
    def ATK(self):
        "ATK getter"
        return self._ATK

    @ATK.setter
    def ATK(self, value):
        "ATK setter"
        self._ATK = value
    

def get_battle_data():
    with open("data.txt") as file:
        pass
    pass

def initialise_battle(names, HPs, ATKs):
    fighter1 = Fighter(names[0], HPs[0], ATKs[0])
    fighter2 = Fighter(names[1], HPs[1], ATKs[1])
    #print(fighter1.name, fighter1.HP, fighter1.ATK)
    #print(fighter2.name, fighter2.HP, fighter2.ATK)
    fighters = [fighter1, fighter2]
    return fighters

def attack(attacker, defender):
    a = attacker
    d = defender
    d_HP = d.HP
    a_ATK = a.ATK
    print(a.name + " attacks " + d.name)
    print(d.name + "'s HP fell from " + str(d.HP), end = "")
    d.HP(d_HP - a_ATK)
    print(" to " + str(d.HP))

def battle(fighters):
    pass

def main():
    names = ["F1", "F2"]
    HPs = [100, 150]
    ATKs = [50, 25]
    fighters = initialise_battle(names, HPs, ATKs)
    f1 = fighters[0]
    f2 = fighters[1]
    print(f1.name + "'s HP: " + str(f1.HP))
    attack(f1, f2)
    attack(f2, f1)

main()    
