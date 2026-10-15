"""Bounded Git CLI adapter used by sandbox validators."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Mapping, Optional, Sequence


GIT_TIMEOUT_SECONDS = 10


def run_git_command(
    sandbox_path: Path,
    command: Sequence[str],
    timeout: int = GIT_TIMEOUT_SECONDS,
    environment_overrides: Optional[Mapping[str, str]] = None,
) -> subprocess.CompletedProcess:
    """Run a non-interactive Git command with a timeout and captured output."""
    if not command or command[0] != "git":
        raise ValueError("The Git adapter only accepts commands beginning with 'git'.")

    environment = os.environ.copy()
    environment.update(
        {
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_TERMINAL_PROMPT": "0",
            "LC_ALL": "C",
        }
    )
    if environment_overrides:
        environment.update(environment_overrides)

    try:
        return subprocess.run(
            list(command),
            cwd=sandbox_path,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=environment,
            check=False,
        )
    except FileNotFoundError:
        return subprocess.CompletedProcess(command, 127, "", "Git executable was not found.")
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(
            command,
            124,
            "",
            f"Git command exceeded the {timeout}-second timeout.",
        )


def is_git_repository(sandbox_path: Path) -> bool:
    """Return whether a directory is inside a Git work tree."""
    result = run_git_command(
        sandbox_path,
        ["git", "rev-parse", "--is-inside-work-tree"],
    )
    return result.returncode == 0 and result.stdout.strip() == "true"


def has_commit(sandbox_path: Path) -> bool:
    """Return whether a sandbox repository has at least one commit."""
    result = run_git_command(
        sandbox_path,
        ["git", "rev-parse", "--verify", "HEAD"],
    )
    return result.returncode == 0


def has_branch(sandbox_path: Path, branch_name: str) -> bool:
    """Return whether a named local branch exists."""
    result = run_git_command(
        sandbox_path,
        ["git", "branch", "--list", branch_name],
    )
    branches = (line.lstrip("* ").strip() for line in result.stdout.splitlines())
    return result.returncode == 0 and branch_name in branches
