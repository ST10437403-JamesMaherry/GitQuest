import json
import tempfile
import threading
import unittest
from contextlib import contextmanager
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from gitquest.interfaces.web_app import GitQuestWebApplication, create_web_server


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SCENARIO_ROOT = REPOSITORY_ROOT / "scenarios"


@contextmanager
def running_server(application):
    server = create_web_server(port=0, application=application)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def read_json(url, request=None):
    with urlopen(request or url, timeout=5) as response:
        return response.status, dict(response.headers), json.loads(response.read())


def post_request(url):
    return Request(
        url,
        data=b"{}",
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-GitQuest-Request": "browser-ui",
        },
    )


class WebAppIntegrationTests(unittest.TestCase):
    def test_browser_and_api_routes_share_the_scenario_engine(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            application = GitQuestWebApplication(
                scenario_root=SCENARIO_ROOT,
                workspace_root=temporary_path / "workspaces",
                report_root=temporary_path / "reports",
            )

            with running_server(application) as base_url:
                with urlopen(base_url + "/", timeout=5) as response:
                    html = response.read().decode("utf-8")
                    self.assertEqual(response.status, 200)
                    self.assertIn("GitQuest Operations Console", html)
                    self.assertIn("default-src 'self'", response.headers["Content-Security-Policy"])

                status, _, health = read_json(base_url + "/api/health")
                self.assertEqual(status, 200)
                self.assertEqual(health["status"], "ready")

                _, _, catalog = read_json(base_url + "/api/scenarios")
                self.assertEqual(catalog["scenarios"][0]["id"], "supply-chain-siege")

                start_url = base_url + "/api/scenarios/supply-chain-siege/start"
                status, _, started = read_json(start_url, post_request(start_url))
                self.assertEqual(status, 201)
                self.assertTrue(Path(started["workspace"]).is_dir())

                verify_url = base_url + "/api/scenarios/supply-chain-siege/verify"
                status, _, result = read_json(verify_url, post_request(verify_url))
                self.assertEqual(status, 200)
                self.assertFalse(result["passed"])
                self.assertEqual(result["score"], 0)
                self.assertTrue(Path(result["workspace_path"]).is_dir())
                self.assertTrue(Path(result["reports"]["markdown"]).is_file())
                self.assertTrue(Path(result["reports"]["json"]).is_file())

    def test_mutating_routes_require_the_browser_verification_header(self):
        application = GitQuestWebApplication(scenario_root=SCENARIO_ROOT)
        with running_server(application) as base_url:
            request = Request(
                base_url + "/api/scenarios/supply-chain-siege/start",
                data=b"{}",
                method="POST",
                headers={"Content-Type": "application/json"},
            )
            with self.assertRaises(HTTPError) as raised:
                urlopen(request, timeout=5)

            self.assertEqual(raised.exception.code, 403)

    def test_non_local_host_header_is_rejected(self):
        application = GitQuestWebApplication(scenario_root=SCENARIO_ROOT)
        with running_server(application) as base_url:
            request = Request(
                base_url + "/api/health",
                headers={"Host": "attacker.example"},
            )
            with self.assertRaises(HTTPError) as raised:
                urlopen(request, timeout=5)

            self.assertEqual(raised.exception.code, 421)


if __name__ == "__main__":
    unittest.main()
