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
    types = [t["type"]["name"].title() for t in ability_info["types"]]

    print("=" * 50)
    print(f"{'Name':<15}: {pokemon.title()}")
    print(f"{'National Dex':<15}: {poke_info['order']}")
    print(f"{'Generation':<15}: {poke_info['generation']['name']}")
    print(f"{'Height':<15}: {ability_info['height']}")
    print(f"{'Weight':<15}: {ability_info['weight']}")
    print(f"{'Type':<15}: {' / '.join(types)}")
    print(f"{'Ability':<15}: {ability_info['abilities'][0]['ability']['name']}")
    print(f"{'Growth Rate':<15}: {poke_info['growth_rate']['name']}")
    print("\nStats")
    print("-" * 50)

    bst = 0

    for stat in ability_info["stats"]:
        name = stat["stat"]["name"].replace("-", " ").title()
        value = stat["base_stat"]

        bst += value

        bar = "█" * (value // 10)

        print(f"{name:<18} {bar:<15} {value}")

    print("-" * 50)
    print(f"{'BST':<18} {bst}")
    print("=" * 50)

    if not poke_info["form_descriptions"]:
        print("Forms: NA")
    else:
        print("Forms:", poke_info["form_descriptions"][0]["description"])

    # japanese fix
    description = "No description available."
    version = "Unknown"

    for entry in poke_info["flavor_text_entries"]:
        if entry["language"]["name"] == "en":
            description = entry["flavor_text"].replace("\n", " ").replace("\f", " ")
            version = entry["version"]["name"]
            break

    print("About:", description)
    print("Version:", version)
    print("=" * 50)
    print("AUTHORED BY SIlver")

    sprite_url = ability_info["sprites"]["front_default"]

    if sprite_url:
        output = from_url(sprite_url)
        output.to_terminal(columns=100, char=" ▁▂▃▄▅▆▇█")

    print("\n" + "=" * 50 + "\n")
