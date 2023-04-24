import random
import names
import sys


class Soldier:
    def __init__(self, name, health, training, morale, rank):
        self.name = name
        self.health = health
        self.training = training
        self.morale = morale
        self.rank = rank
        self.fatigue = 0
        self.diseases = []

    def effectiveness(self):
        return self.training * self.morale * (1 - self.fatigue) * (1 - self.disease)

    def __str__(self):
        return f"{self.rank} {self.name} ({self.unit_type.capitalize()})"


class Infantry(Soldier):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.unit_type = "infantry"


class Cavalry(Soldier):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.unit_type = "cavalry"


class Artillery(Soldier):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.unit_type = "artillery"


class Company:
    counter = 1

    def __init__(self, leader, unit_type):
        self.name = self.generate_name(unit_type)
        self.leader = leader
        self.soldiers = []
        Company.counter += 1

    @classmethod
    def generate_name(cls, unit_type):
        return f"{cls.counter} {str(unit_type).capitalize()} Company"

    def add_soldier(self, soldier):
        self.soldiers.append(soldier)

    def find_soldier(self, name):
        for soldier in self.soldiers:
            if soldier.name == name:
                return soldier
        return None
    
    def is_full(self):
        max_soldiers = 50  # soldiers per company
        return len(self.soldiers) >= max_soldiers
    
    def assign_leader(self, leader):
        if isinstance(leader, Officer) and leader.rank == "lieutenant":
            self.leader = leader
        else:
            raise ValueError("Only lieutenants can be assigned as company leaders.")

    def __str__(self):
        return f"Company: {self.name} (Leader: {self.leader.name})"


class Regiment:
    counter = 1

    def __init__(self, leader, unit_type):
        self.name = self.generate_name(unit_type)
        self.leader = leader
        self.companies = []
        Regiment.counter += 1

    @classmethod
    def generate_name(cls, unit_type):
        return f"{cls.counter} {str(unit_type).capitalize()} Regiment"

    def add_company(self, company):
        self.companies.append(company)

    def find_soldier(self, name):
        for company in self.companies:
            soldier = company.find_soldier(name)
            if soldier:
                return soldier
        return None
    
    def find_company(self, name):
        for company in self.companies:
            if company.name == name:
                return company
        return None
    
    def is_full(self):
        max_companies = 4  # companies per regiment
        return len(self.companies) >= max_companies
    
    def assign_leader(self, leader):
        if isinstance(leader, Officer) and leader.rank == "captain":
            self.leader = leader
        else:
            raise ValueError("Only captains can be assigned as regiment leaders.")

    def __str__(self):
        return f"Regiment: {self.name} (Leader: {self.leader.name})"


class Officer(Soldier):
    def __init__(self, name, health, training, morale, officer_rank, skills=None):
        super().__init__(name, health, training, morale, rank=officer_rank)
        self.subordinates = []
        self.skills = skills or {
            'strategy': 0,
            'tactics': 0,
            'logistics': 0,
            'communication': 0,
            'discipline': 0,
            'inspiration': 0
        }
        
        if officer_rank in ["Major", "General", "Major General"]:
            self.skills.update({
                "diplomacy": random.uniform(0, 1),
                "intelligence": random.uniform(0, 1),
                "recruitment": random.uniform(0, 1),
            })

    def add_subordinate(self, soldier):
        self.subordinates.append(soldier)

    def generate_skills(self):
        for skill in self.skills:
            self.skills[skill] = random.randint(1, 100)

    def __str__(self):
        subordinates_str = ", ".join(soldier.name for soldier in self.subordinates)
        return f"{super().__str__()}, Leadership: {self.leadership}, Skills: {self.skills}, Subordinates: [{subordinates_str}]"


class Army:
    def __init__(self, name):
        self.name = name
        self.soldiers = []
        self.regiments = [] 

    def add_soldier(self, soldier):
        self.soldiers.append(soldier)

    def add_regiment(self, regiment):
        self.regiments.append(regiment)

    def simulate_disease(self):
        for soldier in self.soldiers:
            if random.random() < 0.3:  # Increased probability
                soldier.health -= random.randint(1, 10)

    def simulate_travel(self, distance, terrain, weather, season):
        terrain_factors = {
            "flat": 1,
            "hilly": 1.2,
            "mountainous": 1.5,
        }

        weather_factors = {
            "sunny": 1,
            "rainy": 1.3,
            "snowy": 1.7,
        }

        season_factors = {
            "spring": 1,
            "summer": 1,
            "fall": 1.2,
            "winter": 1.5,
        }

        terrain_factor = terrain_factors.get(terrain, 1)
        weather_factor = weather_factors.get(weather, 1)
        season_factor = season_factors.get(season, 1)
        total_factor = terrain_factor * weather_factor * season_factor

        for soldier in self.soldiers:
            if random.random() < 0.1 * total_factor:  # Increased probability for fatigue
                soldier.health -= random.randint(1, 5)
            if random.random() < 0.05 * total_factor:  # Increased probability for injury
                soldier.health -= random.randint(5, 10)
            if random.random() < 0.03 * total_factor:  # Desertion instead of missing soldiers
                self.soldiers.remove(soldier)

        self.soldiers = [soldier for soldier in self.soldiers if soldier.health > 0]
        self.simulate_disease()

    def find_soldier(self, name):
        for soldier in self.soldiers:
            if soldier.name == name:
                return soldier
        return None

    def find_regiment(self, name):
        for soldier in self.soldiers:
            if isinstance(soldier, Officer) and soldier.leader_of:
                regiment = next((r for r in soldier.leader_of if isinstance(r, Regiment)), None)
                if regiment and regiment.name == name:
                    return regiment
        return None
    
    def remove_casualties(self, casualties):
        for _ in range(casualties):
            if self.soldiers:
                soldier = random.choice(self.soldiers)
                self.soldiers.remove(soldier)

    def __str__(self):
        result = "Army:\n"
        for soldier in self.soldiers:
            if isinstance(soldier, Officer):
                result += f"  {soldier}\n"
                regiment = next((r for r in soldier.leader_of if isinstance(r, Regiment)), None)
                if regiment:
                    result += f"    {regiment}\n"
                    for company in regiment.companies:
                        result += f"      {company}\n"
                        for company_soldier in company.soldiers:
                            result += f"        {company_soldier}\n"
        return result


def generate_random_name():
    first_names = ["John", "Michael", "David", "James", "Robert", "Jonas", "Greg", "Jimmy", "Frank", "Charles", "Bob", "Ken", "Thomas", "Joseph", "Harry", "Henry", "Oliver", "Alexander", "Isaac", "Elias", "Frederick", "Malcolm"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Taylor", "Walker", "Walford", "Turner", "Axton", "Badger", "Beesley", "Adams", "Harris", "Burton", "Baker", "Payne", "Webb", "Foster", "Young", "Hughes"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"


def generate_random_soldier(is_officer=False):
    name = generate_random_name()
    health = random.randint(50, 100)
    rank = "Private"
    training = random.uniform(0.5, 1)
    morale = random.uniform(0.5, 1)

    unit_probabilities = [0.6, 0.3, 0.1]
    unit_type = random.choices(["infantry", "cavalry", "artillery"], unit_probabilities)[0]

    if is_officer:
        leadership = random.uniform(0.5, 1)
        skills = {"tactics": random.uniform(0, 1), "strategy": random.uniform(0, 1), "logistics": random.uniform(0, 1)}
        officer = Officer(name, health, rank, training, morale, leadership, skills)
        officer.unit_type = unit_type
        return officer
    else:
        if unit_type == "infantry":
            return Infantry(name, health, rank, training, morale)
        elif unit_type == "cavalry":
            return Cavalry(name, health, rank, training, morale)
        elif unit_type == "artillery":
            return Artillery(name, health, rank, training, morale)


def generate_army(name, size):
    army = Army(name)
    regiment = None
    company = None

    for i in range(size):
        soldier_rank = random.choices(["private", "corporal", "sergeant", "lieutenant", "captain"],
                                    weights=[0.85, 0.1, 0.03, 0.015, 0.005], k=1)[0]

        name = names.get_full_name()
        health = random.randint(75, 100)
        training = random.randint(50, 100)
        morale = random.randint(50, 100)

        progress = (i + 1) / size * 100
        sys.stdout.write(f'\rGenerating army... {progress:.1f}%')
        sys.stdout.flush()

        if soldier_rank in ["private", "corporal", "sergeant"]:
            soldier = Soldier(name, health, training, morale, rank=soldier_rank)
        else:
            officer = Officer(name, health, training, morale, officer_rank=soldier_rank)
            officer.generate_skills()
            soldier = officer

        if soldier_rank == "captain":
            if regiment is None or regiment.is_full():
                regiment = Regiment(name, len(army.regiments) + 1)
                army.add_regiment(regiment)
            regiment.assign_leader(soldier)

        elif soldier_rank == "lieutenant":
            if company is None or company.is_full():
                company = Company(regiment.name, len(regiment.companies) + 1)
                regiment.add_company(company)
            company.assign_leader(soldier)

        if regiment is None or regiment.is_full():
            regiment = Regiment(army.name, len(army.regiments) + 1)
            army.add_regiment(regiment)

        if company is None or company.is_full():
            company = Company(regiment.name, len(regiment.companies) + 1)
            regiment.add_company(company)

        company.add_soldier(soldier)

    sys.stdout.write('\rGenerating army... Done!   \n')
    sys.stdout.flush()

    return army


def display_army_structure(army):
    print(f"{army.name} Structure:")
    for regiment in army.regiments:
        print(f"  Regiment {regiment.name}:")
        for company in regiment.companies:
            print(f"    Company {company.name}:")
            for soldier in company.soldiers:
                print(f"      Soldier {soldier.name}, Rank: {soldier.rank}")


def combat(army1, army2):
    def inflict_hits(attacking_army, defending_army):
        hits = 0
        for soldier in attacking_army.soldiers:
            if isinstance(soldier, Officer):
                if "strategy" in soldier.skills:
                    hits += soldier.skills["strategy"] * 0.1
            hit_chance = soldier.combat_effectiveness() / 100
            if random.random() < hit_chance:
                hits += 1
        return hits

    def apply_hits(hits, defending_army):
        casualties = 0
        for _ in range(int(hits)):
            soldier = random.choice(defending_army.soldiers)
            damage = random.randint(10, 50)
            soldier.health -= damage
            if soldier.health <= 0:
                defending_army.soldiers.remove(soldier)
                casualties += 1
        return casualties

    def morale_check(army):
        if not army.soldiers:
            return False
        
        total_morale = sum([soldier.morale for soldier in army.soldiers])
        average_morale = total_morale / len(army.soldiers)
        return average_morale >= 25

    rounds = 10
    for _ in range(rounds):
        hits1 = inflict_hits(army1, army2)
        hits2 = inflict_hits(army2, army1)

        casualties1 = apply_hits(hits2, army1)
        casualties2 = apply_hits(hits1, army2)

        if not morale_check(army1) or not morale_check(army2):
            break

    if len(army1.soldiers) > len(army2.soldiers):
        winner = army1.name
    else:
        winner = army2.name

    casualties1 = len(army1.soldiers) - sum(soldier.health > 0 for soldier in army1.soldiers)
    casualties2 = len(army2.soldiers) - sum(soldier.health > 0 for soldier in army2.soldiers)

    return winner, casualties1, casualties2


def print_soldier_info(soldier):
    print(f"Name: {soldier.name}")
    print(f"Rank: {soldier.rank}")
    print(f"Unit type: {soldier.unit_type.capitalize()}")
    print(f"Health: {soldier.health}")
    print(f"Training: {soldier.training:.2f}")
    print(f"Morale: {soldier.morale:.2f}")


def navigate_army(army):
    while True:
        print("\nCommands:")
        print("  ls - list all regiments")
        print("  reg <regiment_name> - explore a regiment")
        print("  exit - exit the program")
        command = input("Enter a command: ")

        if command == "ls":
            for soldier in army.soldiers:
                if isinstance(soldier, Officer) and soldier.leader_of:
                    regiment = next((r for r in soldier.leader_of if isinstance(r, Regiment)), None)
                    if regiment:
                        print(regiment)
        elif command.startswith("reg "):
            regiment_name = " ".join(command.split(" ")[1:])
            regiment = army.find_regiment(regiment_name)
            if regiment:
                navigate_regiment(regiment)
            else:
                print("Regiment not found.")
        elif command == "exit":
            break
        else:
            print("Invalid command.")


def navigate_regiment(regiment):
    while True:
        print("\nCommands:")
        print("  ls - list all companies")
        print("  comp <company_name> - explore a company")
        print("  back - go back to army level")
        command = input("Enter a command: ")

        if command == "ls":
            for company in regiment.companies:
                print(company)
        elif command.startswith("comp "):
            company_name = " ".join(command.split(" ")[1:])
            company = regiment.find_company(company_name)
            if company:
                navigate_company(company)
            else:
                print("Company not found.")
        elif command == "back":
            break
        else:
            print("Invalid command.")


def navigate_company(company):
    while True:
        print("\nCommands:")
        print("  ls - list all soldiers")
        print("  find <name> - find a soldier by name")
        print("  back - go back to regiment level")
        command = input("Enter a command: ")

        if command == "ls":
            for soldier in company.soldiers:
                print(soldier)
        elif command.startswith("find "):
            name = command.split(" ")[1]
            soldier = company.find_soldier(name)
            if soldier:
                print_soldier_info(soldier)
            else:
                print("Soldier not found.")
        elif command == "back":
            break
        else:
            print("Invalid command.")


def main():
    armies = []
    while True:
        print("Available commands:")
        print("1. Generate army")
        print("2. Display armies")
        print("3. Simulate combat")
        print("4. Quit")

        user_choice = input("Enter command number: ")

        if user_choice == "1":
            army_name = input("Enter army name: ")
            army_size = int(input("Enter army size: "))
            army = generate_army(army_name, army_size)
            armies.append(army)
            print(f"{army_name} generated.")

        elif user_choice == "2":
            if not armies:
                print("No armies generated yet.")
            else:
                for army in armies:
                    print(army.name)
                    display_army_structure(army)

        elif user_choice == "3":
            if len(armies) < 2:
                print("Need at least 2 armies to simulate combat.")
            else:
                army1 = armies[0]
                army2 = armies[1]
                winner, casualties1, casualties2 = combat(army1, army2)
                print(f"{winner.name} wins!")
                print(f"{army1.name} casualties: {casualties1}")
                print(f"{army2.name} casualties: {casualties2}")

        elif user_choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
