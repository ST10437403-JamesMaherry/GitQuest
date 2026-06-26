MISSION_AREAS = {
    "git_basics": {
        "name": "Git Basics",
        "description": "Learn the foundation commands every developer needs.",
        "required_level": 1
    },
    "branching_forest": {
        "name": "Branching Forest",
        "description": "Create, view, and switch between branches safely.",
        "required_level": 1
    },
    "merge_conflict_dungeon": {
        "name": "Merge Conflict Dungeon",
        "description": "Face one of Git's scariest challenges: merge conflicts.",
        "required_level": 3
    },
    "remote_repository_citadel": {
        "name": "Remote Repository Citadel",
        "description": "Learn how to work with GitHub and remote repositories.",
        "required_level": 4
    }
}


def get_area_missions(area_key, missions):
    """
    Finds all missions that belong to a specific area.

    Args:
        area_key: The internal key of the mission area.
        missions: The full list of missions.

    Returns:
        A list of missions for the selected area.
    """
    area_missions = []

    for mission in missions:
        if mission["area"] == area_key:
            area_missions.append(mission)

    return area_missions


def count_completed_area_missions(area_key, missions, completed_missions):
    """
    Counts how many missions the player has completed in a specific area.

    Args:
        area_key: The internal key of the mission area.
        missions: The full list of missions.
        completed_missions: The player's completed mission IDs.

    Returns:
        The number of completed missions in the selected area.
    """
    completed_count = 0

    for mission in missions:
        if mission["area"] == area_key and mission["id"] in completed_missions:
            completed_count += 1

    return completed_count


def is_area_unlocked(area_data, player):
    """
    Checks whether the player has unlocked an area.

    For now, area unlocking is based on player level.

    Args:
        area_data: The data for one mission area.
        player: The current player object.

    Returns:
        True if the player's level is high enough.
        False otherwise.
    """
    return player.level >= area_data["required_level"]