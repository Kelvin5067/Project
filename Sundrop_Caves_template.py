# Name: Kelvin Teo
# Class: IM02
# Student ID: S10275067

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

# To Save the current player stats and progress to the savegame.json file
def save_game(player, fog, show_msg=True):
    try:
        with open("savegame.json", "w") as f:
            json.dump({'player': player, 'fog': fog}, f)
        if show_msg:
            print("Game saved.")
    except Exception as e:
        print(f"Failed to save game: {e}")

