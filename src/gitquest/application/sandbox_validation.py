"""Application-level validation for the current Git sandbox missions."""

from gitquest.adapters.git_cli import has_branch, has_commit, is_git_repository


def validate_sandbox_mission(mission, sandbox_path):
    """
    Validates whether the player completed a sandbox mission correctly.

    This function returns two values:
    - A boolean showing whether the mission passed
    - A helpful message explaining the result

    Returning a message makes the game more beginner-friendly because
    the player can understand what they still need to fix.

    Args:
        mission: The mission dictionary.
        sandbox_path: The folder where the player ran Git commands.

    Returns:
        A tuple in this format:
        (passed_validation, feedback_message)

        Example:
        (True, "Sandbox objective completed successfully.")
        (False, "No commit was found yet.")
    """
    validation_type = mission.get("sandbox_validation")

    # Mission type: the player must initialize the folder as a Git repository.
    if validation_type == "is_git_repository":
        if is_git_repository(sandbox_path):
            return True, "Sandbox objective completed successfully."

        return False, (
            "This folder is not a Git repository yet. "
            "Make sure you moved into the sandbox folder and ran: git init"
        )

    # Mission type: the player must create at least one commit.
    if validation_type == "has_commit":
        # A commit can only exist inside a Git repository.
        # Checking this first gives the player a clearer error message.
        if not is_git_repository(sandbox_path):
            return False, (
                "No Git repository was found. "
                "Start by running: git init"
            )

        if has_commit(sandbox_path):
            return True, "A commit was found in the sandbox repository."

        return False, (
            "No commit was found yet. "
            "Create a file, run git add ., then run git commit -m \"First commit\"."
        )

    # Mission type: the player must create a specific branch.
    if validation_type == "has_branch":
        expected_branch = mission.get("expected_branch")

        # Again, check for a Git repository first so the feedback is more useful.
        if not is_git_repository(sandbox_path):
            return False, (
                "No Git repository was found. "
                "Start by running: git init"
            )

        if has_branch(sandbox_path, expected_branch):
            return True, f"The expected branch '{expected_branch}' was found."

        return False, (
            f"The expected branch '{expected_branch}' was not found. "
            f"Try running: git switch -c {expected_branch}"
        )

    # Fallback for unknown validation types.
    return False, (
        "This sandbox mission has an unknown validation type. "
        "Check the sandbox_validation value in the mission definition."
    )
