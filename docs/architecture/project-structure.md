# Project structure

GitQuest uses a small layered Python architecture. The terminal and browser are interfaces over the
same learning concepts; Git operations and filesystem work stay behind adapters and managed runtime
boundaries.

```text
gitquest/
├── .github/                 # CI and dependency updates
├── data/                    # ignored local player progress
├── docs/                    # architecture, roadmap, and execution plan
├── src/gitquest/
│   ├── adapters/            # Git and system process boundaries
│   ├── application/         # game orchestration and diagnostics
│   ├── domain/              # missions, answers, players, and map rules
│   ├── interfaces/          # terminal UI and localhost HTTP adapter
│   ├── persistence/         # local progress storage
│   ├── runtime/             # marked disposable workspaces
│   └── web/                 # packaged HTML, CSS, JavaScript, and logo
└── tests/                   # unit and local integration tests
```

## Current request flow

```text
Terminal -> GameEngine -> mission rules -> Git adapter / workspace -> JSON progress
Browser  -> local HTTP -> curriculum data -> packaged static interface
```

The browser is intentionally read-only at the reset baseline. It must not grow a second gameplay
engine. The next architecture step is to extract lesson execution from the terminal `GameEngine`
into application services that both interfaces can call.

## Dependency rules

- Domain code does not import terminal, HTTP, filesystem, subprocess, or persistence code.
- Application services coordinate domain rules and explicit ports.
- Adapters are the only place that execute Git or inspect system tools.
- Interfaces translate input and output; they do not decide whether a lesson passed.
- Runtime code creates only marked, contained, disposable repositories.
- Persistence is local and replaceable; lesson correctness never depends on analytics.

## Target gameplay boundary

The browser will submit a typed action such as `stage_file` or `create_branch`, not an arbitrary
shell string. An application service will map that action to an allow-listed Git adapter operation,
then a validator will inspect repository state. This keeps lessons authentic without turning the
local HTTP process into a general command-execution server.
