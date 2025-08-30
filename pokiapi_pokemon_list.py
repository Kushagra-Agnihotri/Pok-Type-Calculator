import requests
import sys
import json


if len(sys.argv) < 2:
    print("Usage: python pokiapi_pokemon_list.py <output_filename.json>")
    sys.exit(1)

output_filename = sys.argv[1]
PATH = "pokemon.txt"

txt = []
with open(PATH, "r") as f:
    txt = f.readlines()

all_pokemon = {}

for pokemon in txt:
    pokemon_name = pokemon.strip("\n")
    URL_Pokemon = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    obj_pokemon = requests.get(URL_Pokemon)
    if obj_pokemon.status_code != 200:
        print(f"Error fetching {pokemon_name}: {obj_pokemon.status_code}")
        continue
    pokemon_dict = obj_pokemon.json()

    ability_list = []
    type_list = []
    for ability in pokemon_dict["abilities"]:
        ability_list.append(ability["ability"]["name"])
    for type in pokemon_dict["types"]:
        type_list.append(type["type"]["name"])

    species_name = pokemon_dict["species"]["name"]
    URL_SPECIES = f"https://pokeapi.co/api/v2/pokemon-species/{species_name}"
    obj_species = requests.get(URL_SPECIES)
    if obj_species.status_code != 200:
        print(f"Error fetching species for {species_name}: {obj_species.status_code}")
        continue
    species_dict = obj_species.json()

    all_pokemon[species_name] = {
        "id": pokemon_dict["id"],
        "abilities": ability_list,
        "types": type_list,
        "is_mythical": species_dict['is_mythical'],
        "is_legendary": species_dict["is_legendary"],
    }

with open(output_filename, "w") as out_file:
    json.dump(all_pokemon, out_file, indent=4)

print(f"Data written to {output_filename}")









