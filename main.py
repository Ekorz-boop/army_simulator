import random

class Soldier:
    def __init__(self, name, health, rank):
        self.name = name
        self.health = health
        self.rank = rank

    def __str__(self):
        return f"{self.name}, {self.rank}, Health: {self.health}"

class Army:
    def __init__(self):
        self.soldiers = []

    def add_soldier(self, soldier):
        self.soldiers.append(soldier)

    def simulate_disease(self):
        for soldier in self.soldiers:
            if random.random() < 0.1:
                soldier.health -= random.randint(1, 10)

    def __str__(self):
        return "\n".join(str(soldier) for soldier in self.soldiers)

def generate_random_name():
    first_names = ["John", "Michael", "David", "James", "Robert"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_random_soldier():
    name = generate_random_name()
    health = random.randint(50, 100)
    rank = random.choice(["Private", "Sergeant", "Lieutenant", "Captain", "Major"])
    return Soldier(name, health, rank)

def main():
    my_army = Army()

    for _ in range(100):
        my_army.add_soldier(generate_random_soldier())

    print("Army before disease:")
    print(my_army)

    my_army.simulate_disease()

    print("\nArmy after disease:")
    print(my_army)

if __name__ == "__main__":
    main()
