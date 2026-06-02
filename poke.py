import requests
from PIL import Image
from io import BytesIO
from ascii_magic import from_url


id = input()
spec_url = f"https://pokeapi.co/api/v2/pokemon-species/{id}/"
abi_url = f"https://pokeapi.co/api/v2/pokemon/{id}/"
response = requests.get(spec_url)
response2 = requests.get(abi_url)

poke_info = response.json()
ability_info = response2.json()

if poke_info:
    print("Name: ", id)
    print("ID: ", poke_info["order"])
    print("ID(per gen): ", poke_info["pokedex_numbers"][0]["entry_number"])
    print("Gen: ", poke_info["generation"]["name"])
    print("Hieght: ", ability_info["height"])
    print("Weight: ", ability_info["weight"])
    print("Ability: ", ability_info["abilities"][0]["ability"]["name"])
    print("Growth Rate: ", poke_info["growth_rate"]["name"])
    if poke_info["form_descriptions"] == []:
        print("Forms: NA")
    else:
        print(poke_info["form_descriptions"])


sprite_url = ability_info["sprites"]["front_default"]
print("About: ", poke_info["flavor_text_entries"][0]["flavor_text"])
print("Version: ", poke_info["flavor_text_entries"][0]["version"]["name"])


output = from_url(sprite_url)
output.to_terminal(columns=100, char=" ▁▂▃▄▅▆▇█")
