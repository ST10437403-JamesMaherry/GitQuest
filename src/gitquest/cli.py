"""GitQuest command-line entry point."""

from __future__ import annotations

import argparse
import json
from typing import Optional, Sequence

from gitquest import __version__
from gitquest.application.doctor import run_doctor
from gitquest.application.engine import GameEngine
from gitquest.interfaces.doctor_ui import render_doctor_report


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
    return parser


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

    GameEngine().start()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
