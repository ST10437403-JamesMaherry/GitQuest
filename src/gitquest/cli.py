"""GitQuest command-line entry point."""

from gitquest.application.engine import GameEngine

def main():
    game = GameEngine()
    game.start()


if __name__ == "__main__":
    main()
