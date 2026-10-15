# ADR 0001: Data-driven security scenarios

- **Status:** Accepted
- **Date:** 2026-10-15

## Context

The original GitQuest missions are Python dictionaries interpreted by a large interactive engine.
That works for command quizzes, but it makes security labs difficult to review, test, version, and
extend. A portfolio-grade DevSecOps simulator also needs reproducible vulnerable states and
evidence that does not depend on a human claiming the task was completed.

## Decision

Security scenarios live under `scenarios/<category>/<scenario-id>/`. Each pack contains a versioned
JSON manifest and an offline fixture. The application validates manifests into immutable domain
objects before creating a safety-marked disposable Git repository.

Objectives contain declarative checks and must total 100 points. Application services evaluate the
checks and normalize the outcome before the reporting layer writes Markdown and JSON. Reports store
commit identifiers and check results, but never copy candidate secret values or file contents.

The first scenario uses the Lite runtime profile so it requires only Python and Git. Later adapters
may supply normalized evidence from free tools such as Gitleaks, Trivy, Conftest, and Cosign without
coupling their raw output to the scenario domain.

## Consequences

- New scenario content can be reviewed separately from the engine.
- The same manifest drives terminal instructions, automated scoring, tests, and evidence reports.
- Fixtures and checks require strict validation because they cross filesystem and regex boundaries.
- The manifest format is intentionally small; new check types require application code and tests.
- Legacy quiz missions remain supported and can be migrated gradually.
