"""Capability diagnostics for GitQuest runtime profiles."""

from __future__ import annotations

import platform
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from gitquest.adapters.system_tools import inspect_tool
from gitquest.runtime.workspace import SANDBOX_ROOT, check_workspace_access


@dataclass(frozen=True)
class DiagnosticCheck:
    """One capability required by one or more GitQuest profiles."""

    key: str
    label: str
    available: bool
    profiles: tuple[str, ...]
    detail: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class DoctorReport:
    """Complete local capability report."""

    checks: tuple[DiagnosticCheck, ...]

    def check(self, key: str) -> DiagnosticCheck:
        return next(check for check in self.checks if check.key == key)

    def profile_ready(self, profile: str) -> bool:
        relevant = [check for check in self.checks if profile in check.profiles]
        return bool(relevant) and all(check.available for check in relevant)

    @property
    def lite_ready(self) -> bool:
        return self.profile_ready("Lite")

    def to_dict(self) -> dict:
        return {
            "lite_ready": self.lite_ready,
            "profiles": {
                profile: self.profile_ready(profile)
                for profile in ("Lite", "Standard", "Full")
            },
            "checks": [check.to_dict() for check in self.checks],
        }


TOOL_SPECS = (
    ("git", "Git", ("Lite", "Standard", "Full"), ("--version",)),
    ("podman", "Podman", ("Standard", "Full"), ("--version",)),
    ("gitleaks", "Gitleaks", ("Standard", "Full"), ("version",)),
    ("trivy", "Trivy", ("Standard", "Full"), ("--version",)),
    ("tofu", "OpenTofu", ("Full",), ("version",)),
    ("conftest", "Conftest", ("Full",), ("--version",)),
    ("kind", "kind", ("Full",), ("--version",)),
    ("kubectl", "kubectl", ("Full",), ("version", "--client")),
    ("cosign", "Cosign", ("Full",), ("version",)),
)


def _tool_checks() -> Iterable[DiagnosticCheck]:
    for key, label, profiles, version_arguments in TOOL_SPECS:
        tool = inspect_tool(key, version_arguments)
        if not tool.available:
            detail = "Not found on PATH."
        elif tool.error:
            detail = f"Found at {tool.path}; {tool.error}"
        else:
            detail = tool.version or f"Found at {tool.path}"

        yield DiagnosticCheck(
            key=key,
            label=label,
            available=tool.available and tool.error is None,
            profiles=profiles,
            detail=detail,
        )


def run_doctor(workspace_root: Path = SANDBOX_ROOT) -> DoctorReport:
    """Inspect required and optional local capabilities without changing project data."""
    python_available = sys.version_info >= (3, 9)
    python_check = DiagnosticCheck(
        key="python",
        label="Python",
        available=python_available,
        profiles=("Lite", "Standard", "Full"),
        detail=f"Python {platform.python_version()} ({sys.executable})",
    )

    workspace_available, workspace_detail = check_workspace_access(workspace_root)
    workspace_check = DiagnosticCheck(
        key="workspace",
        label="Managed workspace",
        available=workspace_available,
        profiles=("Lite", "Standard", "Full"),
        detail=workspace_detail,
    )

    return DoctorReport(checks=(python_check, workspace_check, *_tool_checks()))
