import tempfile
import unittest
from pathlib import Path

from gitquest.adapters.git_cli import is_git_repository, run_git_command


class GitCliIntegrationTests(unittest.TestCase):
    def test_detects_initialized_repository(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)
            result = run_git_command(repository, ["git", "init", "--quiet"])

            if result.returncode == 127:
                self.skipTest("Git is not installed.")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(is_git_repository(repository))

    def test_rejects_non_git_commands(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            with self.assertRaises(ValueError):
                run_git_command(Path(temporary_directory), ["echo", "unsafe"])


if __name__ == "__main__":
    unittest.main()
