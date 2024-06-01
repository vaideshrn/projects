import random
import time
import sys

class Character:
    def __init__(self, name, max_hp, attack, defense, level=1, exp=0):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack = attack
        self.defense = defense
        self.level = level
        self.exp = exp

    def attack_enemy(self, enemy):
        damage = max(0, self.attack - enemy.defense)
        enemy.hp -= damage
        print(f"{self.name} attacks {enemy.name} and deals {damage} damage.")
        if enemy.hp <= 0:
            print(f"{enemy.name} has been defeated!")
            self.exp += enemy.level * 10
            if self.exp >= self.level * 100:
                self.level_up()
            return True
        return False

    def level_up(self):
        self.level += 1
        self.max_hp += 10
        self.hp = self.max_hp
        self.attack += 5
        self.defense += 2
        print(f"{self.name} leveled up to level {self.level}!")
        print(f"Max HP: {self.max_hp}, Attack: {self.attack}, Defense: {self.defense}")

    def __str__(self):
        return f"{self.name} (Level {self.level}) - HP: {self.hp}/{self.max_hp}, Attack: {self.attack}, Defense: {self.defense}, EXP: {self.exp}/{self.level * 100}"

class Enemy(Character):
    def __init__(self, name, max_hp, attack, defense, level):
        super().__init__(name, max_hp, attack, defense, level)

class Location:
    def __init__(self, name, enemies):
        self.name = name
        self.enemies = enemies

    def explore(self, player):
        print(f"You are exploring {self.name}...")
        time.sleep(1)
        enemy = random.choice(self.enemies)
        print(f"A wild {enemy.name} (Level {enemy.level}) appears!")
        while player.hp > 0 and enemy.hp > 0:
            print(player)
            print(enemy)
            action = input("What will you do? (1. Attack, 2. Run) ")
            if action == "1":
                if player.attack_enemy(enemy):
                    break
                if enemy.attack_enemy(player):
                    break
            elif action == "2":
                print("You run away from the battle...")
                break
            else:
                print("Invalid action. Try again.")
        if player.hp <= 0:
            print("You were defeated...")
            sys.exit()

def create_player():
    name = input("Enter your name: ")
    print("Choose your class:")
    print("1. Warrior (High attack, low defense)")
    print("2. Knight (Balanced attack and defense)")
    print("3. Mage (Low attack, high defense)")
    choice = input("Enter your choice: ")
    if choice == "1":
        return Character(name, 100, 20, 10)
    elif choice == "2":
        return Character(name, 120, 15, 15)
    elif choice == "3":
        return Character(name, 80, 10, 20)
    else:
        print("Invalid choice. Defaulting to Warrior.")
        return Character(name, 100, 20, 10)

def main():
    print("Welcome to Text RPG!")
    player = create_player()
    print(f"Welcome, {player.name}!")
    locations = [
        Location("Forest", [Enemy("Goblin", 50, 10, 5, 1), Enemy("Wolf", 40, 15, 3, 2)]),
        Location("Cave", [Enemy("Bat", 30, 20, 2, 1), Enemy("Spider", 40, 15, 5, 2)]),
        Location("Castle", [Enemy("Guard", 100, 15, 10, 3), Enemy("Knight", 150, 20, 15, 4)])
    ]
    while True:
        print("\nLocations:")
        for i, location in enumerate(locations, start=1):
            print(f"{i}. {location.name}")
        choice = input("Choose a location to explore (1-3): ")
        if choice.isdigit() and 1 <= int(choice) <= len(locations):
            location = locations[int(choice) - 1]
            location.explore(player)
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
