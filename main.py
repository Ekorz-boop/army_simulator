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
            if random.random() < 0.3:  # Increased probability
                soldier.health -= random.randint(1, 10)

    def simulate_travel(self, distance):
        for soldier in self.soldiers:
            if random.random() < 0.1:  # Increased probability for fatigue
                soldier.health -= random.randint(1, 5)
            if random.random() < 0.05:  # Increased probability for injury
                soldier.health -= random.randint(5, 10)
            if random.random() < 0.03:  # Desertion instead of missing soldiers
                self.soldiers.remove(soldier)

        self.soldiers = [soldier for soldier in self.soldiers if soldier.health > 0]
        self.simulate_disease()

    def __str__(self):
        return "\n".join(str(soldier) for soldier in self.soldiers)


def generate_random_name():
    first_names = ["John", "Michael", "David", "James", "Robert"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"


def generate_random_soldier():
    name = generate_random_name()
    health = random.randint(50, 100)
    rank_probabilities = [0.8, 0.15, 0.03, 0.015, 0.005]
    rank = random.choices(["Private", "Sergeant", "Lieutenant", "Captain", "Major"], rank_probabilities)[0]
    return Soldier(name, health, rank)


def main():
    my_army = Army()

    for _ in range(100):
        my_army.add_soldier(generate_random_soldier())

    


if __name__ == "__main__":
    main()
