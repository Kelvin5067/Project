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

#This Function is to Handle a single move which will check the map boundary, ans will block ores that players wont be able to mine with their current axe level or when bag is full,  and updates position steps and turns, and mines ore if possible, and reveals fog around the new spot.
def mine_tile(game_map, player, fog, dx, dy):
    new_x = player['x'] + dx
    new_y = player['y'] + dy
    if not (0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT):
        print("You can't move outside the map.")
    else:
        symbol = game_map[new_y][new_x]
        ore_req = {'C': 1, 'S': 2, 'G': 3}
        load = player['copper'] + player['silver'] + player['gold']
        if symbol in 'CSG' and player['pickaxe'] < ore_req[symbol]:
            print("Your pickaxe is not strong enough to mine this ore.")
            return
        if load >= player['max_load'] and symbol in 'CSG':
            print("You can't carry any more, so you can't go that way.")
        else:
            player['x'], player['y'] = new_x, new_y
            player['steps'] += 1
            player['turns'] -= 1
            if symbol in 'CSG':
                ore_type = mineral_names[symbol]
                max_pick = {'copper': 5, 'silver': 3, 'gold': 2}[ore_type]
                qty = randint(1, max_pick)
                free_space = player['max_load'] - load
                if qty > free_space:
                    print(f"You mined {qty} piece(s) of {ore_type}.")
                    print(f"...but you can only carry {free_space} more piece(s)!")
                    qty = free_space
                else:
                    print(f"You mined {qty} piece(s) of {ore_type}.")
                player[ore_type] += qty
            clear_fog(fog, player)

#This function is to let the player use the portal stone to sell all carried ores at random prices, adds the GP earned, saves the current location as the portal spot, teleports the player back to (0,0), resets turns, advances the day, clears the fog around town, and auto-saves the game
def return_to_town(player):
    print("\nYou place your portal stone here and zap back to town.")
    for ore in ['copper', 'silver', 'gold']:
        qty = player[ore]
        if qty > 0:
            min_price, max_price = prices[ore]
            rate = randint(min_price, max_price)
            gp = qty * rate
            player['GP'] += gp
            print(f"You sell {qty} {ore} ore for {gp} GP.")
            player[ore] = 0
    print(f"You now have {player['GP']} GP!")
    player['portal'] = [player['x'], player['y']]
    player['x'], player['y'] = 0, 0
    player['turns'] = TURNS_PER_DAY
    player['day'] += 1
    clear_fog(fog, player)
    save_game(player, fog, show_msg=False)

#Menu
def show_main_menu():
    print()
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
    print("(Q)uit")
    print("------------------")

def show_town_menu():
    print(f"\nDAY {player['day']}")
    print("----- Sundrop Town -----")
    print("(B)uy stuff")
    print("(I)nformation")
    print("See Mine (M)ap")
    print("(E)nter mine")
    print("Sa(V)e game")
    print("(Q)uit to main menu")
    print("------------------------")

def show_mine_menu():
    print(f"\nDAY {player['day']}")
    draw_view(game_map, player)
    print(f"Turns left: {player['turns']}    Load: {player['copper'] + player['silver'] + player['gold']} / {player['max_load']}    Steps: {player['steps']}")
    print("(WASD) to move")
    print("(M)ap, (I)nformation, (P)ortal, (Q)uit to main menu")


def main():
    global player, fog
    #Main Menu Use N to Start a New Game, L to load saved game from save game json file and Q to Quit Game
    while True:
        show_main_menu()
        choice = input("Your choice? ").strip().upper()
        if choice == 'N':
            initialize_game(game_map, fog, player)
        elif choice == 'L':
            loaded_player, loaded_fog = load_game()
            if loaded_player:
                player = loaded_player
                fog = loaded_fog
                load_map("level1.txt", game_map)
                clear_fog(fog, player)
            else:
                continue
        elif choice == 'Q':
            print("Thanks for playing Sundrop Caves!")
            break
        else:
            continue
        
        #Town Menu B = Buy items, I = View stats, M = Show map, E = Enter mine from portal
        while True:
            show_town_menu()
            town_choice = input("Your choice? ").strip().upper()
            if town_choice == 'B':
                buy_stuff(player)
            elif town_choice == 'I':
                show_information(player)
            elif town_choice == 'M':
                draw_map(game_map, fog, player)
            elif town_choice == 'E':
                player['x'], player['y'] = player['portal']

                # Mine Menu: WASD = Move, M = Show map, I = View stats, P = Return to town, Q = Quit, plus exhaustion and win checks
                while True:
                    show_mine_menu()
                    action = input("Action? ").strip().upper()
                    if action == 'W':
                        mine_tile(game_map, player, fog, 0, -1)
                    elif action == 'A':
                        mine_tile(game_map, player, fog, -1, 0)
                    elif action == 'S':
                        mine_tile(game_map, player, fog, 0, 1)
                    elif action == 'D':
                        mine_tile(game_map, player, fog, 1, 0)
                    elif action == 'M':
                        draw_map(game_map, fog, player)
                    elif action == 'I':
                        show_information(player)
                    elif action == 'P':
                        return_to_town(player)
                        break
                    elif action == 'Q':
                        return
                    if player['turns'] <= 0:
                        print("You are exhausted.")
                        return_to_town(player)
                        break
                    if player['GP'] >= WIN_GP:
                        print(f"\nWoo-hoo! Well done, {player['name']}, you have {player['GP']} GP!")
                        print("You now have enough to retire and play video games every day.")
                        print(f"And it only took you {player['day']} days and {player['steps']} steps! You win!")
                        return
            elif town_choice == 'V':
                save_game(player, fog, show_msg=True)
            elif town_choice == 'Q':
                break


