"""GitQuest command-line entry point."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Optional, Sequence

from gitquest import __version__
from gitquest.application.doctor import run_doctor
from gitquest.application.engine import GameEngine
from gitquest.application.scenario_catalog import list_scenarios, load_scenario
from gitquest.application.scenario_runner import (
    ScenarioRuntimeError,
    start_scenario,
    verify_scenario,
)
from gitquest.domain.scenario import ScenarioManifestError
from gitquest.interfaces.doctor_ui import render_doctor_report
from gitquest.interfaces.scenario_ui import (
    render_scenario_list,
    render_scenario_result,
    render_scenario_started,
)
from gitquest.reporting.incident_report import write_incident_reports
from gitquest.runtime.workspace import WorkspaceSafetyError


def build_parser() -> argparse.ArgumentParser:
    """Build the public GitQuest command interface."""
    parser = argparse.ArgumentParser(
        prog="gitquest",
        description="A hands-on Git and DevSecOps learning adventure.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"GitQuest {__version__}",
    )

    commands = parser.add_subparsers(dest="command")
    commands.add_parser("play", help="Start the current GitQuest campaign.")

    doctor = commands.add_parser(
        "doctor",
        help="Check whether this machine can run each free GitQuest profile.",
    )
    doctor.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Print machine-readable diagnostic results.",
    )

    scenario = commands.add_parser(
        "scenario",
        help="Run a hands-on security incident scenario.",
    )
    scenario_commands = scenario.add_subparsers(dest="scenario_command", required=True)
    scenario_commands.add_parser("list", help="List available security scenarios.")

    scenario_start = scenario_commands.add_parser(
        "start",
        help="Create a fresh vulnerable repository for a scenario.",
    )
    scenario_start.add_argument("scenario_id", help="Scenario ID shown by 'scenario list'.")

    scenario_verify = scenario_commands.add_parser(
        "verify",
        help="Score a remediation and generate evidence reports.",
    )
    scenario_verify.add_argument("scenario_id", help="Scenario ID shown by 'scenario list'.")
    scenario_verify.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Print the verification result as JSON.",
    )
    return parser


def _run_scenario_command(args: argparse.Namespace) -> int:
    try:
        if args.scenario_command == "list":
            render_scenario_list(list_scenarios())
            return 0

        manifest = load_scenario(args.scenario_id)
        if args.scenario_command == "start":
            workspace = start_scenario(manifest)
            render_scenario_started(manifest, str(workspace))
            return 0

        result = verify_scenario(manifest)
        project_root = manifest.source_directory.parents[2]
        markdown_path, json_path = write_incident_reports(
            result,
            output_root=project_root / "artifacts" / "reports",
        )
        if args.json_output:
            payload = {
                **result.to_dict(),
                "reports": {
                    "markdown": str(markdown_path),
                    "json": str(json_path),
                },
            }
            print(json.dumps(payload, indent=2))
        else:
            render_scenario_result(
                result,
                (str(markdown_path), str(json_path)),
            )
        return 0 if result.passed else 1
    except (OSError, ScenarioManifestError, ScenarioRuntimeError, WorkspaceSafetyError) as error:
        print(f"GitQuest scenario error: {error}", file=sys.stderr)
        return 2


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Run a GitQuest command and return a process exit code."""
    args = build_parser().parse_args(argv)

    if args.command == "doctor":
        report = run_doctor()
        if args.json_output:
            print(json.dumps(report.to_dict(), indent=2))
        else:
            render_doctor_report(report)
        return 0 if report.lite_ready else 1

    if args.command == "scenario":
        return _run_scenario_command(args)

    GameEngine().start()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
