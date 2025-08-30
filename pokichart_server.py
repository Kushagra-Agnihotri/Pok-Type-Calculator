import json
import threading
import requests
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pokiapi_type_chart import *
from urllib.parse import urlparse, parse_qs



class TypeChartHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        if parsed_url.path == '/typechart':
            query = parse_qs(parsed_url.query)
            attacker = query.get('attacker', [None])[0]
            defender = query.get('defender', [None])[0]
            #print(attacker,defender)
            if attacker and defender:
                try:
                    effectiveness = relations[defender][all_pokemon_types.index(attacker)]
                    response = {'effectiveness': effectiveness}
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode())
                except (KeyError, ValueError):
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'Invalid attacker or defender type')
            elif defender:
                try:
                    def_relations = relations[defender]
                    atk_dict = {}
                    for i in all_pokemon_types:
                        atk_dict[i] = def_relations[all_pokemon_types.index(i)]

                    response = {"defender":defender,"from_attackers": atk_dict }
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode())

                except(KeyError,ValueError):
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(self.wfile.write(b'Invalid defender type'))
            elif attacker:
                try:
                    def_dict = {}
                    for i in all_pokemon_types:
                        id = all_pokemon_types.index(i)
                        def_dict[i] = matrix[len(matrix)-id -1][0]
                    

                    response = {"attacker":attacker,"to_defender": def_dict }
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode())

                except(KeyError,ValueError):
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(self.wfile.write(b'Invalid defender type'))
            else:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(type_chart).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')
    def log_message(self, format, *args):
        pass
def run(server_class=HTTPServer, handler_class=TypeChartHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print('Server running on http://localhost:8000/typechart')
    httpd.serve_forever()

def calculateMultipliers(double_dmg, zero_dmg) -> dict:

    all_types = list(all_pokemon_types)
    
    final_multipliers = {}
    
    for attacking_type in all_types:
        multiplier = 1.0
        

        for defending_type in double_dmg.keys():
            if attacking_type in double_dmg[defending_type]:
                multiplier *= 2.0
            elif attacking_type in zero_dmg[defending_type]:
                multiplier = 0.0
                break  
        
        final_multipliers[attacking_type] = multiplier
    
    return final_multipliers 

def runserver():
    run()
if __name__ == '__main__':
    print("="*50)
    print("WELCOME TO POKI API")
    print("="*50)
     
    server_thread = threading.Thread(target=run, daemon=True)
    server_thread.start()
    
    time.sleep(2)
    
    T_URL = "http://localhost:8000/typechart"
    
    print("Pokemon Type Calculator - Enter 'quit' or 'exit' to stop")
    print("=" * 50)

    while True:
        try:
            print("\nEnter the name of the pokemon (or 'quit' to exit): ")
            x = input().strip().lower()
            
            # Check for exit commands
            if x in ['quit', 'exit', 'q', 'stop']:
                print("Goodbye! Shutting down...")
                break
            
            if not x:
                print("Please enter a valid Pokemon name.")
                continue
            
            print(f"\nFetching data for {x.title()}...")
            
            URL = f"https://pokeapi.co/api/v2/pokemon/{x}"

            try:
                data = requests.get(URL)
                if data.status_code == 404:
                    print(f"Pokemon '{x}' not found. Please check the spelling.")
                    continue
                elif data.status_code != 200:
                    print(f"Error: HTTP {data.status_code}")
                    continue
                    
            except requests.exceptions.ConnectionError:
                print("Could not connect to PokeAPI. Please check your internet connection.")
                continue
            except Exception as e:
                print(f"Error: {e}")
                continue
      
            data_json = data.json()
            pokemon_name = data_json["name"].title()
            pokemon_type = [x["type"]["name"] for x in data_json["types"]]
            
            print(f"\n{pokemon_name} is a {'/'.join(pokemon_type).title()} type Pokemon!")
            print("=" * 40)
             
            doubl_dmg = {}
            zero_dmg = {}
            
            for pokemon_type_name in pokemon_type:
                try:
                    param = {"defender": pokemon_type_name}
                    type_data = requests.get(T_URL, params=param)
                    
                    if type_data.status_code != 200:
                        print(f"Error getting type data for {pokemon_type_name}")
                        continue
                        
                except requests.exceptions.ConnectionError:
                    print("Could not connect to local server. Make sure it's running.")
                    continue
                except Exception as e:
                    print(f"Error: {e}")
                    continue
                
                type_multipliers = dict(type_data.json())
                dtemp = []
                ztemp = []
                
                for i, j in type_multipliers["from_attackers"].items():
                    if j == 2.0:
                        dtemp.append(i)
                    elif j == 0.0:
                        ztemp.append(i)
                        
                doubl_dmg[pokemon_type_name] = dtemp
                zero_dmg[pokemon_type_name] = ztemp

            print(f"\n{pokemon_name}'s Type Analysis:")
            print("=" * 30)
            
            print("\nDouble damage types:")
            for pokemon_type_name, weak_types in doubl_dmg.items():
                if weak_types:
                    print(f"  {pokemon_type_name.title()}: {', '.join(weak_types).title()}")
                else:
                    print(f"  {pokemon_type_name.title()}: None")

            print("\nZero damage types (Immunities):")
            for pokemon_type_name, immune_types in zero_dmg.items():
                if immune_types:
                    print(f"  {pokemon_type_name.title()}: {', '.join(immune_types).title()}")
                else:
                    print(f"  {pokemon_type_name.title()}: None")

            # Final multipliers
            final_multipliers = calculateMultipliers(doubl_dmg, zero_dmg)

            print("\nFinal Damage Multipliers:")
            print("-" * 25)
            
            multiplier_groups = {}
            for attacking_type, multiplier in final_multipliers.items():
                if multiplier not in multiplier_groups:
                    multiplier_groups[multiplier] = []
                multiplier_groups[multiplier].append(attacking_type)
            
            #Final damage multi
            for multiplier in sorted(multiplier_groups.keys(), reverse=True):
                if multiplier != 1.0:  # Skip normal effectiveness
                    types_list = ', '.join(multiplier_groups[multiplier]).title()
                    if multiplier == 0.0:
                        print(f"  Immune (0x): {types_list}")
                    elif multiplier == 4.0:
                        print(f"  4x Weak: {types_list}")
                    elif multiplier == 2.0:
                        print(f"  2x Weak: {types_list}")
                    elif multiplier == 0.5:
                        print(f"  0.5x Resistant: {types_list}")
                    elif multiplier == 0.25:
                        print(f"  0.25x Very Resistant: {types_list}")
            
            print("\n" + "=" * 50)
            
        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Shutting down...")
            break
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            print("Please try again or enter 'quit' to exit.")
            continue

    print("\nServer is running in background. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
 
