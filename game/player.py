class Player:
    def __init__(self, name, level=1, xp=0, completed_missions=None):
        self.name = name
        self.level = level
        self.xp = xp
        self.completed_missions = completed_missions or []

    def add_xp(self, amount):
        self.xp += amount
        print(f"\nYou gained {amount} XP!")

        if self.xp >= self.level * 100:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp = 0
        print(f"\nLevel up! You are now level {self.level}.")

    def complete_mission(self, mission_id):
        if mission_id not in self.completed_missions:
            self.completed_missions.append(mission_id)