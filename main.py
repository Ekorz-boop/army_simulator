import random


class Soldier:
    def __init__(self, name, health, rank, training, morale):
        self.name = name
        self.health = health
        self.rank = rank
        self.training = training
        self.morale = morale
        self.fatigue = 0
        self.disease = 0

    def effectiveness(self):
        return self.training * self.morale * (1 - self.fatigue) * (1 - self.disease)

    def __str__(self):
        return f"{self.name}, {self.rank}, Health: {self.health}, Effectiveness: {self.effectiveness()}"


class Officer(Soldier):
    def __init__(self, name, health, rank, training, morale, leadership, skills=None):
        super().__init__(name, health, rank, training, morale)
        self.leadership = leadership
        self.subordinates = []
        self.skills = skills if skills else {}

    def add_subordinate(self, soldier):
        self.subordinates.append(soldier)

    def __str__(self):
        subordinates_str = ", ".join(soldier.name for soldier in self.subordinates)
        return f"{super().__str__()}, Leadership: {self.leadership}, Skills: {self.skills}, Subordinates: [{subordinates_str}]"


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


def generate_random_soldier(is_officer=False):
    name = generate_random_name()
    health = random.randint(50, 100)
    rank_probabilities = [0.8, 0.15, 0.03, 0.015, 0.005]
    rank = random.choices(["Private", "Sergeant", "Lieutenant", "Captain", "Major"], rank_probabilities)[0]
    training = random.uniform(0.5, 1)
    morale = random.uniform(0.5, 1)

    if is_officer:
        leadership = random.uniform(0.5, 1)
        skills = {"tactics": random.uniform(0, 1), "strategy": random.uniform(0, 1), "logistics": random.uniform(0, 1)}
        return Officer(name, health, rank, training, morale, leadership, skills)
    else:
        return Soldier(name, health, rank, training, morale)


def main():
    my_army = Army()

    # Create custom higher-ranking officers
    custom_officers = [
        Officer("George Washington", 100, "General", 0.9, 0.95, 0.9, {"tactics": 0.85, "strategy": 0.9, "logistics": 0.8}),
        Officer("Horatio Gates", 100, "Major General", 0.8, 0.9, 0.85, {"tactics": 0.75, "strategy": 0.8, "logistics": 0.7})
    ]

    for officer in custom_officers:
        my_army.add_soldier(officer)

    for _ in range(100):
        soldier = generate_random_soldier()
        my_army.add_soldier(soldier)
        # Assign soldiers to officers based on their rank
        if soldier.rank == "Private":
            random.choice(custom_officers).add_subordinate(soldier)
        elif soldier.rank == "Sergeant":
            custom_officers[1].add_subordinate(soldier)
        elif soldier.rank == "Lieutenant":
            custom_officers[0].add_subordinate(soldier)


if __name__ == "__main__":
    main()
