"""Read-only discovery of local command-line tools."""

from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass
from typing import Optional, Sequence


@dataclass(frozen=True)
class ToolInfo:
    """Discovery result for one external command-line tool."""

    name: str
    path: Optional[str]
    version: Optional[str]
    error: Optional[str] = None

    @property
    def available(self) -> bool:
        return self.path is not None


def inspect_tool(
    name: str,
    version_arguments: Sequence[str] = ("--version",),
    timeout: int = 5,
) -> ToolInfo:
    """Locate a tool and retrieve a short version string without using a shell."""
    executable = shutil.which(name)
    if executable is None:
        return ToolInfo(name=name, path=None, version=None)

    environment = os.environ.copy()
    environment.update({"LC_ALL": "C", "GIT_TERMINAL_PROMPT": "0"})

    try:
        result = subprocess.run(
            [executable, *version_arguments],
            capture_output=True,
            text=True,
            timeout=timeout,
            env=environment,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return ToolInfo(name=name, path=executable, version=None, error=str(error))

    version_output = (result.stdout or result.stderr).strip().splitlines()
    version = version_output[0][:160] if version_output else None
    error = None if result.returncode == 0 else f"Version command exited {result.returncode}."
    return ToolInfo(name=name, path=executable, version=version, error=error)
