"""GitQuest command-line entry point."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Optional, Sequence

from gitquest import __version__
from gitquest.application.doctor import run_doctor
from gitquest.application.engine import GameEngine
from gitquest.interfaces.doctor_ui import render_doctor_report
from gitquest.interfaces.web_app import serve_web


def build_parser() -> argparse.ArgumentParser:
    """Build the public GitQuest command interface."""
    parser = argparse.ArgumentParser(
        prog="gitquest",
        description="Learn Git and GitHub through guided, hands-on practice.",
    )
    parser.add_argument("--version", action="version", version=f"GitQuest {__version__}")

    commands = parser.add_subparsers(dest="command")
    commands.add_parser("play", help="Start the terminal learning campaign.")

    doctor = commands.add_parser(
        "doctor", help="Check whether this machine is ready to run GitQuest."
    )
    doctor.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Print machine-readable diagnostic results.",
    )

    web = commands.add_parser("web", help="Open the local GitQuest curriculum in a browser.")
    web.add_argument(
        "--port", type=int, default=8000, help="Localhost port to use (default: 8000)."
    )
    web.add_argument(
        "--no-open",
        action="store_true",
        help="Start the server without opening the browser automatically.",
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

    if args.command in {None, "web"}:
        port = getattr(args, "port", 8000)
        open_browser = not getattr(args, "no_open", False)
        try:
            return serve_web(port=port, open_browser=open_browser)
        except (OSError, ValueError) as error:
            print(f"GitQuest web error: {error}", file=sys.stderr)
            return 2

    GameEngine().start()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
