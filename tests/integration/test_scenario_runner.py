import json
import tempfile
import unittest
from pathlib import Path

from gitquest.adapters.git_cli import run_git_command
from gitquest.application.scenario_catalog import load_scenario
from gitquest.application.scenario_runner import start_scenario, verify_scenario
from gitquest.reporting.incident_report import write_incident_reports


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SCENARIO_ROOT = REPOSITORY_ROOT / "scenarios"
PINNED_CHECKOUT = "11bd71901bbe5b1630ceea73d27597364c9af683"


class ScenarioRunnerIntegrationTests(unittest.TestCase):
    def test_supply_chain_siege_has_a_reproducible_baseline(self):
        manifest = load_scenario("supply-chain-siege", SCENARIO_ROOT)

        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            start_scenario(manifest, workspace_root=temporary_path / "first")
            start_scenario(manifest, workspace_root=temporary_path / "second")

            first = verify_scenario(manifest, workspace_root=temporary_path / "first")
            second = verify_scenario(manifest, workspace_root=temporary_path / "second")

            self.assertEqual(first.baseline_commit, second.baseline_commit)

    def test_supply_chain_siege_fails_then_passes_and_writes_safe_evidence(self):
        manifest = load_scenario("supply-chain-siege", SCENARIO_ROOT)

        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            workspace_root = temporary_path / "workspaces"
            workspace = start_scenario(manifest, workspace_root=workspace_root)

            initial_result = verify_scenario(manifest, workspace_root=workspace_root)
            self.assertFalse(initial_result.passed)
            self.assertEqual(initial_result.score, 0)

            (workspace / ".env").unlink()
            (workspace / ".gitignore").write_text("__pycache__/\ndist/\n.env\n")
            workflow = workspace / ".github" / "workflows" / "release.yml"
            workflow.write_text(
                "name: Release\n"
                "jobs:\n"
                "  build:\n"
                "    steps:\n"
                "      - uses: actions/checkout@" + PINNED_CHECKOUT + "\n"
                "      - run: bash ./scripts/install-tool.sh\n",
                encoding="utf-8",
            )
            add_result = run_git_command(workspace, ["git", "add", "--all"])
            self.assertEqual(add_result.returncode, 0, add_result.stderr)
            commit_result = run_git_command(
                workspace,
                [
                    "git",
                    "-c",
                    "commit.gpgsign=false",
                    "commit",
                    "-m",
                    "security: contain supply chain incident",
                ],
            )
            self.assertEqual(commit_result.returncode, 0, commit_result.stderr)

            result = verify_scenario(manifest, workspace_root=workspace_root)
            self.assertTrue(result.passed)
            self.assertEqual(result.score, 100)

            markdown_path, json_path = write_incident_reports(
                result,
                output_root=temporary_path / "reports",
            )
            markdown = markdown_path.read_text(encoding="utf-8")
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertIn("**Outcome:** PASSED", markdown)
            self.assertNotIn("training-token-not-a-real-secret", markdown)
            self.assertTrue(payload["passed"])
            self.assertEqual(payload["score"], 100)


if __name__ == "__main__":
    unittest.main()
