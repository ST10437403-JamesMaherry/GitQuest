"""Local HTTP application for the GitQuest browser interface."""

from __future__ import annotations

import json
import logging
import mimetypes
import re
import threading
import webbrowser
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from urllib.parse import unquote, urlsplit

from gitquest import __version__
from gitquest.application.scenario_catalog import list_scenarios, load_scenario
from gitquest.application.scenario_runner import (
    ScenarioRuntimeError,
    default_scenario_workspace_root,
    scenario_workspace_name,
    start_scenario,
    verify_scenario,
)
from gitquest.domain.scenario import ScenarioManifest, ScenarioManifestError
from gitquest.reporting.incident_report import write_incident_reports
from gitquest.runtime.workspace import PathLike, WorkspaceSafetyError


LOGGER = logging.getLogger("gitquest.web")
ASSET_ROOT = Path(__file__).resolve().parents[1] / "web"
ASSET_ROUTES = {
    "/": ASSET_ROOT / "index.html",
    "/assets/app.js": ASSET_ROOT / "app.js",
    "/assets/gitquest-logo.png": ASSET_ROOT / "gitquest-logo.png",
    "/assets/styles.css": ASSET_ROOT / "styles.css",
}
MAX_REQUEST_BODY = 1024
SCENARIO_ROUTE = re.compile(r"^/api/scenarios/([^/]+)(?:/(start|verify))?$")


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


def _scenario_payload(manifest: ScenarioManifest, include_objectives: bool = True) -> dict:
    payload = {
        "id": manifest.id,
        "title": manifest.title,
        "summary": manifest.summary,
        "category": manifest.category,
        "difficulty": manifest.difficulty,
        "profile": manifest.profile,
        "total_points": manifest.total_points,
    }
    if include_objectives:
        payload["objectives"] = [
            {
                "id": objective.id,
                "title": objective.title,
                "description": objective.description,
                "points": objective.points,
            }
            for objective in manifest.objectives
        ]
    return payload


class GitQuestWebApplication:
    """Routes browser and API requests into the existing scenario services."""

    def __init__(
        self,
        scenario_root: Optional[Path] = None,
        workspace_root: Optional[PathLike] = None,
        report_root: Optional[Path] = None,
    ) -> None:
        self.scenario_root = scenario_root
        self.workspace_root = workspace_root
        self.report_root = report_root

    def _report_root(self, manifest: ScenarioManifest) -> Path:
        return self.report_root or (manifest.source_directory.parents[2] / "artifacts" / "reports")

    def _scenario(self, scenario_id: str) -> ScenarioManifest:
        return load_scenario(scenario_id, self.scenario_root)

    def dispatch(self, method: str, raw_path: str) -> WebResponse:
        """Return a response for one normalized local request."""
        path = urlsplit(raw_path).path
        if path in ASSET_ROUTES and method == "GET":
            return self._asset_response(path)
        if path == "/api/health" and method == "GET":
            return _json_response(
                200,
                {
                    "status": "ready",
                    "version": __version__,
                    "interface": "local-web",
                },
            )
        if path == "/api/scenarios" and method == "GET":
            scenarios = list_scenarios(self.scenario_root)
            return _json_response(
                200,
                {
                    "scenarios": [
                        _scenario_payload(scenario, include_objectives=False)
                        for scenario in scenarios
                    ]
                },
            )

        route = SCENARIO_ROUTE.fullmatch(path)
        if route:
            scenario_id = unquote(route.group(1))
            action = route.group(2)
            if not action and method == "GET":
                return _json_response(200, _scenario_payload(self._scenario(scenario_id)))
            if action == "start" and method == "POST":
                manifest = self._scenario(scenario_id)
                workspace = start_scenario(manifest, self.workspace_root)
                return _json_response(
                    201,
                    {
                        "scenario": _scenario_payload(manifest),
                        "workspace": str(workspace),
                        "message": "Scenario workspace initialized.",
                    },
                )
            if action == "verify" and method == "POST":
                manifest = self._scenario(scenario_id)
                result = verify_scenario(manifest, self.workspace_root)
                workspace_root = self.workspace_root or default_scenario_workspace_root(manifest)
                workspace_path = Path(workspace_root).resolve() / scenario_workspace_name(
                    manifest.id
                )
                markdown_path, json_path = write_incident_reports(
                    result,
                    output_root=self._report_root(manifest),
                )
                return _json_response(
                    200,
                    {
                        **result.to_dict(),
                        "workspace_path": str(workspace_path),
                        "reports": {
                            "markdown": str(markdown_path),
                            "json": str(json_path),
                        },
                    },
                )
            return _json_response(405, {"error": "Method not allowed for this route."})

        return _json_response(404, {"error": "Route not found."})

    def _asset_response(self, route: str) -> WebResponse:
        path = ASSET_ROUTES[route]
        try:
            body = path.read_bytes()
        except OSError as error:
            raise ScenarioRuntimeError(f"Web asset could not be loaded: {path.name}") from error
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        if content_type.startswith("text/") or content_type == "application/javascript":
            content_type += "; charset=utf-8"
        return WebResponse(status=200, body=body, content_type=content_type)


class GitQuestRequestHandler(BaseHTTPRequestHandler):
    """Security-hardened localhost request adapter."""

    server_version = "GitQuest"
    sys_version = ""

    @property
    def application(self) -> GitQuestWebApplication:
        return self.server.application  # type: ignore[attr-defined]

    def do_GET(self) -> None:
        self._handle_request("GET")

    def do_POST(self) -> None:
        if self.headers.get("X-GitQuest-Request") != "browser-ui":
            self._send_response(
                _json_response(403, {"error": "Missing local request verification header."})
            )
            return
        content_length = self.headers.get("Content-Length", "0")
        try:
            length = int(content_length)
        except ValueError:
            length = MAX_REQUEST_BODY + 1
        if length < 0 or length > MAX_REQUEST_BODY:
            self._send_response(_json_response(413, {"error": "Request body is too large."}))
            return
        if length:
            self.rfile.read(length)
        self._handle_request("POST")

    def _handle_request(self, method: str) -> None:
        host = self.headers.get("Host", "").split(":", 1)[0].strip("[]").lower()
        if host not in {"127.0.0.1", "localhost"}:
            self._send_response(
                _json_response(421, {"error": "GitQuest accepts localhost requests only."})
            )
            return
        try:
            response = self.application.dispatch(method, self.path)
        except ScenarioManifestError as error:
            status = 404 if str(error).startswith("Unknown scenario:") else 400
            response = _json_response(status, {"error": str(error)})
        except (OSError, ScenarioRuntimeError, WorkspaceSafetyError) as error:
            response = _json_response(409, {"error": str(error)})
        except Exception:
            LOGGER.exception("Unhandled GitQuest web request failure")
            response = _json_response(500, {"error": "Unexpected local server error."})
        self._send_response(response)

    def _send_response(self, response: WebResponse) -> None:
        self.send_response(response.status)
        self.send_header("Content-Type", response.content_type)
        self.send_header("Content-Length", str(len(response.body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; script-src 'self'; style-src 'self'; "
            "connect-src 'self'; img-src 'self' data:; frame-ancestors 'none'",
        )
        self.end_headers()
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
    return GitQuestHTTPServer(
        ("127.0.0.1", port),
        application or GitQuestWebApplication(),
    )


def serve_web(port: int = 8000, open_browser: bool = True) -> int:
    """Run the local browser interface until interrupted."""
    server = create_web_server(port=port)
    actual_port = server.server_address[1]
    url = f"http://127.0.0.1:{actual_port}/"
    print(f"GitQuest web console is running at {url}")
    print("Press Ctrl+C to stop it.")
    if open_browser:
        threading.Timer(0.25, webbrowser.open, args=(url,)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nGitQuest web console stopped.")
    finally:
        server.server_close()
    return 0
