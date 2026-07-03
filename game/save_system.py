import json
from pathlib import Path

from game.player import Player


SAVE_FILE = Path("data/progress.json")


def save_player(player):
    data = {
        "name": player.name,
        "level": player.level,
        "xp": player.xp,
        "completed_missions": player.completed_missions
    }

    SAVE_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(SAVE_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_player():
    if not SAVE_FILE.exists():
        return None

    with open(SAVE_FILE, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            return None

    if not data:
        return None

    return Player(
        name=data["name"],
        level=data["level"],
        xp=data["xp"],
        completed_missions=data["completed_missions"]
    )

def reset_progress():
    """
    Resets the player's saved progress.

    This deletes the progress.json file so the game behaves like it is
    being started for the first time again.

    Returns:
        True if a save file was deleted.
        False if there was no save file to delete.
    """
    # Check whether the save file currently exists.
    # We do this first so the game can give accurate feedback to the player.
    if SAVE_FILE.exists():
        SAVE_FILE.unlink()

        # Returning True tells the game engine that progress was actually reset.
        return True

    # Returning False tells the game engine there was no saved progress to reset.
    return False