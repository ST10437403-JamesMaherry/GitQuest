from game.ui import print_success


class Player:
    def __init__(self, name, level=1, xp=0, completed_missions=None):
        """
        Creates a new player object.

        Args:
            name: The player's chosen developer name.
            level: The player's current level.
            xp: The player's current XP.
            completed_missions: A list of mission IDs the player has completed.
        """
        self.name = name
        self.level = level
        self.xp = xp
        self.completed_missions = completed_missions or []

    def add_xp(self, amount):
        """
        Adds XP to the player and checks if the player should level up.

        Args:
            amount: The amount of XP to add.
        """
        self.xp += amount
        print_success(f"You gained {amount} XP!")

        if self.xp >= self.level * 100:
            self.level_up()

    def level_up(self):
        """
        Increases the player's level and resets XP.

        Later, we can improve this to carry over leftover XP instead of resetting to 0.
        """
        self.level += 1
        self.xp = 0
        print_success(f"Level up! You are now level {self.level}.")

    def complete_mission(self, mission_id):
        """
        Adds a mission ID to the player's completed missions list.

        Args:
            mission_id: The ID of the completed mission.
        """
        if mission_id not in self.completed_missions:
            self.completed_missions.append(mission_id)