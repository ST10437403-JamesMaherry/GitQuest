from game.player import Player
from game.missions import MISSIONS
from game.save_system import save_player, load_player
from game.answer_checker import is_correct_answer
from game.mission_map import (
    MISSION_AREAS,
    get_area_missions,
    count_completed_area_missions,
    is_area_unlocked
)


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
        """
        Shows the main menu and keeps the game running until the player exits.

        The player can:
        - Open the mission map
        - View stats
        - View learned commands
        - Save and exit
        """
        while True:
            print("\n" + "=" * 30)
            print("MAIN MENU")
            print("=" * 30)
            print("1. Open mission map")
            print("2. View player stats")
            print("3. View learned commands")
            print("4. Save and exit")

            choice = input("\nChoose an option: ").strip()

            if choice == "1":
                self.show_mission_map()
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

    def show_mission_map(self):
        """
        Shows all mission areas available in the game.

        The player can choose an unlocked area to view its missions.
        Locked areas are shown, but cannot be entered yet.
        """
        area_keys = list(MISSION_AREAS.keys())

        while True:
            print("\n" + "=" * 40)
            print("MISSION MAP")
            print("=" * 40)

            for index, area_key in enumerate(area_keys, start=1):
                area = MISSION_AREAS[area_key]

                total_missions = len(get_area_missions(area_key, MISSIONS))
                completed_missions = count_completed_area_missions(
                    area_key,
                    MISSIONS,
                    self.player.completed_missions
                )

                if is_area_unlocked(area, self.player):
                    lock_status = "Unlocked"
                else:
                    lock_status = f"Locked - Requires level {area['required_level']}"

                print(
                    f"{index}. {area['name']} "
                    f"({completed_missions}/{total_missions}) - {lock_status}"
                )

            print("0. Back to main menu")

            choice = input("\nChoose an area: ").strip()

            if choice == "0":
                return

            if not choice.isdigit():
                print("\nPlease enter a valid number.")
                continue

            selected_index = int(choice)

            if selected_index < 1 or selected_index > len(area_keys):
                print("\nThat area does not exist.")
                continue

            selected_area_key = area_keys[selected_index - 1]
            selected_area = MISSION_AREAS[selected_area_key]

            if not is_area_unlocked(selected_area, self.player):
                print(
                    f"\n{selected_area['name']} is locked. "
                    f"Reach level {selected_area['required_level']} to unlock it."
                )
                continue

            self.show_area_missions(selected_area_key)

    def show_area_missions(self, area_key):
        """
        Shows the missions inside a selected area.

        The player can choose an incomplete mission to play.
        Completed missions are shown as completed.
        """
        area = MISSION_AREAS[area_key]
        area_missions = get_area_missions(area_key, MISSIONS)

        while True:
            print("\n" + "=" * 40)
            print(area["name"].upper())
            print("=" * 40)
            print(area["description"])
            print()

            for index, mission in enumerate(area_missions, start=1):
                if mission["id"] in self.player.completed_missions:
                    status = "Completed"
                else:
                    status = "Incomplete"

                print(f"{index}. {mission['title']} - {status}")

            print("0. Back to mission map")

            choice = input("\nChoose a mission: ").strip()

            if choice == "0":
                return

            if not choice.isdigit():
                print("\nPlease enter a valid number.")
                continue

            selected_index = int(choice)

            if selected_index < 1 or selected_index > len(area_missions):
                print("\nThat mission does not exist.")
                continue

            selected_mission = area_missions[selected_index - 1]

            if selected_mission["id"] in self.player.completed_missions:
                print("\nYou have already completed this mission.")
                continue

            self.play_mission(selected_mission)

    def start_next_mission(self):
        for mission in MISSIONS:
            if mission["id"] not in self.player.completed_missions:
                self.play_mission(mission)
                return

        print("\nYou have completed all available missions!")

    def play_mission(self, mission):
        """
        Runs a single mission.

        This method:
        - Shows the mission title and story
        - Asks the player a Git command question
        - Checks the answer using our flexible answer checker
        - Rewards the player if they are correct
        """
        print("\n" + "=" * 50)
        print(f"MISSION {mission['id']}: {mission['title']}")
        print("=" * 50)
        print(mission["story"])
        print()

        answer = input(mission["question"] + "\n> ").strip()

        if is_correct_answer(answer, mission):
            print("\nCorrect!")
            print(f"Command unlocked: {mission['command_unlocked']}")

            self.player.add_xp(mission["xp"])
            self.player.complete_mission(mission["id"])
            save_player(self.player)
        else:
            print("\nNot quite.")
            print(f"Hint: {mission['hint']}")

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