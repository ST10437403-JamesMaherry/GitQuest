from rich.table import Table

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
from game.ui import (
    console,
    print_title,
    print_success,
    print_error,
    print_warning,
    print_info,
    print_story,
    create_menu_table
)
from game.sandbox_manager import create_sandbox, validate_sandbox_mission


class GameEngine:
    def __init__(self):
        """
        Creates the main game engine.

        The engine controls:
        - Starting the game
        - Loading or creating the player
        - Showing menus
        - Running missions
        - Saving progress
        """
        self.player = None

    def start(self):
        """
        Starts the game.

        This method is called from main.py and controls the first flow of the game.
        """
        self.show_intro()
        self.load_or_create_player()
        self.main_menu()

    def show_intro(self):
        """
        Shows the opening title screen.

        Rich panels make the intro feel more like a proper terminal game.
        """
        print_title(
            "GITQUEST: THE VERSION CONTROL ADVENTURE",
            "Master Git commands through missions, XP, and developer challenges."
        )

    def load_or_create_player(self):
        """
        Loads an existing player from the save file.

        If no save file exists, the game asks the user to create a new developer name.
        """
        existing_player = load_player()

        # If we already have saved progress, use it instead of creating a new player.
        if existing_player:
            self.player = existing_player
            print_success(f"Welcome back, {self.player.name}!")
            return

        # If there is no saved player, ask the user for a name.
        name = input("Enter your developer name: ").strip()

        # If the user presses Enter without typing a name, use a default name.
        if not name:
            name = "Apprentice"

        self.player = Player(name)
        save_player(self.player)

        print_success(f"Welcome, {self.player.name}. Your Git journey begins now.")

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
            table = create_menu_table("Main Menu")
            table.add_row("1", "Open mission map")
            table.add_row("2", "View player stats")
            table.add_row("3", "View learned commands")
            table.add_row("4", "Save and exit")

            console.print()
            console.print(table)

            choice = input("\nChoose an option: ").strip()

            if choice == "1":
                self.show_mission_map()
            elif choice == "2":
                self.show_stats()
            elif choice == "3":
                self.show_learned_commands()
            elif choice == "4":
                save_player(self.player)
                print_success("Progress saved. Goodbye!")
                break
            else:
                print_error("Invalid choice. Try again.")

    def show_mission_map(self):
        """
        Shows all mission areas available in the game.

        The player can choose an unlocked area to view its missions.
        Locked areas are shown, but cannot be entered yet.
        """
        area_keys = list(MISSION_AREAS.keys())

        while True:
            table = Table(title="Mission Map", show_header=True, header_style="bold cyan")
            table.add_column("Option", style="bold")
            table.add_column("Area")
            table.add_column("Progress")
            table.add_column("Status")

            for index, area_key in enumerate(area_keys, start=1):
                area = MISSION_AREAS[area_key]

                # Count how many missions exist in this area.
                total_missions = len(get_area_missions(area_key, MISSIONS))

                # Count how many of those missions the player has completed.
                completed_missions = count_completed_area_missions(
                    area_key,
                    MISSIONS,
                    self.player.completed_missions
                )

                # Show whether the area is unlocked based on the player's level.
                if is_area_unlocked(area, self.player):
                    lock_status = "[green]Unlocked[/green]"
                else:
                    lock_status = f"[red]Locked - Requires level {area['required_level']}[/red]"

                table.add_row(
                    str(index),
                    area["name"],
                    f"{completed_missions}/{total_missions}",
                    lock_status
                )

            table.add_row("0", "Back to main menu", "-", "[blue]Return[/blue]")

            console.print()
            console.print(table)

            choice = input("\nChoose an area: ").strip()

            if choice == "0":
                return

            if not choice.isdigit():
                print_warning("Please enter a valid number.")
                continue

            selected_index = int(choice)

            if selected_index < 1 or selected_index > len(area_keys):
                print_error("That area does not exist.")
                continue

            selected_area_key = area_keys[selected_index - 1]
            selected_area = MISSION_AREAS[selected_area_key]

            if not is_area_unlocked(selected_area, self.player):
                print_warning(
                    f"{selected_area['name']} is locked. "
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
            print_title(area["name"], area["description"])

            table = Table(title="Available Missions", show_header=True, header_style="bold cyan")
            table.add_column("Option", style="bold")
            table.add_column("Mission")
            table.add_column("XP")
            table.add_column("Status")

            for index, mission in enumerate(area_missions, start=1):
                if mission["id"] in self.player.completed_missions:
                    status = "[green]Completed[/green]"
                else:
                    status = "[yellow]Incomplete[/yellow]"

                table.add_row(
                    str(index),
                    mission["title"],
                    str(mission["xp"]),
                    status
                )

            table.add_row("0", "Back to mission map", "-", "[blue]Return[/blue]")

            console.print()
            console.print(table)

            choice = input("\nChoose a mission: ").strip()

            if choice == "0":
                return

            if not choice.isdigit():
                print_warning("Please enter a valid number.")
                continue

            selected_index = int(choice)

            if selected_index < 1 or selected_index > len(area_missions):
                print_error("That mission does not exist.")
                continue

            selected_mission = area_missions[selected_index - 1]

            if selected_mission["id"] in self.player.completed_missions:
                print_info("You have already completed this mission.")
                continue

            self.play_mission(selected_mission)

    def start_next_mission(self):
        """
        Starts the next incomplete mission.

        This is not currently used by the main menu, because we now use the mission map.
        It is being kept here in case we want to add a Quick Play option later.
        """
        for mission in MISSIONS:
            if mission["id"] not in self.player.completed_missions:
                self.play_mission(mission)
                return

        print_info("You have completed all available missions!")

    def play_mission(self, mission):
        """
        Runs a single mission.

        This method supports two mission types:

        1. Quiz missions:
           The player types an answer directly into the game.

        2. Sandbox missions:
           The game creates a temporary sandbox folder where the player can run Git commands.
           The game then checks whether the objective was completed.
        """
        mission_type = mission.get("mission_type", "quiz")

        if mission_type == "sandbox":
            self.play_sandbox_mission(mission)
            return

        self.play_quiz_mission(mission)

    def play_quiz_mission(self, mission):
        """
        Runs a normal quiz-style mission.

        The player types an answer directly into the game.
        """
        print_title(
            f"MISSION {mission['id']}: {mission['title']}",
            f"Reward: {mission['xp']} XP"
        )

        print_story(mission["story"])

        console.print(f"[bold white]{mission['question']}[/bold white]")
        answer = input("> ").strip()

        if is_correct_answer(answer, mission):
            self.complete_mission(mission)
        else:
            print_error("Not quite.")
            print_warning(f"Hint: {mission['hint']}")

    def play_sandbox_mission(self, mission):
        """
        Runs a sandbox-style mission.

        The game creates a temporary sandbox folder where the player can run Git commands.
        The game then checks whether the objective was completed.
        """
        print_title(
            f"SANDBOX MISSION {mission['id']}: {mission['title']}",
            f"Reward: {mission['xp']} XP"
        )

        print_story(mission["story"])

        sandbox_path = create_sandbox(mission["id"])
        absolute_path = sandbox_path.resolve()

        print_info("A clean sandbox folder has been created for this mission.")
        console.print()
        console.print("[bold cyan]Sandbox folder:[/bold cyan]")
        console.print(f"[white]{absolute_path}[/white]")
        console.print()

        console.print("[bold yellow]Instructions:[/bold yellow]")
        console.print("1. Open a new terminal tab or split terminal in VS Code.")
        console.print("2. Move into the sandbox folder using cd.")
        console.print("3. Run the required Git command.")
        console.print("4. Return to this game terminal and press Enter.")
        console.print()

        console.print("[bold cyan]Command to enter the sandbox:[/bold cyan]")
        console.print(f"cd {absolute_path}")
        console.print()

        console.print(f"[bold white]{mission['question']}[/bold white]")
        input("> Press Enter after completing the sandbox task...")

        if validate_sandbox_mission(mission, sandbox_path):
            self.complete_mission(mission)
        else:
            print_error("Sandbox objective not completed yet.")
            print_warning(f"Hint: {mission['hint']}")
            print_info("You can select the mission again to retry with a fresh sandbox.")

    def complete_mission(self, mission):
        """
        Rewards the player and saves progress after a mission is completed.

        This method is used by both quiz missions and sandbox missions.
        """
        print_success("Correct!")
        print_info(f"Command unlocked: {mission['command_unlocked']}")

        self.player.add_xp(mission["xp"])
        self.player.complete_mission(mission["id"])
        save_player(self.player)

    def show_stats(self):
        """
        Shows the player's current progress in a styled table.
        """
        table = Table(title="Player Stats", show_header=True, header_style="bold cyan")
        table.add_column("Stat")
        table.add_column("Value")

        table.add_row("Name", self.player.name)
        table.add_row("Level", str(self.player.level))
        table.add_row("XP", str(self.player.xp))
        table.add_row("Completed Missions", str(len(self.player.completed_missions)))

        console.print()
        console.print(table)

    def show_learned_commands(self):
        """
        Shows all Git commands unlocked by completing missions.
        """
        learned_commands = []

        for mission in MISSIONS:
            if mission["id"] in self.player.completed_missions:
                learned_commands.append(mission["command_unlocked"])

        if not learned_commands:
            print_warning("You have not unlocked any commands yet.")
            return

        table = Table(title="Learned Commands", show_header=True, header_style="bold cyan")
        table.add_column("Command", style="green")

        for command in learned_commands:
            table.add_row(command)

        console.print()
        console.print(table)