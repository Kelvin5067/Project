# Name: Kelvin Teo
# Class: IM02
# Student ID: S10275067

# To Set up the game's global variables, constants, and the data structure for player stats, map data, ore types, and selling prices

from random import randint
import json

player = {}
game_map = []
fog = []

MAP_WIDTH = 0
MAP_HEIGHT = 0

TURNS_PER_DAY = 20
WIN_GP = 500

minerals = ['copper', 'silver', 'gold']
mineral_names = {'C': 'copper', 'S': 'silver', 'G': 'gold'}

prices = {
    'copper': (1, 3),
    'silver': (5, 8),
    'gold': (10, 18)
}

# To Save the current player stats and progress to the savegame.json file
def save_game(player, fog, show_msg=True):
    try:
        with open("savegame.json", "w") as f:
            json.dump({'player': player, 'fog': fog}, f)
        if show_msg:
            print("Game saved.")
    except Exception as e:
        print(f"Failed to save game: {e}")

# To Load player stats and progress from 'savegame.json' and returns them for game continuation
def load_game():
    try:
        with open("savegame.json", "r") as f:
            data = json.load(f)
        print("Game loaded successfully!")
        return data['player'], data['fog']
    except Exception as e:
        print(f"Failed to load game: {e}")
        return None, None

#To Load the mine layout from a file into a 2D list and set the map's width and height
def load_map(filename, map_struct):
    global MAP_WIDTH, MAP_HEIGHT
    map_struct.clear()
    with open(filename, 'r') as map_file:
        for line in map_file:
            row = list(line.strip())
            if row:
                map_struct.append(row)
    MAP_HEIGHT = len(map_struct)
    MAP_WIDTH = len(map_struct[0]) if MAP_HEIGHT > 0 else 0

# To Load the surrounding 3×3 area around the player's current position
def clear_fog(fog, player):
    x, y = player['x'], player['y']
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            nx, ny = x + dx, y + dy
            if 0 <= ny < MAP_HEIGHT and 0 <= nx < MAP_WIDTH:
                fog[ny][nx] = ' '



#Menu
def show_main_menu():
    print()
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
    print("(Q)uit")
    print("------------------")

def show_town_menu():
    print(f"Day")
    print("----- Sundrop Town -----")
    print("(B)uy stuff")
    print("(I)nformation")
    print("See Mine (M)ap")
    print("(E)nter mine")
    print("Sa(V)e game")
    print("(Q)uit to main menu")
    print("------------------------")

