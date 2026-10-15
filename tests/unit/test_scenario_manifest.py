import json
import unittest
from pathlib import Path

from gitquest.application.scenario_catalog import list_scenarios, load_scenario
from gitquest.application.scenario_runner import default_scenario_workspace_root
from gitquest.domain.scenario import ScenarioManifest, ScenarioManifestError


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SCENARIO_ROOT = REPOSITORY_ROOT / "scenarios"
MANIFEST_PATH = (
    SCENARIO_ROOT / "supply_chain" / "supply-chain-siege" / "scenario.json"
)


class ScenarioManifestTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    def test_catalog_loads_supply_chain_siege(self):
        manifest = load_scenario("supply-chain-siege", SCENARIO_ROOT)

        self.assertEqual(manifest.title, "Supply Chain Siege")
        self.assertEqual(manifest.profile, "Lite")
        self.assertEqual(manifest.total_points, 100)
        self.assertIn(manifest, list_scenarios(SCENARIO_ROOT))
        self.assertEqual(
            default_scenario_workspace_root(manifest),
            REPOSITORY_ROOT / "sandboxes" / ".gitquest",
        )

    def test_manifest_rejects_path_traversal(self):
        self.data["objectives"][0]["checks"][0]["path"] = "../outside"

        with self.assertRaises(ScenarioManifestError):
            ScenarioManifest.from_dict(self.data, MANIFEST_PATH.parent)

    def test_manifest_requires_one_hundred_total_points(self):
        self.data["objectives"][0]["points"] = 24

        with self.assertRaisesRegex(ScenarioManifestError, "total 100"):
            ScenarioManifest.from_dict(self.data, MANIFEST_PATH.parent)


if __name__ == "__main__":
    unittest.main()
