from game.player import Player
from game.missions import MISSIONS
from game.save_system import save_player, load_player


class GameEngine:
    def __init__(self):
        self.player = None

    def start(self):
        self.show_intro()
        self.load_or_create_player()
        self.main_menu()

    def show_intro(self):
        print("=" * 50)
        print("GITQUEST: THE VERSION CONTROL ADVENTURE")
        print("=" * 50)
        print("Master Git commands by completing terminal-based missions.")
        print()

    def load_or_create_player(self):
        existing_player = load_player()

        if existing_player:
            self.player = existing_player
            print(f"Welcome back, {self.player.name}!")
            return

        name = input("Enter your developer name: ").strip()

        if not name:
            name = "Apprentice"

        self.player = Player(name)
        save_player(self.player)

        print(f"\nWelcome, {self.player.name}. Your Git journey begins now.")

    def main_menu(self):
        while True:
            print("\n" + "=" * 30)
            print("MAIN MENU")
            print("=" * 30)
            print("1. Start next mission")
            print("2. View player stats")
            print("3. View learned commands")
            print("4. Save and exit")

            choice = input("\nChoose an option: ").strip()

            if choice == "1":
                self.start_next_mission()
            elif choice == "2":
                self.show_stats()
            elif choice == "3":
                self.show_learned_commands()
            elif choice == "4":
                save_player(self.player)
                print("\nProgress saved. Goodbye!")
                break
            else:
                print("\nInvalid choice. Try again.")

    def start_next_mission(self):
        for mission in MISSIONS:
            if mission["id"] not in self.player.completed_missions:
                self.play_mission(mission)
                return

        print("\nYou have completed all available missions!")

    def play_mission(self, mission):
        print("\n" + "=" * 50)
        print(f"MISSION {mission['id']}: {mission['title']}")
        print("=" * 50)
        print(mission["story"])
        print()

        answer = input(mission["question"] + "\n> ").strip()

        if answer == mission["answer"]:
            print("\nCorrect!")
            print(f"Command unlocked: {mission['command_unlocked']}")

            self.player.add_xp(mission["xp"])
            self.player.complete_mission(mission["id"])
            save_player(self.player)
        else:
            print("\nNot quite.")
            print(f"Hint: The correct command is related to: {mission['command_unlocked']}")

    def show_stats(self):
        print("\n" + "=" * 30)
        print("PLAYER STATS")
        print("=" * 30)
        print(f"Name: {self.player.name}")
        print(f"Level: {self.player.level}")
        print(f"XP: {self.player.xp}")
        print(f"Completed missions: {len(self.player.completed_missions)}")

    def show_learned_commands(self):
        print("\n" + "=" * 30)
        print("LEARNED COMMANDS")
        print("=" * 30)

        learned_commands = []

        for mission in MISSIONS:
            if mission["id"] in self.player.completed_missions:
                learned_commands.append(mission["command_unlocked"])

        if not learned_commands:
            print("You have not unlocked any commands yet.")
            return

        for command in learned_commands:
            print(f"- {command}")