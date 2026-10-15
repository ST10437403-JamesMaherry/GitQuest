"""Discovery and loading for versioned scenario packs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Optional

from gitquest.domain.scenario import ScenarioManifest, ScenarioManifestError


def find_scenario_root() -> Path:
    """Find the repository scenario directory from a checkout or editable install."""
    candidates = (
        Path.cwd() / "scenarios",
        Path(__file__).resolve().parents[3] / "scenarios",
    )
    for candidate in candidates:
        if candidate.is_dir():
            return candidate.resolve()
    raise ScenarioManifestError(
        "Could not find the scenarios directory. Run GitQuest from the project checkout."
    )


def _manifest_paths(scenario_root: Path) -> Iterable[Path]:
    return sorted(scenario_root.glob("*/*/scenario.json"))


def load_manifest_file(path: Path) -> ScenarioManifest:
    """Load and validate one scenario manifest."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ScenarioManifestError(f"Could not read scenario manifest {path}: {error}") from error
    if not isinstance(data, dict):
        raise ScenarioManifestError(f"Scenario manifest must contain an object: {path}")

    manifest = ScenarioManifest.from_dict(data, path.parent)
    if manifest.id != path.parent.name:
        raise ScenarioManifestError(
            f"Scenario ID '{manifest.id}' must match directory '{path.parent.name}'."
        )
    if manifest.category != path.parent.parent.name:
        raise ScenarioManifestError(
            f"Scenario category '{manifest.category}' must match directory "
            f"'{path.parent.parent.name}'."
        )
    fixture = path.parent / "fixture"
    if fixture.is_symlink() or not fixture.is_dir():
        raise ScenarioManifestError(f"Scenario fixture directory is missing: {path.parent}")
    return manifest


def list_scenarios(scenario_root: Optional[Path] = None) -> tuple[ScenarioManifest, ...]:
    """Return every valid scenario in stable order."""
    root = (scenario_root or find_scenario_root()).resolve()
    manifests = tuple(load_manifest_file(path) for path in _manifest_paths(root))
    ids = [manifest.id for manifest in manifests]
    if len(ids) != len(set(ids)):
        raise ScenarioManifestError("Scenario IDs must be unique across all packs.")
    return manifests


def load_scenario(
    scenario_id: str,
    scenario_root: Optional[Path] = None,
) -> ScenarioManifest:
    """Return one scenario by ID."""
    matches = [item for item in list_scenarios(scenario_root) if item.id == scenario_id]
    if not matches:
        raise ScenarioManifestError(f"Unknown scenario: {scenario_id}")
    return matches[0]
