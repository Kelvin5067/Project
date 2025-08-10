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


# To Display the entire mine map with the player’s position , portal location , unexplored areas, and visible tiles from game_map
def draw_map(game_map, fog, player):
    print("+------------------------------+")
    for y in range(MAP_HEIGHT):
        row = '|'
        for x in range(MAP_WIDTH):
            if (x, y) == (player['x'], player['y']):
                row += 'M '
            elif 'portal' in player and (x, y) == tuple(player['portal']):
                row += 'P '
            elif fog[y][x] == '?':
                row += '? '
            else:
                row += game_map[y][x] + ' '
        row += '|'
        print(row)
    print("+------------------------------+")

# To display the 3×3 local view around the player,  but it only shows the nearby tiles instead of the whole map
def draw_view(game_map, player):
    print("+---+")
    for dy in range(-1, 2):
        row = '|'
        for dx in range(-1, 2):
            nx = player['x'] + dx
            ny = player['y'] + dy
            if 0 <= ny < MAP_HEIGHT and 0 <= nx < MAP_WIDTH:
                if dx == 0 and dy == 0:
                    row += 'M'
                else:
                    row += game_map[ny][nx]
            else:
                row += '#'
        row += '|'
        print(row)
    print("+---+")

#To load the map, the fog of war, and gives the player all their default starting stats like position, ores, GP, turns, and pickaxe level when they start a new game
def initialize_game(game_map, fog, player):
    load_map("level1.txt", game_map)
    fog.clear()
    for row in range(MAP_HEIGHT):
        fog_row = ['?' for _ in range(MAP_WIDTH)]
        fog.append(fog_row)
    player['name'] = input("Greetings, miner! What is your name? ").strip()
    print(f"Pleased to meet you, {player['name']}. Welcome to Sundrop Town!")
    player.update({
        'x': 0, 'y': 0,
        'copper': 0, 'silver': 0, 'gold': 0,
        'GP': 0,
        'day': 1,
        'steps': 0,
        'turns': TURNS_PER_DAY,
        'max_load': 10,
        'pickaxe': 1,
        'portal': [0, 0]
    })
    clear_fog(fog, player)

# To display player info on Player Name,Position Pickaxe Level Number of Gold, Silver and Copper the load the gp and the number of steps taken
def show_information(player):
    print("----- Player Information -----")
    print(f"Name: {player['name']}")
    print(f"Current position: ({player['x']}, {player['y']})")
    pickaxe_name = {1: '1 (copper)', 2: '2 (silver)', 3: '3 (gold)'}[player['pickaxe']]
    print(f"Pickaxe level: {pickaxe_name}")
    print(f"Gold: {player['gold']}")
    print(f"Silver: {player['silver']}")
    print(f"Copper: {player['copper']}")
    load = player['gold'] + player['silver'] + player['copper']
    print(f"Load: {load} / {player['max_load']}")
    print(f"GP: {player['GP']}")
    print(f"Steps taken: {player['steps']}")
    print("------------------------------")


# To display the player shop to upgrade pickaxe, backpack or to leave shop
def buy_stuff(player):
    while True:
        print("----------------------- Shop Menu -------------------------")
        if player['pickaxe'] == 1:
            print(f"(P)ickaxe upgrade to Level 2 to mine silver ore for 50 GP")
        elif player['pickaxe'] == 2:
            print(f"(P)ickaxe upgrade to Level 3 to mine gold ore for 150 GP")
        print(f"(B)ackpack upgrade to carry {player['max_load']+2} items for {player['max_load']*2} GP")
        print("(L)eave shop")
        print("-----------------------------------------------------------")
        print(f"GP: {player['GP']}")
        choice = input("Your choice? ").strip().upper()
        if choice == 'B':
            cost = player['max_load'] * 2
            if player['GP'] >= cost:
                player['GP'] -= cost
                player['max_load'] += 2
                print(f"Congratulations! You can now carry {player['max_load']} items!")
            else:
                print("Not enough GP!")
        elif choice == 'P':
            if player['pickaxe'] == 1 and player['GP'] >= 50:
                player['GP'] -= 50
                player['pickaxe'] = 2
                print("Pickaxe upgraded to Level 2! You can now mine silver ore.")
            elif player['pickaxe'] == 2 and player['GP'] >= 150:
                player['GP'] -= 150
                player['pickaxe'] = 3
                print("Pickaxe upgraded to Level 3! You can now mine gold ore.")
            else:
                print("Not enough GP or already at maximum pickaxe level!")
        elif choice == 'L':
            break

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

