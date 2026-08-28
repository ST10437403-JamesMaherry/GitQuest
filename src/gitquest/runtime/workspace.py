"""Create disposable local workspaces for hands-on missions."""

import shutil
from pathlib import Path


SANDBOX_ROOT = Path("sandboxes")


def create_sandbox(mission_id):
    """Create a clean sandbox directory for a mission."""
    sandbox_path = SANDBOX_ROOT / f"mission_{mission_id}"

    if sandbox_path.exists():
        shutil.rmtree(sandbox_path)

    sandbox_path.mkdir(parents=True, exist_ok=True)
    return sandbox_path
