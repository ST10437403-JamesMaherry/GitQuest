"""Git CLI adapter used by sandbox validators."""

import subprocess


def run_git_command(sandbox_path, command):
    """Run a Git command inside a sandbox directory."""
    return subprocess.run(
        command,
        cwd=sandbox_path,
        capture_output=True,
        text=True,
    )


def is_git_repository(sandbox_path):
    """Return whether a directory is inside a Git work tree."""
    result = run_git_command(
        sandbox_path,
        ["git", "rev-parse", "--is-inside-work-tree"],
    )
    return result.returncode == 0 and result.stdout.strip() == "true"


def has_commit(sandbox_path):
    """Return whether a sandbox repository has at least one commit."""
    result = run_git_command(
        sandbox_path,
        ["git", "rev-parse", "--verify", "HEAD"],
    )
    return result.returncode == 0


def has_branch(sandbox_path, branch_name):
    """Return whether a named local branch exists."""
    result = run_git_command(
        sandbox_path,
        ["git", "branch", "--list", branch_name],
    )
    return branch_name in result.stdout
