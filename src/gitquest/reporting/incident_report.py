"""Portfolio-safe evidence reports for completed scenario attempts."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Tuple

from gitquest.application.scenario_runner import ScenarioResult


def _markdown_report(result: ScenarioResult, generated_at: str) -> str:
    outcome = "PASSED" if result.passed else "IN PROGRESS"
    rows = [
        f"# GitQuest Incident Report: {result.title}",
        "",
        f"- **Scenario:** `{result.scenario_id}`",
        f"- **Outcome:** {outcome}",
        f"- **Score:** {result.score}/100",
        f"- **Generated:** {generated_at}",
        f"- **Baseline commit:** `{result.baseline_commit}`",
        f"- **Verified commit:** `{result.current_commit}`",
        "",
        "## Objective evidence",
        "",
        "| Objective | Result | Points |",
        "| --- | --- | ---: |",
    ]
    for objective in result.objectives:
        status = "PASS" if objective.passed else "NEEDS WORK"
        rows.append(
            f"| {objective.title} | {status} | {objective.awarded_points}/{objective.points} |"
        )

    rows.extend(["", "## Control evidence", ""])
    for objective in result.objectives:
        rows.append(f"### {objective.title}")
        rows.append("")
        for check in objective.checks:
            marker = "x" if check.passed else " "
            rows.append(f"- [{marker}] `{check.type}` — {check.message}")
        rows.append("")

    rows.extend(["## Debrief", ""])
    rows.extend(f"- {item}" for item in result.debrief)
    rows.extend(
        [
            "",
            "## Evidence handling",
            "",
            "This report contains check results and commit identifiers only. Secret values and "
            "file contents are intentionally excluded.",
            "",
        ]
    )
    return "\n".join(rows)


def write_incident_reports(
    result: ScenarioResult,
    output_root: Path = Path("artifacts") / "reports",
) -> Tuple[Path, Path]:
    """Write JSON and Markdown evidence without copying potentially sensitive files."""
    if not output_root.is_absolute():
        current = Path.cwd()
        for part in output_root.parts:
            current = current / part
            if current.is_symlink():
                raise OSError(f"Report path cannot contain symbolic links: {output_root}")
    if output_root.is_symlink():
        raise OSError(f"Report directory cannot be a symbolic link: {output_root}")
    output_root.mkdir(parents=True, exist_ok=True)
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    stem = f"{result.scenario_id}-latest"
    json_path = output_root / f"{stem}.json"
    markdown_path = output_root / f"{stem}.md"
    if json_path.is_symlink() or markdown_path.is_symlink():
        raise OSError("Refusing to replace a symbolic-link evidence report.")

    payload = {"generated_at": generated_at, **result.to_dict()}
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(_markdown_report(result, generated_at), encoding="utf-8")
    return markdown_path.resolve(), json_path.resolve()
