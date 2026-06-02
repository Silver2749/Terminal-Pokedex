# Pokédex CLI

A terminal-based Pokédex built with Python that fetches Pokémon data from PokéAPI and renders Pokémon sprites as colored ASCII art directly in your terminal.

## Features

- Search Pokémon by name
- Display Pokémon sprites as ASCII art
- View Pokédex descriptions
- Show growth rates, abilities, height, and weight
- Display generation information
- Automatically fetch data from PokéAPI

## Examples

### Metagross

<img width="660" height="928" alt="Screenshot 2026-06-03 003844" src="https://github.com/user-attachments/assets/196f93ef-a9ac-4c8d-bda5-dc5301fa4862" />

### Goodra

<img width="1091" height="946" alt="Screenshot 2026-06-03 003239" src="https://github.com/user-attachments/assets/fb6d1f2b-432c-45dd-92ae-915ded300c9b" />

### Palkia

<img width="700" height="962" alt="Screenshot 2026-06-03 003102" src="https://github.com/user-attachments/assets/82d2fe8e-b1cd-4f13-9e51-1ea00ae9948f" />

## Requirements

- Python 3.10+
- Internet connection

## Installation

```bash
git clone <your-repository-url>
cd <repository-name>
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python poke.py
```

Enter a Pokémon name:

```text
metagross
```

Example output:

```text
Name: Metagross
ID: 406
Generation: generation-iii
Ability: clear-body
Growth Rate: slow
...
```


## Data Source

This project uses PokéAPI:

https://pokeapi.co

## Dependencies

- requests
- Pillow
- ascii_magic

