"""Small local HTTP application for the GitQuest browser interface."""

from __future__ import annotations

import json
import logging
import mimetypes
import threading
import webbrowser
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from urllib.parse import urlsplit

from gitquest import __version__
from gitquest.domain.mission_map import MISSION_AREAS, get_area_missions
from gitquest.domain.missions import MISSIONS


LOGGER = logging.getLogger("gitquest.web")
ASSET_ROOT = Path(__file__).resolve().parents[1] / "web"
ASSET_ROUTES = {
    "/": ASSET_ROOT / "index.html",
    "/assets/app.js": ASSET_ROOT / "app.js",
    "/assets/gitquest-logo.png": ASSET_ROOT / "gitquest-logo.png",
    "/assets/styles.css": ASSET_ROOT / "styles.css",
}
BROWSER_ROUTES = {"/", "/learn", "/guide"}


@dataclass(frozen=True)
class WebResponse:
    """Framework-free response returned by the application router."""

    status: int
    body: bytes
    content_type: str


def _json_response(status: int, payload: Dict[str, Any]) -> WebResponse:
    return WebResponse(
        status=status,
        body=(json.dumps(payload, indent=2) + "\n").encode("utf-8"),
        content_type="application/json; charset=utf-8",
    )


def _curriculum_payload() -> dict:
    areas = []
    for area_id, area in MISSION_AREAS.items():
        missions = get_area_missions(area_id, MISSIONS)
        areas.append(
            {
                "id": area_id,
                "name": area["name"],
                "description": area["description"],
                "status": "playable" if missions else "planned",
                "missions": [
                    {
                        "id": mission["id"],
                        "title": mission["title"],
                        "command": mission["command_unlocked"],
                        "type": mission.get("mission_type", "quiz"),
                    }
                    for mission in missions
                ],
            }
        )
    return {"areas": areas}


class GitQuestWebApplication:
    """Serve static pages and a read-only view of the current curriculum."""

    def dispatch(self, method: str, raw_path: str) -> WebResponse:
        """Return a response for one normalized local request."""
        path = urlsplit(raw_path).path
        if path in ASSET_ROUTES and method == "GET":
            return self._asset_response(path)
        if method == "GET" and path in BROWSER_ROUTES:
            return self._asset_response("/")
        if path == "/api/health" and method == "GET":
            return _json_response(
                200,
                {"status": "ready", "version": __version__, "interface": "local-web"},
            )
        if path == "/api/curriculum" and method == "GET":
            return _json_response(200, _curriculum_payload())
        if method != "GET":
            return _json_response(405, {"error": "Method not allowed."})
        if not path.startswith(("/api/", "/assets/")):
            return self._asset_response("/", status=404)
        return _json_response(404, {"error": "Route not found."})

    def _asset_response(self, route: str, status: int = 200) -> WebResponse:
        path = ASSET_ROUTES[route]
        body = path.read_bytes()
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        if content_type.startswith("text/") or content_type == "application/javascript":
            content_type += "; charset=utf-8"
        return WebResponse(status=status, body=body, content_type=content_type)


class GitQuestRequestHandler(BaseHTTPRequestHandler):
    """Localhost-only HTTP adapter."""

    server_version = "GitQuest"
    sys_version = ""

    @property
    def application(self) -> GitQuestWebApplication:
        return self.server.application  # type: ignore[attr-defined]

    def do_GET(self) -> None:
        self._handle_request("GET")

    def do_HEAD(self) -> None:
        self._handle_request("GET", include_body=False)

    def do_POST(self) -> None:
        self._handle_request("POST")

    def _handle_request(self, method: str, include_body: bool = True) -> None:
        host = self.headers.get("Host", "").split(":", 1)[0].strip("[]").lower()
        if host not in {"127.0.0.1", "localhost"}:
            response = _json_response(421, {"error": "GitQuest accepts localhost requests only."})
        else:
            try:
                response = self.application.dispatch(method, self.path)
            except OSError:
                LOGGER.exception("GitQuest web asset failure")
                response = _json_response(500, {"error": "The browser interface could not load."})
            except Exception:
                LOGGER.exception("Unhandled GitQuest web request failure")
                response = _json_response(500, {"error": "Unexpected local server error."})
        self._send_response(response, include_body=include_body)

    def _send_response(self, response: WebResponse, include_body: bool = True) -> None:
        self.send_response(response.status)
        self.send_header("Content-Type", response.content_type)
        self.send_header("Content-Length", str(len(response.body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Resource-Policy", "same-origin")
        self.send_header(
            "Permissions-Policy",
            "camera=(), geolocation=(), microphone=(), payment=(), usb=()",
        )
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; script-src 'self'; style-src 'self'; "
            "connect-src 'self'; img-src 'self' data:; object-src 'none'; "
            "base-uri 'none'; form-action 'none'; frame-ancestors 'none'",
        )
        self.end_headers()
        if include_body:
            self.wfile.write(response.body)

    def log_message(self, format_string: str, *args: object) -> None:
        LOGGER.info("%s - %s", self.client_address[0], format_string % args)


class GitQuestHTTPServer(ThreadingHTTPServer):
    """HTTP server carrying the framework-free application instance."""

    daemon_threads = True

    def __init__(
        self,
        server_address: Tuple[str, int],
        application: GitQuestWebApplication,
    ) -> None:
        self.application = application
        super().__init__(server_address, GitQuestRequestHandler)


def create_web_server(
    port: int = 8000,
    application: Optional[GitQuestWebApplication] = None,
) -> GitQuestHTTPServer:
    """Create a localhost-only server. Port zero selects an ephemeral test port."""
    if not 0 <= port <= 65535:
        raise ValueError("Port must be between 0 and 65535.")
    return GitQuestHTTPServer(("127.0.0.1", port), application or GitQuestWebApplication())


def serve_web(port: int = 8000, open_browser: bool = True) -> int:
    """Run the local browser interface until interrupted."""
    server = create_web_server(port=port)
    actual_port = server.server_address[1]
    url = f"http://127.0.0.1:{actual_port}/"
    print(f"GitQuest is running at {url}")
    print("Press Ctrl+C to stop it.")
    if open_browser:
        threading.Timer(0.25, webbrowser.open, args=(url,)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nGitQuest stopped.")
    finally:
        server.server_close()
    return 0
