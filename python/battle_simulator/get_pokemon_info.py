"""
This program retrieves pokemon information from http://www.serebii.net
and saves the information in text files:
- List of pokemon and their number in the B/W national dex
  e.g. { 001 : "Bulbasaur" }
- Moveset of pokemon from the B/W pokedex
  e.g. { 001 : ["Tackle", "Growl", ...] }
- Moves from the B/W attackdex
  e.g. { "Tackle" : [50, 100, "Physical"] }
- Base stats for each pokemon
"""
import urllib.request
import os.path
import ast
from bs4 import BeautifulSoup

def get_pokemon_from_region(main_text, first_pokemon, last_pokemon, region):
    # First string is e.g. "001 Bulbasaur", argument provides "Bulbasaur"
    main_text = main_text[main_text.find(region):]
    start = main_text.find(first_pokemon) - 4
    end = main_text.find(last_pokemon) + len(last_pokemon)
    
    return main_text[start : end] + "\n", main_text[start:]
        
def get_pokemon_list():
    url = "http://www.serebii.net/pokedex-bw/001.shtml"
    main_text = get_html(url, "text")
    text = main_text
    #print(main_text)
    pokemon = ""
    # Mew requires the number as 150 is Mewtwo, so just providing "Mew"
    # causes the program to stop at Mewtwo
    p, text = get_pokemon_from_region(text, "Bulbasaur", "151 Mew", "Kanto:")
    pokemon += p
    p, text = get_pokemon_from_region(text, "Chikorita", "Celebi", "Johto:")
    pokemon += p
    p, text = get_pokemon_from_region(text, "Treecko", "Deoxys", "Hoenn:")
    pokemon += p
    p, text = get_pokemon_from_region(text, "Turtwig", "Arceus", "Sinnoh:")
    pokemon += p
    p, text = get_pokemon_from_region(text, "Victini", "Genesect", "Unova:")
    pokemon += p

    return pokemon.split("\n")
    
def pokemon_list_to_dict_string(pokemon_list):
    # Convert list to dict {num : "name", ...}
    dict_string = "{\n"
    for element in pokemon_list:
        element = element.strip()
        if len(element) < 2: break
        space = element.find(" ")
        dict_string += "\t \"" + element[:space] + "\" : "
        dict_string += "\"" + element[space + 1:] + "\""
        if element != pokemon_list[-2]: dict_string += ",\n"
    dict_string += "\n}"

    # Write list to a txt file
    with open("Resources\\numbered_pokemon.txt", 'w') as file:
        file.write(dict_string)
        
    return dict_string
    
def get_html(url, form):
    with urllib.request.urlopen(url) as response:
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")

    if form == "messy": return soup
    if form == "neat": return soup.prettify()
    if form == "text": return soup.get_text()
    else:
        raise Exception("Incorrect form argument in get_html(url, form)")

def get_numbered_pokemon():
    if not(os.path.isfile("Resources\\numbered_pokemon.txt")):    
        pokemon_list = get_pokemon_list()
        pokemon_list_to_dict_string(pokemon_list)
    else: print("numbered_pokemon.txt already exists! Using the existing file.")    

def pokemon_number(number):
    if int(number) < 1 or int(number) > 649: number = "001"
    number = str(number)
    return ["00" + number, "0" + number, number][len(number) - 1]

def is_integer(string):
    try: i = int(string)
    except: return False

    return True
    
def get_pokemon_movesets():
    move_sets = {} # {pokemon_num : [move name, attack, accuracy]}
    with open("Resources\\numbered_pokemon.txt", 'r') as file:
        numbered_pokemon = ast.literal_eval(file.read())
    for n in range(1, 650):
        pokemon = n
        move_level = 0
        pokemon_num = pokemon_number(str(pokemon))
        url = "http://www.serebii.net/pokedex-bw/" + pokemon_num + ".shtml"
        page_text = get_html(url, "text")
        page_text = page_text[page_text.find("Level Up"):]
        #print(page_text)
        moves_list = page_text.split("\n")
        m = moves_list
        temp_moves = []
        for i in range(1, len(m)):
            if m[i] != "" and m[i] != "Details" and m[i][0].isalpha() \
               and len(m[i]) < 20:
                if is_integer(m[i - 1]) or m[i - 1] == "-":
                    # Continue loop until the highest level up move is found
                    if int(m[i - 1]) < move_level: break
                    else:
                        temp_moves += [[m[i], m[i + 3], m[i + 4]]]
                        move_level = int(m[i - 1])
        print(pokemon_num + " -- " + numbered_pokemon[pokemon_num] + " done!")               
        move_sets[pokemon_num] = [temp_moves]

    if not(os.path.isfile("Resources\\pokemon_movesets.txt")):    
        with open("Resources\\pokemon_movesets.txt", 'w') as file:
            file.write(str(move_sets))
    else: print("pokemon_movesets.txt already exists! Using the existing file.")
            
def get_dict(dict_name):
    try:
        with open("Resources\\" + dict_name, 'r') as file:
            return ast.literal_eval(file.read())
    except:
        print("File " + dict_name + " not found!")

if __name__ == "__main__":
    #get_numbered_pokemon()
    #get_pokemon_movesets()
    

    print(len(numbered_pokemon))
      

