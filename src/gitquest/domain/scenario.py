"""Validated domain model for data-driven GitQuest scenarios."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Dict, Optional, Tuple


SCENARIO_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{1,63}$")
ITEM_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{1,63}$")
SUPPORTED_PROFILES = {"Lite", "Standard", "Full"}
SUPPORTED_CHECKS = {
    "path_absent": ("path",),
    "git_path_untracked": ("path",),
    "file_contains_line": ("path", "value"),
    "file_matches": ("path", "pattern"),
    "file_not_matches": ("path", "pattern"),
    "git_head_advanced": (),
    "git_clean": (),
}


class ScenarioManifestError(ValueError):
    """Raised when a scenario manifest is invalid or unsafe."""


def _required_text(data: Dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ScenarioManifestError(f"'{key}' must be a non-empty string.")
    return value.strip()


def _safe_relative_path(value: str) -> str:
    path = PurePosixPath(value)
    if path.is_absolute() or not path.parts or any(
        part in ("", ".", "..") for part in path.parts
    ):
        raise ScenarioManifestError(f"Scenario check path is not safe: {value}")
    if path.parts[0] in (".git", ".gitquest-workspace"):
        raise ScenarioManifestError(f"Scenario checks cannot inspect internal state: {value}")
    return path.as_posix()


@dataclass(frozen=True)
class ScenarioCheck:
    """One declarative assertion used to score an objective."""

    type: str
    path: Optional[str] = None
    value: Optional[str] = None
    pattern: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ScenarioCheck":
        if not isinstance(data, dict):
            raise ScenarioManifestError("Scenario checks must be objects.")
        check_type = _required_text(data, "type")
        if check_type not in SUPPORTED_CHECKS:
            raise ScenarioManifestError(f"Unsupported scenario check type: {check_type}")

        for required_key in SUPPORTED_CHECKS[check_type]:
            _required_text(data, required_key)

        path = data.get("path")
        if path is not None:
            if not isinstance(path, str):
                raise ScenarioManifestError("Scenario check paths must be strings.")
            path = _safe_relative_path(path)

        value = data.get("value")
        pattern = data.get("pattern")
        if value is not None and not isinstance(value, str):
            raise ScenarioManifestError("Scenario check values must be strings.")
        if pattern is not None:
            if not isinstance(pattern, str):
                raise ScenarioManifestError("Scenario check patterns must be strings.")
            try:
                re.compile(pattern)
            except re.error as error:
                raise ScenarioManifestError(f"Invalid scenario regex: {error}") from error

        return cls(type=check_type, path=path, value=value, pattern=pattern)


@dataclass(frozen=True)
class ScenarioObjective:
    """A scored remediation outcome."""

    id: str
    title: str
    description: str
    points: int
    checks: Tuple[ScenarioCheck, ...]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ScenarioObjective":
        if not isinstance(data, dict):
            raise ScenarioManifestError("Scenario objectives must be objects.")
        objective_id = _required_text(data, "id")
        if not ITEM_ID_PATTERN.fullmatch(objective_id):
            raise ScenarioManifestError(f"Invalid objective ID: {objective_id}")

        points = data.get("points")
        if not isinstance(points, int) or isinstance(points, bool) or points <= 0:
            raise ScenarioManifestError("Objective points must be a positive integer.")

        raw_checks = data.get("checks")
        if not isinstance(raw_checks, list) or not raw_checks:
            raise ScenarioManifestError("Every objective must define at least one check.")

        return cls(
            id=objective_id,
            title=_required_text(data, "title"),
            description=_required_text(data, "description"),
            points=points,
            checks=tuple(ScenarioCheck.from_dict(check) for check in raw_checks),
        )


@dataclass(frozen=True)
class ScenarioManifest:
    """A complete, versioned scenario definition."""

    schema_version: int
    id: str
    title: str
    summary: str
    category: str
    difficulty: str
    profile: str
    objectives: Tuple[ScenarioObjective, ...]
    debrief: Tuple[str, ...]
    source_directory: Path

    @property
    def total_points(self) -> int:
        return sum(objective.points for objective in self.objectives)

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
        source_directory: Path,
    ) -> "ScenarioManifest":
        if data.get("schema_version") != 1:
            raise ScenarioManifestError("Only scenario schema_version 1 is supported.")

        scenario_id = _required_text(data, "id")
        if not SCENARIO_ID_PATTERN.fullmatch(scenario_id):
            raise ScenarioManifestError(f"Invalid scenario ID: {scenario_id}")

        profile = _required_text(data, "profile")
        if profile not in SUPPORTED_PROFILES:
            raise ScenarioManifestError(f"Unsupported runtime profile: {profile}")

        raw_objectives = data.get("objectives")
        if not isinstance(raw_objectives, list) or not raw_objectives:
            raise ScenarioManifestError("A scenario must define at least one objective.")
        objectives = tuple(ScenarioObjective.from_dict(item) for item in raw_objectives)
        objective_ids = [objective.id for objective in objectives]
        if len(objective_ids) != len(set(objective_ids)):
            raise ScenarioManifestError("Scenario objective IDs must be unique.")
        if sum(objective.points for objective in objectives) != 100:
            raise ScenarioManifestError("Scenario objective points must total 100.")

        raw_debrief = data.get("debrief", [])
        if not isinstance(raw_debrief, list) or not all(
            isinstance(item, str) and item.strip() for item in raw_debrief
        ):
            raise ScenarioManifestError("Scenario debrief must be a list of non-empty strings.")

        return cls(
            schema_version=1,
            id=scenario_id,
            title=_required_text(data, "title"),
            summary=_required_text(data, "summary"),
            category=_required_text(data, "category"),
            difficulty=_required_text(data, "difficulty"),
            profile=profile,
            objectives=objectives,
            debrief=tuple(item.strip() for item in raw_debrief),
            source_directory=source_directory.resolve(),
        )
