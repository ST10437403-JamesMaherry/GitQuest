import shutil
import subprocess
from pathlib import Path


# All sandbox folders will be created inside this folder.
# This keeps practice repositories separate from the main GitQuest repo.
SANDBOX_ROOT = Path("sandboxes")


def create_sandbox(mission_id):
    """
    Creates a clean sandbox folder for a mission.

    Args:
        mission_id: The ID of the mission that needs a sandbox.

    Returns:
        The path to the created sandbox folder.
    """
    sandbox_path = SANDBOX_ROOT / f"mission_{mission_id}"

    # If this sandbox already exists from a previous attempt, delete it first.
    # This gives the player a clean environment every time.
    if sandbox_path.exists():
        shutil.rmtree(sandbox_path)

    # Create the sandbox folder and any missing parent folders.
    sandbox_path.mkdir(parents=True, exist_ok=True)

    return sandbox_path


def run_git_command(sandbox_path, command):
    """
    Runs a Git command inside the sandbox folder.

    Args:
        sandbox_path: The folder where the command should run.
        command: The Git command as a list, for example ["git", "status"].

    Returns:
        A subprocess.CompletedProcess object containing the command result.
    """
    return subprocess.run(
        command,
        cwd=sandbox_path,
        capture_output=True,
        text=True
    )


def is_git_repository(sandbox_path):
    """
    Checks whether the sandbox folder is a valid Git repository.

    Args:
        sandbox_path: The folder to check.

    Returns:
        True if the folder is a Git repository.
        False otherwise.
    """
    result = run_git_command(
        sandbox_path,
        ["git", "rev-parse", "--is-inside-work-tree"]
    )

    return result.returncode == 0 and result.stdout.strip() == "true"


def has_commit(sandbox_path):
    """
    Checks whether the sandbox repository has at least one commit.

    Args:
        sandbox_path: The sandbox repository folder.

    Returns:
        True if the repository has at least one commit.
        False otherwise.
    """
    result = run_git_command(
        sandbox_path,
        ["git", "rev-parse", "--verify", "HEAD"]
    )

    return result.returncode == 0


def has_branch(sandbox_path, branch_name):
    """
    Checks whether a specific branch exists in the sandbox repository.

    Args:
        sandbox_path: The sandbox repository folder.
        branch_name: The name of the branch to check.

    Returns:
        True if the branch exists.
        False otherwise.
    """
    result = run_git_command(
        sandbox_path,
        ["git", "branch", "--list", branch_name]
    )

    return branch_name in result.stdout


def validate_sandbox_mission(mission, sandbox_path):
    """
    Validates whether the player completed a sandbox mission correctly.

    Args:
        mission: The mission dictionary.
        sandbox_path: The folder where the player ran Git commands.

    Returns:
        True if the mission objective was completed.
        False otherwise.
    """
    validation_type = mission.get("sandbox_validation")

    if validation_type == "is_git_repository":
        return is_git_repository(sandbox_path)

    if validation_type == "has_commit":
        return has_commit(sandbox_path)

    if validation_type == "has_branch":
        expected_branch = mission.get("expected_branch")
        return has_branch(sandbox_path, expected_branch)

    return False