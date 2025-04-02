import random

# Game heroes
ACTIVE_HERO = "Aidan"

heroes = {
    "Aidan": {"health": 100, "magic": 100, "shards": 0},
    "Lira": {"health": 80, "magic": 120, "shards": 0},
    "Regan": {"health": 90, "magic": 110, "shards": 0},
}

hero_list = list(heroes.keys())

# Dictionary to track completed locations
completed_locations = {hero: set() for hero in heroes}

resources = {
    "crystals": 10,
    "artifacts": [],
    "potions": 3,
    "cards": [],
    "gold": 50,
}

# Number of attempts remaining
remaining_moves = 6

# Game functions
def print_status():
    print("\n--- Current Status ---")
    print(f"Attempts remaining: {remaining_moves}")
    for hero, stats in heroes.items():
        print(f"{hero}: Health - {stats['health']}, Magic - {stats['magic']}, Shards - {stats['shards']}")
    print(f"Resources: {resources}")

def choose_path(hero_name):
    print(f"\n{hero_name}, choose your path:")
    print("1. Ancient Forest")
    print("2. Abandoned City")
    print("3. Mountain Peaks")
    while True:
        choice = input("> ")
        if choice in ["1", "2", "3"]:
            return choice
        print("Invalid choice. Enter 1, 2 or 3")

def test_wisdom():
    print("\nAncient guardians pose a riddle:")
    print("What has cities, mountains and rivers, but no houses, trees or water?")
    answer = input("Your answer: ").lower()
    if answer == "map":
        print("Correct! You receive a shard.")
        return True
    print("Wrong! The guardian attacks!")
    heroes[ACTIVE_HERO]["health"] -= 20
    return False

def test_tragedy():
    print('\nVolcanic eruption! Your actions:')
    print('1. Run away')
    print('2. Use magic')
    print('3. Freeze in fear')
    choice = input("> ")
    
    if choice == "1":
        heroes[ACTIVE_HERO]["health"] -= 30
        print('Escaped but got injured. Receive a shard.')
        return True
    elif choice == "2":
        if heroes[ACTIVE_HERO]["magic"] >= 40:
            heroes[ACTIVE_HERO]["magic"] -= 40
            print('Created a magic shield! Receive a shard.')
            return True
        print('Not enough magic! Took damage.')
        heroes[ACTIVE_HERO]["health"] -= 50
        return False
    elif choice == "3":
        print('Perished in lava...')
        heroes[ACTIVE_HERO]["health"] = 0
        return False
    print("Invalid choice!")
    return False

def test_forest_fairy():
    print('\nThe fairy asks you to solve 3 limits:')
    correct = 0
    
    if int(input('lim((1 - cosx)/x) as x→0: ')) == 0:
        correct += 1
    if int(input('lim((arcsinx)/x) as x→0: ')) == 1:
        correct += 1
    if int(input('lim((ln(1 + x))/x) as x→0: ')) == 1:
        correct += 1
    
    if correct == 3:
        print('All correct! Receive a shard!')
        return True
    
    print(f'Correct answers: {correct}/3. The fairy is disappointed...')
    return False

def trade_with_nomads():
    print("\nYou encountered nomads. Your actions:")
    print("1. Buy a potion (10 gold)")
    print("2. Get information (5 gold)")
    print("3. Leave")

    choice = input("> ")
    
    if heroes[ACTIVE_HERO]["health"] <= 0:
        print(f"{ACTIVE_HERO} can't trade - character is dead!")
        return
    
    if choice == "1" and resources["gold"] >= 10:
        resources["potions"] += 1
        resources["gold"] -= 10
        print("Bought a potion.")
    elif choice == "2" and resources["gold"] >= 5:
        resources["gold"] -= 5
        print("Nomads gave you advice.")
    else:
        print("Left.")

def combat(enemy_name, enemy_health):
    print(f"\nYou were attacked by {enemy_name} ({enemy_health} HP)!")
    
    while heroes[ACTIVE_HERO]["health"] > 0 and enemy_health > 0:
        print(f"\n{ACTIVE_HERO}: Health {heroes[ACTIVE_HERO]['health']}")
        print(f"{enemy_name}: Health {enemy_health}")
        print("1. Attack")
        print("2. Use potion (+20 HP)")

        action = input("> ")
        
        if action == "1":
            damage = random.randint(10, 20)
            enemy_health -= damage
            print(f"Dealt {damage} damage!")
        elif action == "2" and resources["potions"] > 0:
            heroes[ACTIVE_HERO]["health"] += 20
            resources["potions"] -= 1
            print("Health restored!")
        else:
            print("Invalid choice or no potions left.")

        if enemy_health > 0:
            damage = random.randint(5, 15)
            heroes[ACTIVE_HERO]["health"] -= damage
            print(f"{enemy_name} dealt {damage} damage!")

    if heroes[ACTIVE_HERO]["health"] > 0:
        print(f"Defeated {enemy_name}!")
        return True
    
    print("Defeated...")
    return False

def random_event():
    events = [
        ("Magic storm", lambda: [print("Lost 5 gold!"), resources.update({"gold": max(0, resources["gold"] - 5)})]),
        ("Found treasure", lambda: [print("+10 gold!"), resources.update({"gold": resources["gold"] + 10})]),
        ("Goblin attack", lambda: combat("Goblin", 50)),
        ("Nomad encounter", trade_with_nomads)
    ]
    
    if heroes[ACTIVE_HERO]["health"] <= 0:
        print(f"{ACTIVE_HERO} can't participate in events - character is dead!")
        return
    
    event = random.choice(events)
    print(f"\nEvent: {event[0]}")
    event[1]()

def main_game_loop():
    print("=== Game 'Heart of Aether' ===")
    print("Collect 3 shards to save the world!")
    
    global ACTIVE_HERO, remaining_moves
    
    while remaining_moves > 0:
        # Check win conditions
        if any(hero["shards"] >= 3 for hero in heroes.values()):
            winner = [name for name, stats in heroes.items() if stats["shards"] >= 3][0]
            print("\n=== Game Over ===")
            print(f"VICTORY! {winner} collected 3 shards!")
            return
        
        # Check if any heroes are alive
        if all(hero["health"] <= 0 for hero in heroes.values()):
            print("\n=== Game Over ===")
            print("Defeat... All heroes have perished.")
            return
        
        print_status()
        
        for hero_name in hero_list:
            ACTIVE_HERO = hero_name
            
            if heroes[ACTIVE_HERO]["health"] <= 0:
                print(f"\n{ACTIVE_HERO} can't act!")
                continue
                
            print(f"\n--- {ACTIVE_HERO}'s turn ---")
            
            # Hero chooses their path
            path = choose_path(ACTIVE_HERO)
            
            # Check if hero already completed this location and got a shard
            if path in completed_locations[ACTIVE_HERO]:
                print(f"{ACTIVE_HERO} already completed this trial and received a shard. Skipping.")
                continue
                
            if path == "1":
                if test_forest_fairy():
                    heroes[ACTIVE_HERO]["shards"] += 1
                    completed_locations[ACTIVE_HERO].add(path)
            elif path == "2":
                if test_wisdom():
                    heroes[ACTIVE_HERO]["shards"] += 1
                    completed_locations[ACTIVE_HERO].add(path)
            elif path == "3":
                if test_tragedy():
                    heroes[ACTIVE_HERO]["shards"] += 1
                    completed_locations[ACTIVE_HERO].add(path)
            
            # Check for victory after each action
            if heroes[ACTIVE_HERO]["shards"] >= 3:
                print("\n=== Game Over ===")
                print(f"VICTORY! {ACTIVE_HERO} collected 3 shards!")
                return
            
            random_event()
        
        remaining_moves -= 1
        print("\n=== End of round ===")

    print("\n=== Game Over ===")
    print("Defeat... Time's up.")

# Start the game
if __name__ == "__main__":
    main_game_loop()
