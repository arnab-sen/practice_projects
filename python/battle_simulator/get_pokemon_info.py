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
    pokemon = ""
    p, text = get_pokemon_from_region(text, "Bulbasaur", "Mew", "Kanto:")
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
        dict_string += "\t" + element[:space] + " : "
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
    
def main():
    pokemon = "001"
    url = "http://www.serebii.net/pokedex-bw/" + pokemon + ".shtml"
    #with open("hello_world.txt", 'w') as file:
    #    file.write("Hi\n")
    
    pokemon_list = get_pokemon_list()
    pokemon_list_to_dict_string(pokemon_list)

main()

