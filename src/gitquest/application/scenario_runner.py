"""Prepare, inspect, and score hands-on security scenarios."""

from __future__ import annotations

import json
import re
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Mapping, Optional, Tuple

from gitquest.adapters.git_cli import run_git_command
from gitquest.domain.scenario import ScenarioCheck, ScenarioManifest, ScenarioObjective
from gitquest.runtime.workspace import (
    SANDBOX_ROOT,
    PathLike,
    create_managed_workspace,
    get_managed_workspace,
)


SESSION_FILE = "gitquest-session.json"


class ScenarioRuntimeError(RuntimeError):
    """Raised when a scenario cannot be prepared or inspected safely."""


@dataclass(frozen=True)
class CheckResult:
    """Result of one declarative scenario check."""

    type: str
    passed: bool
    message: str


@dataclass(frozen=True)
class ObjectiveResult:
    """Scored result for one scenario objective."""

    id: str
    title: str
    description: str
    points: int
    passed: bool
    checks: Tuple[CheckResult, ...]

    @property
    def awarded_points(self) -> int:
        return self.points if self.passed else 0


@dataclass(frozen=True)
class ScenarioResult:
    """Complete verification result and portfolio-safe evidence metadata."""

    scenario_id: str
    title: str
    workspace: str
    baseline_commit: str
    current_commit: str
    objectives: Tuple[ObjectiveResult, ...]
    debrief: Tuple[str, ...]

    @property
    def score(self) -> int:
        return sum(objective.awarded_points for objective in self.objectives)

    @property
    def passed(self) -> bool:
        return all(objective.passed for objective in self.objectives)

    def to_dict(self) -> dict:
        return {
            "scenario_id": self.scenario_id,
            "title": self.title,
            "workspace": self.workspace,
            "baseline_commit": self.baseline_commit,
            "current_commit": self.current_commit,
            "score": self.score,
            "passed": self.passed,
            "objectives": [
                {
                    **asdict(objective),
                    "awarded_points": objective.awarded_points,
                }
                for objective in self.objectives
            ],
            "debrief": list(self.debrief),
        }


def scenario_workspace_name(scenario_id: str) -> str:
    return f"scenario_{scenario_id}"


def default_scenario_workspace_root(manifest: ScenarioManifest) -> Path:
    """Anchor generated workspaces to the checkout, independent of the shell directory."""
    project_root = manifest.source_directory.parents[2]
    return project_root / SANDBOX_ROOT


def _run_required_git(
    workspace: Path,
    command: list[str],
    environment_overrides: Optional[Mapping[str, str]] = None,
) -> str:
    result = run_git_command(
        workspace,
        command,
        environment_overrides=environment_overrides,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "Unknown Git failure."
        raise ScenarioRuntimeError(f"Git command failed ({' '.join(command)}): {detail}")
    return result.stdout.strip()


def _copy_fixture(fixture: Path, workspace: Path) -> None:
    if not fixture.is_dir():
        raise ScenarioRuntimeError(f"Scenario fixture does not exist: {fixture}")
    for source in fixture.rglob("*"):
        if source.is_symlink():
            raise ScenarioRuntimeError(f"Scenario fixtures cannot contain symlinks: {source}")
    shutil.copytree(fixture, workspace, dirs_exist_ok=True)


def start_scenario(
    manifest: ScenarioManifest,
    workspace_root: Optional[PathLike] = None,
) -> Path:
    """Create a fresh vulnerable repository and record its baseline commit."""
    resolved_workspace_root = workspace_root or default_scenario_workspace_root(manifest)
    workspace = create_managed_workspace(
        scenario_workspace_name(manifest.id),
        root=resolved_workspace_root,
    )
    _copy_fixture(manifest.source_directory / "fixture", workspace)

    _run_required_git(workspace, ["git", "init", "--quiet"])
    _run_required_git(workspace, ["git", "config", "user.name", "GitQuest Scenario Bot"])
    _run_required_git(
        workspace,
        ["git", "config", "user.email", "scenario-bot@gitquest.local"],
    )
    disabled_hooks = workspace / ".git" / "gitquest-hooks-disabled"
    disabled_hooks.mkdir()
    _run_required_git(
        workspace,
        ["git", "config", "core.hooksPath", str(disabled_hooks)],
    )

    exclude_file = workspace / ".git" / "info" / "exclude"
    with exclude_file.open("a", encoding="utf-8") as file:
        file.write("\n.gitquest-workspace\n")

    _run_required_git(workspace, ["git", "add", "--all"])
    _run_required_git(
        workspace,
        [
            "git",
            "-c",
            "commit.gpgsign=false",
            "commit",
            "--quiet",
            "-m",
            "Baseline: compromised release pipeline",
        ],
        environment_overrides={
            "GIT_AUTHOR_DATE": "2026-01-01T00:00:00Z",
            "GIT_COMMITTER_DATE": "2026-01-01T00:00:00Z",
        },
    )
    baseline_commit = _run_required_git(workspace, ["git", "rev-parse", "HEAD"])

    session_data = {
        "schema_version": 1,
        "scenario_id": manifest.id,
        "baseline_commit": baseline_commit,
    }
    (workspace / ".git" / SESSION_FILE).write_text(
        json.dumps(session_data, indent=2) + "\n",
        encoding="utf-8",
    )
    return workspace


def _load_session(workspace: Path, scenario_id: str) -> dict:
    path = workspace / ".git" / SESSION_FILE
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ScenarioRuntimeError(
            "Scenario session metadata is missing or invalid. Start the scenario again."
        ) from error
    if (
        not isinstance(data, dict)
        or data.get("schema_version") != 1
        or data.get("scenario_id") != scenario_id
        or not isinstance(data.get("baseline_commit"), str)
    ):
        raise ScenarioRuntimeError("Scenario session metadata does not match this scenario.")
    return data


def _read_check_file(workspace: Path, check: ScenarioCheck) -> Optional[str]:
    if check.path is None:
        return None
    target = workspace / check.path
    current = workspace
    for part in Path(check.path).parts:
        current = current / part
        if current.is_symlink():
            return None
    if not target.is_file():
        return None
    try:
        return target.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def _evaluate_check(
    workspace: Path,
    check: ScenarioCheck,
    baseline_commit: str,
    current_commit: str,
) -> CheckResult:
    target = workspace / check.path if check.path else None

    if check.type == "path_absent":
        passed = target is not None and not target.exists() and not target.is_symlink()
        message = (
            f"{check.path} is absent."
            if passed
            else f"Remove {check.path} from the workspace."
        )
    elif check.type == "git_path_untracked":
        result = run_git_command(
            workspace,
            ["git", "ls-files", "--error-unmatch", "--", check.path or ""],
        )
        passed = result.returncode != 0
        message = (
            f"{check.path} is not tracked by Git."
            if passed
            else f"Remove {check.path} from the Git index."
        )
    elif check.type == "file_contains_line":
        content = _read_check_file(workspace, check)
        passed = content is not None and check.value in {
            line.strip() for line in content.splitlines()
        }
        message = (
            f"{check.path} contains the required protection."
            if passed
            else f"Add the exact line '{check.value}' to {check.path}."
        )
    elif check.type in ("file_matches", "file_not_matches"):
        content = _read_check_file(workspace, check)
        matched = bool(
            content is not None
            and check.pattern is not None
            and re.search(check.pattern, content, flags=re.MULTILINE | re.IGNORECASE)
        )
        passed = matched if check.type == "file_matches" else content is not None and not matched
        message = (
            f"{check.path} satisfies the policy."
            if passed
            else f"Review the unsafe or missing configuration in {check.path}."
        )
    elif check.type == "git_head_advanced":
        passed = bool(current_commit) and current_commit != baseline_commit
        message = (
            "A remediation commit exists."
            if passed
            else "Commit the remediation so the incident response is auditable."
        )
    elif check.type == "git_clean":
        result = run_git_command(workspace, ["git", "status", "--porcelain"])
        passed = result.returncode == 0 and not result.stdout.strip()
        message = (
            "The remediation repository is clean."
            if passed
            else "Commit all remediation changes before verification."
        )
    else:
        passed = False
        message = f"Unsupported check type: {check.type}"

    return CheckResult(type=check.type, passed=passed, message=message)


def _evaluate_objective(
    workspace: Path,
    objective: ScenarioObjective,
    baseline_commit: str,
    current_commit: str,
) -> ObjectiveResult:
    checks = tuple(
        _evaluate_check(workspace, check, baseline_commit, current_commit)
        for check in objective.checks
    )
    return ObjectiveResult(
        id=objective.id,
        title=objective.title,
        description=objective.description,
        points=objective.points,
        passed=all(check.passed for check in checks),
        checks=checks,
    )


def verify_scenario(
    manifest: ScenarioManifest,
    workspace_root: Optional[PathLike] = None,
) -> ScenarioResult:
    """Verify the current remediation and return normalized evidence."""
    resolved_workspace_root = workspace_root or default_scenario_workspace_root(manifest)
    workspace = get_managed_workspace(
        scenario_workspace_name(manifest.id),
        root=resolved_workspace_root,
    )
    session = _load_session(workspace, manifest.id)
    baseline_commit = session["baseline_commit"]
    current_commit = _run_required_git(workspace, ["git", "rev-parse", "HEAD"])
    objectives = tuple(
        _evaluate_objective(workspace, objective, baseline_commit, current_commit)
        for objective in manifest.objectives
    )
    return ScenarioResult(
        scenario_id=manifest.id,
        title=manifest.title,
        workspace=workspace.name,
        baseline_commit=baseline_commit,
        current_commit=current_commit,
        objectives=objectives,
        debrief=manifest.debrief,
    )
