"""Safe disposable workspaces for hands-on GitQuest missions."""

from __future__ import annotations

import re
import shutil
import tempfile
from pathlib import Path
from typing import Union


PathLike = Union[str, Path]

SANDBOX_ROOT = Path("sandboxes") / ".gitquest"
ROOT_MARKER = ".gitquest-root"
WORKSPACE_MARKER = ".gitquest-workspace"
MARKER_CONTENT = "managed-by=gitquest\n"
MISSION_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")
WORKSPACE_NAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,95}$")


class WorkspaceSafetyError(RuntimeError):
    """Raised when GitQuest cannot safely manage a workspace path."""


def normalize_mission_id(mission_id: object) -> str:
    """Return a filesystem-safe mission identifier or raise a clear error."""
    normalized = str(mission_id)
    if not MISSION_ID_PATTERN.fullmatch(normalized):
        raise WorkspaceSafetyError(
            "Mission IDs must contain only letters, numbers, hyphens, or underscores "
            "and be no longer than 64 characters."
        )
    return normalized


def normalize_workspace_name(workspace_name: object) -> str:
    """Return a safe managed-workspace name."""
    normalized = str(workspace_name)
    if not WORKSPACE_NAME_PATTERN.fullmatch(normalized):
        raise WorkspaceSafetyError(
            "Workspace names must contain only letters, numbers, hyphens, or underscores "
            "and be no longer than 96 characters."
        )
    return normalized


def ensure_sandbox_root(root: PathLike = SANDBOX_ROOT) -> Path:
    """Create and mark the managed sandbox root, rejecting a root symlink."""
    root_path = Path(root)
    if not root_path.is_absolute():
        current = Path.cwd()
        for part in root_path.parts:
            current = current / part
            if current.is_symlink():
                raise WorkspaceSafetyError(
                    "The GitQuest sandbox path cannot contain symbolic links."
                )
    if root_path.is_symlink():
        raise WorkspaceSafetyError("The GitQuest sandbox root cannot be a symbolic link.")

    root_path.mkdir(parents=True, exist_ok=True)
    marker = root_path / ROOT_MARKER

    if marker.exists() or marker.is_symlink():
        try:
            marker_is_valid = marker.is_file() and marker.read_text(
                encoding="utf-8"
            ) == MARKER_CONTENT
        except OSError as error:
            raise WorkspaceSafetyError(
                "The GitQuest sandbox root safety marker cannot be read."
            ) from error

        if not marker_is_valid:
            raise WorkspaceSafetyError("The GitQuest sandbox root has an invalid safety marker.")

    marker.write_text(MARKER_CONTENT, encoding="utf-8")
    return root_path.resolve()


def _assert_direct_child(workspace: Path, root: Path) -> None:
    """Require a workspace to be a direct child of the managed root."""
    if workspace.parent != root:
        raise WorkspaceSafetyError("Refusing to manage a path outside the sandbox root.")


def _remove_managed_workspace(workspace: Path, root: Path) -> None:
    """Remove only a marked, non-symlink workspace inside the managed root."""
    _assert_direct_child(workspace, root)

    if workspace.is_symlink():
        raise WorkspaceSafetyError("Refusing to remove a symbolic-link workspace.")

    marker = workspace / WORKSPACE_MARKER
    try:
        marker_is_valid = marker.is_file() and marker.read_text(
            encoding="utf-8"
        ) == MARKER_CONTENT
    except OSError as error:
        raise WorkspaceSafetyError(
            f"The workspace safety marker cannot be read: {workspace}"
        ) from error

    if not marker_is_valid:
        raise WorkspaceSafetyError(
            f"Refusing to reset unmarked directory: {workspace}. "
            "Move or remove it manually if it is safe to do so."
        )

    shutil.rmtree(workspace)


def create_managed_workspace(
    workspace_name: object,
    root: PathLike = SANDBOX_ROOT,
) -> Path:
    """Create a clean workspace that GitQuest can safely reset later."""
    normalized_name = normalize_workspace_name(workspace_name)
    root_path = ensure_sandbox_root(root)
    workspace = root_path / normalized_name
    _assert_direct_child(workspace, root_path)

    if workspace.exists() or workspace.is_symlink():
        _remove_managed_workspace(workspace, root_path)

    workspace.mkdir()
    (workspace / WORKSPACE_MARKER).write_text(MARKER_CONTENT, encoding="utf-8")
    return workspace


def get_managed_workspace(
    workspace_name: object,
    root: PathLike = SANDBOX_ROOT,
) -> Path:
    """Open an existing marked workspace without resetting its contents."""
    normalized_name = normalize_workspace_name(workspace_name)
    root_path = ensure_sandbox_root(root)
    workspace = root_path / normalized_name
    _assert_direct_child(workspace, root_path)

    if not workspace.exists() or not workspace.is_dir():
        raise WorkspaceSafetyError(f"Managed workspace does not exist: {workspace}")
    if workspace.is_symlink():
        raise WorkspaceSafetyError("Refusing to open a symbolic-link workspace.")

    marker = workspace / WORKSPACE_MARKER
    try:
        marker_is_valid = marker.is_file() and marker.read_text(
            encoding="utf-8"
        ) == MARKER_CONTENT
    except OSError as error:
        raise WorkspaceSafetyError(
            f"The workspace safety marker cannot be read: {workspace}"
        ) from error

    if not marker_is_valid:
        raise WorkspaceSafetyError(f"Refusing to open unmarked directory: {workspace}")
    return workspace


def create_sandbox(mission_id: object, root: PathLike = SANDBOX_ROOT) -> Path:
    """Create a clean, marked sandbox directory for a mission."""
    normalized_id = normalize_mission_id(mission_id)
    return create_managed_workspace(f"mission_{normalized_id}", root=root)


def check_workspace_access(root: PathLike = SANDBOX_ROOT) -> tuple[bool, str]:
    """Check that GitQuest can safely create temporary data below its root."""
    try:
        root_path = ensure_sandbox_root(root)
        with tempfile.TemporaryDirectory(prefix="doctor_", dir=root_path) as probe:
            probe_file = Path(probe) / "write-check"
            probe_file.write_text("ok\n", encoding="utf-8")
            if probe_file.read_text(encoding="utf-8") != "ok\n":
                return False, "Workspace write verification returned unexpected data."
    except (OSError, WorkspaceSafetyError) as error:
        return False, str(error)

    return True, f"Managed workspace is writable at {root_path}"
