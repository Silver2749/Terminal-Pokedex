import requests
from ascii_magic import from_url

while True:
    pokemon = input("Enter Pokémon Name (quit to exit): ").lower()

    if pokemon == "quit":
        print("Goodbye!")
        break

    spec_url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon}/"
    abi_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}/"

    response = requests.get(spec_url)
    response2 = requests.get(abi_url)

    if response.status_code != 200 or response2.status_code != 200:
        print("Pokémon not found!")
        continue

    poke_info = response.json()
    ability_info = response2.json()

    print("\nName:", pokemon)
    print("ID:", poke_info["order"])
    print("ID(per gen):", poke_info["pokedex_numbers"][0]["entry_number"])
    print("Gen:", poke_info["generation"]["name"])
    print("Height:", ability_info["height"])
    print("Weight:", ability_info["weight"])
    print("Ability:", ability_info["abilities"][0]["ability"]["name"])
    print("Growth Rate:", poke_info["growth_rate"]["name"])

    if not poke_info["form_descriptions"]:
        print("Forms: NA")
    else:
        print("Forms:", poke_info["form_descriptions"][0]["description"])

    #japanese fix
    description = "No description available."
    version = "Unknown"

    for entry in poke_info["flavor_text_entries"]:
        if entry["language"]["name"] == "en":
            description = entry["flavor_text"].replace("\n", " ").replace("\f", " ")
            version = entry["version"]["name"]
            break

    print("About:", description)
    print("Version:", version)

    sprite_url = ability_info["sprites"]["front_default"]

    if sprite_url:
        output = from_url(sprite_url)
        output.to_terminal(columns=100, char=" ▁▂▃▄▅▆▇█")

    print("\n" + "=" * 50 + "\n")
