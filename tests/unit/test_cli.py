import io
import json
import unittest
from contextlib import redirect_stdout
from unittest.mock import Mock, patch

from gitquest.application.doctor import DiagnosticCheck, DoctorReport
from gitquest.cli import main


class CliTests(unittest.TestCase):
    @patch("gitquest.cli.GameEngine")
    def test_no_command_starts_game_for_backwards_compatibility(self, engine_class):
        self.assertEqual(main([]), 0)
        engine_class.return_value.start.assert_called_once_with()

    @patch("gitquest.cli.GameEngine")
    def test_play_command_starts_game(self, engine_class):
        self.assertEqual(main(["play"]), 0)
        engine_class.return_value.start.assert_called_once_with()

    @patch("gitquest.cli.run_doctor")
    def test_doctor_json_is_machine_readable(self, run_doctor_mock):
        run_doctor_mock.return_value = DoctorReport(
            checks=(
                DiagnosticCheck("git", "Git", True, ("Lite",), "ready"),
            )
        )
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(["doctor", "--json"])

        self.assertEqual(exit_code, 0)
        self.assertTrue(json.loads(output.getvalue())["lite_ready"])

    @patch("gitquest.cli.render_doctor_report")
    @patch("gitquest.cli.run_doctor")
    def test_doctor_returns_nonzero_when_lite_is_not_ready(
        self, run_doctor_mock, render_mock
    ):
        report = Mock(lite_ready=False)
        run_doctor_mock.return_value = report

        self.assertEqual(main(["doctor"]), 1)
        render_mock.assert_called_once_with(report)

    @patch("gitquest.cli.render_scenario_list")
    @patch("gitquest.cli.list_scenarios")
    def test_scenario_list_uses_catalog(self, list_scenarios_mock, render_mock):
        list_scenarios_mock.return_value = ()

        self.assertEqual(main(["scenario", "list"]), 0)
        render_mock.assert_called_once_with(())

    @patch("gitquest.cli.serve_web")
    def test_web_command_starts_local_interface(self, serve_web_mock):
        serve_web_mock.return_value = 0

        self.assertEqual(main(["web", "--port", "8765", "--no-open"]), 0)
        serve_web_mock.assert_called_once_with(port=8765, open_browser=False)


if __name__ == "__main__":
    unittest.main()
