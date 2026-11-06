import json
import threading
import unittest
from contextlib import contextmanager
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from gitquest.interfaces.web_app import GitQuestWebApplication, create_web_server


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


def read_json(url):
    with urlopen(url, timeout=5) as response:
        return response.status, dict(response.headers), json.loads(response.read())


class WebAppIntegrationTests(unittest.TestCase):
    def test_browser_routes_and_curriculum_api(self):
        with running_server(GitQuestWebApplication()) as base_url:
            for browser_route in ("/", "/learn", "/guide"):
                with urlopen(base_url + browser_route, timeout=5) as response:
                    html = response.read().decode("utf-8")
                    self.assertEqual(response.status, 200)
                    self.assertIn("Learn Git by doing", html)
                    self.assertIn("Primary navigation", html)
                    self.assertIn("default-src 'self'", response.headers["Content-Security-Policy"])

            status, _, health = read_json(base_url + "/api/health")
            self.assertEqual(status, 200)
            self.assertEqual(health["status"], "ready")

            status, _, curriculum = read_json(base_url + "/api/curriculum")
            self.assertEqual(status, 200)
            self.assertEqual(curriculum["areas"][0]["id"], "git_basics")
            self.assertGreater(len(curriculum["areas"][0]["missions"]), 0)
            self.assertEqual(curriculum["areas"][2]["status"], "planned")

            with urlopen(base_url + "/assets/gitquest-logo.png", timeout=5) as response:
                self.assertEqual(response.headers["Content-Type"], "image/png")
                self.assertTrue(response.read().startswith(b"\x89PNG"))

    def test_head_unknown_routes_and_unsupported_methods(self):
        with running_server(GitQuestWebApplication()) as base_url:
            request = Request(base_url + "/guide", method="HEAD")
            with urlopen(request, timeout=5) as response:
                self.assertEqual(response.status, 200)
                self.assertEqual(response.read(), b"")

            with self.assertRaises(HTTPError) as missing:
                urlopen(base_url + "/missing", timeout=5)
            self.assertEqual(missing.exception.code, 404)
            self.assertIn("text/html", missing.exception.headers["Content-Type"])

            post = Request(base_url + "/api/curriculum", data=b"{}", method="POST")
            with self.assertRaises(HTTPError) as unsupported:
                urlopen(post, timeout=5)
            self.assertEqual(unsupported.exception.code, 405)

    def test_non_local_host_header_is_rejected(self):
        with running_server(GitQuestWebApplication()) as base_url:
            request = Request(base_url + "/api/health", headers={"Host": "attacker.example"})
            with self.assertRaises(HTTPError) as raised:
                urlopen(request, timeout=5)
            self.assertEqual(raised.exception.code, 421)


if __name__ == "__main__":
    unittest.main()
