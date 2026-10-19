# GitQuest project structure

```text
gitquest/
|-- pyproject.toml
|-- src/gitquest/
|   |-- application/     # Use-case orchestration
|   |-- domain/          # Pure game rules, models, and current mission catalogue
|   |-- runtime/         # Disposable workspace lifecycle
|   |-- adapters/        # Git and future security-tool integrations
|   |-- persistence/     # Progress and evidence storage
|   |-- interfaces/      # Terminal and localhost HTTP adapters
|   |-- web/             # Packaged browser UI assets
|   `-- reporting/       # Evidence and human-readable report exports
|-- scenarios/           # Versioned mission packs and fixtures
|-- policies/            # Policy-as-code used by scenarios and CI
|-- tests/               # Unit, contract, integration, and scenario tests
|-- docs/                # Architecture, ADRs, and threat models
`-- .github/workflows/   # Quality, security, scenario, release, and Pages automation
```

## Dependency direction

The domain must not import terminal UI, filesystem, subprocess, database, or scanner code.
Application services coordinate work through runtime, adapter, persistence, and interface
boundaries. External tools are wrapped by adapters so their output can later be normalized
into evidence without leaking tool-specific details across the codebase.

Both the terminal CLI and browser console call the same application services. The local HTTP
adapter owns routing and response security, while browser assets contain presentation behavior only;
neither interface reimplements scenario scoring or workspace rules.

## Transitional modules

The existing mission catalogue and JSON save system were placed in their correct long-term
boundaries but intentionally kept working. Replace them incrementally with validated scenario
manifests and versioned evidence persistence rather than attempting both migrations at once.
