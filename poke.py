import io
import os
import sys
import time
import shutil
import requests
from PIL import Image, ImageEnhance, ImageSequence

ASCII_CHARS = " ▁▂▃▄▅▆▇█"
RESET = "\033[0m"

try:
    import colorama
    colorama.init()
except Exception:
    colorama = None


def get_terminal_columns(default=80):
    try:
        width = shutil.get_terminal_size().columns
        return min(max(40, width), 100)
    except OSError:
        return default


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def download_image(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return Image.open(io.BytesIO(response.content))


def supports_color():
    if not sys.stdout.isatty():
        return False
    if os.name == "nt" and colorama is None:
        return False
    return True


def image_to_ascii(image, columns, colored=False):
    width, height = image.size
    aspect_ratio = height / width
    rows = max(1, int(columns * aspect_ratio * 0.55))
    image = image.resize((columns, rows))

    if colored and supports_color():
        image = image.convert("RGBA")
        pixels = list(image.getdata())
        lines = []
        current_line = ""
        current_color = None

        for index, pixel in enumerate(pixels):
            r, g, b, a = pixel
            if a < 255:
                alpha = a / 255.0
                r = int(r * alpha + 255 * (1 - alpha))
                g = int(g * alpha + 255 * (1 - alpha))
                b = int(b * alpha + 255 * (1 - alpha))

            brightness = int(0.299 * r + 0.587 * g + 0.114 * b)
            char = ASCII_CHARS[brightness * len(ASCII_CHARS) // 256]
            color_code = f"\033[38;2;{r};{g};{b}m"

            if color_code != current_color:
                if current_color is not None:
                    current_line += RESET
                current_line += color_code
                current_color = color_code

            current_line += char
            if (index + 1) % columns == 0:
                if current_color is not None:
                    current_line += RESET
                    current_color = None
                lines.append(current_line)
                current_line = ""

        return "\n".join(lines)

    image = image.convert("L")
    pixels = list(image.getdata())
    scale = len(ASCII_CHARS)
    ascii_pixels = [ASCII_CHARS[pixel * scale // 256] for pixel in pixels]
    lines = ["".join(ascii_pixels[i : i + columns]) for i in range(0, len(ascii_pixels), columns)]
    return "\n".join(lines)


def make_ascii_frames_from_image(image, columns):
    frames = []
    if getattr(image, "is_animated", False):
        for frame in ImageSequence.Iterator(image):
            frames.append(image_to_ascii(frame.convert("RGBA"), columns, colored=True))
    else:
        frames.append(image_to_ascii(image.convert("RGBA"), columns, colored=True))
    return frames


def find_animated_sprite_url(sprites):
    try:
        return sprites["versions"]["generation-v"]["black-white"]["animated"]["front_default"]
    except Exception:
        return None


def get_static_sprite_urls(sprites):
    keys = [
        "front_default",
        "back_default",
        "front_shiny",
        "back_shiny",
        "front_female",
        "back_female",
    ]
    urls = []
    for key in keys:
        url = sprites.get(key)
        if url and url not in urls:
            urls.append(url)
    return urls


def get_ascii_animation_frames(sprites, columns):
    animated_url = find_animated_sprite_url(sprites)
    if animated_url:
        try:
            image = download_image(animated_url)
            frames = make_ascii_frames_from_image(image, columns)
            if len(frames) > 1:
                return frames
        except Exception:
            pass

    static_urls = get_static_sprite_urls(sprites)
    frames = []
    for url in static_urls:
        try:
            image = download_image(url)
            frames.append(image_to_ascii(image.convert("RGBA"), columns, colored=True))
        except Exception:
            continue

    if len(frames) > 1:
        return frames

    if static_urls:
        try:
            image = download_image(static_urls[0]).convert("RGBA")
            normal = image_to_ascii(image, columns, colored=True)
            brighter = image_to_ascii(ImageEnhance.Brightness(image.convert("RGB")).enhance(1.4).convert("RGBA"), columns, colored=True)
            return [normal, brighter]
        except Exception:
            return frames

    return frames


def display_ascii_animation(info_lines, frames, delay=0.16, loops=3):
    if not frames:
        print("No image available for this Pokémon.")
        return

    for loop in range(loops):
        for index, frame in enumerate(frames):
            clear_terminal()
            print("\n".join(info_lines))
            print(frame)
            if loop == loops - 1 and index == len(frames) - 1:
                return
            time.sleep(delay)


while True:
    pokemon = input("Enter Pokémon Name (quit to exit): ").strip().lower()

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

    description = "No description available."
    version = "Unknown"
    for entry in poke_info["flavor_text_entries"]:
        if entry["language"]["name"] == "en":
            description = entry["flavor_text"].replace("\n", " ").replace("\f", " ")
            version = entry["version"]["name"]
            break

    info_lines = [
        "=" * 50,
        f"{'Name':<15}: {pokemon.title()}",
        f"{'National Dex':<15}: {poke_info['order']}",
        f"{'Generation':<15}: {poke_info['generation']['name']}",
        f"{'Height':<15}: {ability_info['height']}",
        f"{'Weight':<15}: {ability_info['weight']}",
        f"{'Type':<15}: {' / '.join(types)}",
        f"{'Ability':<15}: {ability_info['abilities'][0]['ability']['name']}",
        f"{'Growth Rate':<15}: {poke_info['growth_rate']['name']}",
        "",
        "Stats",
        "-" * 50,
    ]

    bst = 0
    for stat in ability_info["stats"]:
        name = stat["stat"]["name"].replace("-", " ").title()
        value = stat["base_stat"]
        bst += value
        bar = "█" * (value // 10)
        info_lines.append(f"{name:<18} {bar:<15} {value}")

    info_lines.extend([
        "-" * 50,
        f"{'BST':<18} {bst}",
        "=" * 50,
    ])

    if not poke_info["form_descriptions"]:
        info_lines.append("Forms: NA")
    else:
        info_lines.append(f"Forms: {poke_info['form_descriptions'][0]['description']}")

    info_lines.extend([
        f"About: {description}",
        f"Version: {version}",
        "=" * 50,
        "AUTHORED BY SIlver",
    ])

    columns = get_terminal_columns(80)
    frames = get_ascii_animation_frames(ability_info["sprites"], columns)
    display_ascii_animation(info_lines, frames)

    print("\n" + "=" * 50 + "\n")
