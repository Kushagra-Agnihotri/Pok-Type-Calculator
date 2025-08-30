import requests
import matplotlib.pyplot as plt
import numpy as np
import json

all_pokemon_types = ["normal", "fire", "water", "grass", "electric", "ice", "fighting", "poison", "ground", "flying", "psychic", "bug", "rock", "ghost", "dragon", "dark", "steel", "fairy"]

relations = {}

for j in all_pokemon_types:
    URL = f"https://pokeapi.co/api/v2/type/{j}"
    types = requests.get(URL)
    #print("compiling for type: ",j , " statuscode: "  ,types.status_code)

    if types.status_code != 200:
        continue
    pokemon_types_dict = types.json()
    type_relations = pokemon_types_dict["damage_relations"] 

    double_dmg_from = [x["name"] for x in type_relations["double_damage_from"]]        
    half_damage_from = [x["name"] for x in type_relations["half_damage_from"]]
    no_damage_from = [x["name"] for x in type_relations["no_damage_from"]]

    row = []
    for i in all_pokemon_types:
        if i not in double_dmg_from and i not in half_damage_from and i not in no_damage_from:
            row.append(1)
        elif i in double_dmg_from:
            row.append(2)
        elif i in half_damage_from:
            row.append(0.5)
        elif i in no_damage_from:
            row.append(0)
    relations[j] = row



type_chart = json.dumps(relations)
matrix = []

for i,j in relations.items():
    matrix.append(j)
     
#print()
#print(matrix)

relations_flipped = matrix[::-1]
matrix = np.array(relations_flipped)
y_labels_flipped = [t.capitalize() for t in all_pokemon_types[::-1]]
x_labels = [t.capitalize() for t in all_pokemon_types]

plt.figure(figsize=(8, 10))
ax = plt.gca()

for i in range(len(all_pokemon_types)):
    for j in range(len(all_pokemon_types)):
        value = matrix[i, j]
        if value == 2:
            color = 'limegreen'
            text = '2'
        elif value == 0.5:
            color = 'red'
            text = '0.5'
        elif value == 0:
            color = 'black'
            text = '0'
        else:
            color = 'white'
            text = ''


        #Drawing the cell    
        rect = plt.Rectangle([j, i], 1, 1, facecolor=color, edgecolor='gray')
        ax.add_patch(rect)


        #Setting the text in the celll
        if text:
            plt.text(j + 0.5, i + 0.5, text, ha='center', va='center', color='white' if color == 'black' else 'black', fontsize=14, fontweight='bold')

#Adding labels in the plot
plt.xticks(np.arange(len(all_pokemon_types)) + 0.5, x_labels, rotation=45, fontsize=12)
plt.yticks(np.arange(len(all_pokemon_types)) + 0.5, y_labels_flipped, fontsize=12)
plt.xlim(0, len(all_pokemon_types))
plt.ylim(0, len(all_pokemon_types))
plt.xlabel("Attacking Type", fontsize=14)
plt.ylabel("Defending Type", fontsize=14)
plt.title("Pokémon Type Effectiveness Chart", fontsize=16)
plt.gca().invert_yaxis()  

plt.tight_layout()
#plt.show()









