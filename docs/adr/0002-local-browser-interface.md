# ADR 0002: Local browser interface over shared learning services

- **Status:** Accepted
- **Date:** 2026-10-19
- **Revised:** 2026-11-05

## Context

GitQuest began as a terminal game, but a visual interface can make repository state and GitHub web
workflows easier to understand. A separate browser game engine would create inconsistent lesson
rules. A hosted service would add cost, accounts, and operational scope before the learning product
is proven.

## Decision

GitQuest uses the localhost browser interface as its default entry point through `gitquest`,
`python -m gitquest`, or `make start`. Python serves packaged HTML, CSS, and JavaScript without a
Node.js build or remote CDN. The terminal campaign remains available explicitly through
`gitquest play`. Both interfaces will eventually use shared application lesson services and
validators.

At the reset baseline the browser is read-only. Interactive routes may be added only after the game
engine is separated from terminal input and repository mutations are expressed as typed,
allow-listed operations.

## Consequences

- The product remains free, offline-capable, and simple to install.
- Curriculum and visual state can be shared without duplicating correctness rules.
- Localhost is the only supported deployment boundary for now.
- A future hosted version would require a separate authentication and isolation design.
