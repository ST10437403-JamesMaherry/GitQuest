import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from gitquest.adapters.system_tools import ToolInfo
from gitquest.application.doctor import DiagnosticCheck, DoctorReport, run_doctor


class DoctorReportTests(unittest.TestCase):
    def test_profile_readiness_uses_only_relevant_checks(self):
        report = DoctorReport(
            checks=(
                DiagnosticCheck("git", "Git", True, ("Lite", "Local"), "ready"),
                DiagnosticCheck("workspace", "Workspace", False, ("Local",), "missing"),
            )
        )

        self.assertTrue(report.profile_ready("Lite"))
        self.assertFalse(report.profile_ready("Local"))

    @patch("gitquest.application.doctor.check_workspace_access")
    @patch("gitquest.application.doctor.inspect_tool")
    def test_doctor_reports_lite_ready_when_git_is_available(
        self, inspect_tool_mock, workspace_access_mock
    ):
        workspace_access_mock.return_value = (True, "workspace ready")

        def inspect(name, version_arguments):
            return ToolInfo(name, "/usr/bin/git", "git version test")

        inspect_tool_mock.side_effect = inspect

        with tempfile.TemporaryDirectory() as temporary_directory:
            report = run_doctor(Path(temporary_directory))

        self.assertTrue(report.lite_ready)
        self.assertTrue(report.profile_ready("Local"))
        self.assertEqual(report.check("git").detail, "git version test")
        self.assertEqual(len(report.to_dict()["checks"]), 3)


if __name__ == "__main__":
    unittest.main()
