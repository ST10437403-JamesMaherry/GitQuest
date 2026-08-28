import re


def normalize_answer(answer):
    """
    Cleans up the player's answer so we can compare commands more fairly.

    Example:
        "  Git   Status  " becomes "git status"

    This helps us avoid marking an answer wrong just because of:
    - Extra spaces
    - Different capitalization
    """
    return " ".join(answer.lower().strip().split())


def check_exact_answer(player_answer, accepted_answers):
    """
    Checks whether the player's answer exactly matches one of the accepted answers.

    This is useful for simple commands like:
    - git init
    - git status
    - git add .

    Args:
        player_answer: The command typed by the player.
        accepted_answers: A list of valid command strings.

    Returns:
        True if the player's answer matches one accepted answer.
        False otherwise.
    """
    cleaned_player_answer = normalize_answer(player_answer)

    for accepted_answer in accepted_answers:
        cleaned_accepted_answer = normalize_answer(accepted_answer)

        if cleaned_player_answer == cleaned_accepted_answer:
            return True

    return False


def check_regex_answer(player_answer, accepted_patterns):
    """
    Checks whether the player's answer matches one of the accepted regex patterns.

    Regex patterns are useful for commands where part of the command changes.

    Example:
        git commit -m "My message"

    The message can be anything, so exact matching is too strict.

    Args:
        player_answer: The command typed by the player.
        accepted_patterns: A list of regex patterns.

    Returns:
        True if the player's answer matches one accepted pattern.
        False otherwise.
    """
    cleaned_player_answer = player_answer.strip()

    for pattern in accepted_patterns:
        if re.fullmatch(pattern, cleaned_player_answer, re.IGNORECASE):
            return True

    return False


def is_correct_answer(player_answer, mission):
    """
    Main answer-checking function used by the game engine.

    A mission can support:
    - exact accepted answers
    - regex accepted patterns

    This gives us flexible validation while keeping the game engine clean.

    Args:
        player_answer: The command typed by the player.
        mission: The current mission dictionary.

    Returns:
        True if the player's answer is correct.
        False otherwise.
    """
    accepted_answers = mission.get("accepted_answers", [])
    accepted_patterns = mission.get("accepted_patterns", [])

    if check_exact_answer(player_answer, accepted_answers):
        return True

    if check_regex_answer(player_answer, accepted_patterns):
        return True

    return False