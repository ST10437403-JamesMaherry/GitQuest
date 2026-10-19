# ADR 0002: Local browser interface over shared application services

- **Status:** Accepted
- **Date:** 2026-10-19

## Context

GitQuest began as a terminal game, but the portfolio goal requires a visual experience that can
communicate incident state, scoring, and evidence to people who are not already using the CLI. A
second implementation of scenario logic would create inconsistent scoring and double the security
surface. A hosted service would also conflict with the free, local-first constraint.

## Decision

GitQuest provides a localhost-only browser interface through `gitquest web`. A Python
standard-library HTTP adapter calls the existing scenario catalog, workspace runtime, verifier, and
reporting services. Static HTML, CSS, and JavaScript are packaged with the Python distribution and
need no Node.js toolchain or remote CDN.

The product interface uses a high-contrast monochrome system and the packaged GitQuest logo.
Status is communicated with text and shape rather than color alone, and keyboard focus remains
visible at every interactive control.

The initial API supports health checks, scenario discovery, scenario detail, lab initialization,
and remediation verification. Terminal and browser interactions therefore produce the same Git
state, scores, and evidence reports.

## Security controls

- The server binds to `127.0.0.1` and rejects non-local Host headers.
- Mutating requests require a custom verification header, which prevents cross-origin simple-form
  requests from resetting a workspace.
- Responses use a restrictive Content Security Policy and deny framing.
- Browser code inserts scenario data with DOM text APIs instead of HTML injection.
- Request bodies are bounded and routes never accept arbitrary filesystem paths.
- No telemetry, remote fonts, analytics, CDNs, or third-party scripts are loaded.

## Consequences

- The project now demonstrates interface separation and local API design in addition to CLI design.
- The browser console remains free and works offline.
- Localhost is the deployment boundary for this phase; remote multi-user hosting would require
  authentication, authorization, CSRF tokens, persistence isolation, and a production web server.
- HTTP integration tests require permission to bind an ephemeral loopback port.
