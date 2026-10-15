import tempfile
import unittest
from pathlib import Path

from gitquest.runtime.workspace import (
    MARKER_CONTENT,
    ROOT_MARKER,
    WORKSPACE_MARKER,
    WorkspaceSafetyError,
    create_sandbox,
)


class WorkspaceTests(unittest.TestCase):
    def test_create_sandbox_marks_managed_directories(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "sandboxes"

            workspace = create_sandbox("F-01", root=root)

            self.assertEqual(workspace, root.resolve() / "mission_F-01")
            self.assertEqual((root / ROOT_MARKER).read_text(), MARKER_CONTENT)
            self.assertEqual((workspace / WORKSPACE_MARKER).read_text(), MARKER_CONTENT)

    def test_recreating_managed_sandbox_removes_stale_contents(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "sandboxes"
            workspace = create_sandbox("F-01", root=root)
            (workspace / "stale.txt").write_text("old data")

            recreated_workspace = create_sandbox("F-01", root=root)

            self.assertEqual(recreated_workspace, workspace)
            self.assertFalse((workspace / "stale.txt").exists())

    def test_invalid_mission_ids_are_rejected(self):
        invalid_ids = ("", "../escape", "nested/path", "a" * 65)
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "sandboxes"

            for mission_id in invalid_ids:
                with self.subTest(mission_id=mission_id):
                    with self.assertRaises(WorkspaceSafetyError):
                        create_sandbox(mission_id, root=root)

    def test_unmarked_existing_directory_is_preserved(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "sandboxes"
            root.mkdir()
            workspace = root / "mission_safe"
            workspace.mkdir()
            important_file = workspace / "important.txt"
            important_file.write_text("do not delete")

            with self.assertRaises(WorkspaceSafetyError):
                create_sandbox("safe", root=root)

            self.assertEqual(important_file.read_text(), "do not delete")

    def test_invalid_root_marker_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "sandboxes"
            root.mkdir()
            (root / ROOT_MARKER).write_text("owned-by-something-else\n")

            with self.assertRaises(WorkspaceSafetyError):
                create_sandbox("safe", root=root)

    def test_workspace_symlink_is_never_removed(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            root = temporary_path / "sandboxes"
            root.mkdir()
            target = temporary_path / "important"
            target.mkdir()
            important_file = target / "important.txt"
            important_file.write_text("do not delete")

            try:
                (root / "mission_safe").symlink_to(target, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("Symbolic links are unavailable on this platform.")

            with self.assertRaises(WorkspaceSafetyError):
                create_sandbox("safe", root=root)

            self.assertEqual(important_file.read_text(), "do not delete")


if __name__ == "__main__":
    unittest.main()
