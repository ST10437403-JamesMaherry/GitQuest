# GitQuest product roadmap

## Product promise

GitQuest is a local-first DevSecOps incident simulator:

> Break it. Fix it. Prove it.

The player receives an intentionally compromised, disposable repository. They investigate the
incident, repair the delivery controls, run deterministic verification, and leave with evidence that
can be reviewed in a portfolio interview.

Every planned feature must strengthen at least one part of that loop. Features that only add
command trivia, decorative gamification, or cloud cost do not belong in the v1 scope.

## Current baseline: v0.4

| Capability | Status | Evidence in the repository |
| --- | --- | --- |
| Installable Python CLI | Complete | pyproject metadata and the gitquest entry point |
| Safe disposable runtime | Complete | marked workspaces, path containment, symlink rejection |
| Runtime capability profiles | Complete | Lite, Standard, and Full doctor checks |
| Data-driven scenario engine | Complete | validated JSON manifests and declarative checks |
| First security incident | Complete | Supply Chain Siege |
| Deterministic scoring | Complete | objective results totaling 100 points |
| Portfolio evidence | Complete | Markdown and JSON incident reports |
| Terminal delivery | Complete | scenario CLI and legacy learning campaign |
| Browser delivery | Complete | localhost-only incident console |
| Local quality workflow | Complete | Make targets for tests, lint, format, and builds |
| Hosted quality workflow | Complete | GitHub Actions across Python 3.9 and 3.13 |
| Dependency maintenance | Complete | weekly Dependabot checks for Python and Actions |

## v0.5: attempts and evidence

**Goal:** turn one-off verification into a progression system that proves repeatable performance.

- Store attempts, scenario versions, timestamps, scores, and evidence paths in SQLite.
- Introduce a small migration mechanism and repository abstraction.
- Add an attempt history screen to the browser console.
- Add safe report viewing and download routes that never accept arbitrary paths.
- Hash generated evidence and include the Git commit identifier in every attempt.
- Add report-schema tests and a sanitized sample report to the repository.

**Exit criteria**

- A player can complete the same scenario twice and compare both results.
- Deleting local reports does not corrupt progress history.
- A browser route cannot read a path outside the internally generated report index.
- The sample report contains no machine-specific absolute paths.

## v0.6: campaign progression

**Goal:** connect the legacy game personality to the evidence-driven incident engine.

- Replace separate quiz and scenario navigation with a single campaign catalog.
- Add prerequisites, estimated duration, skill tags, hint tiers, and debriefs to manifests.
- Award progression for verified objectives, not typed command text.
- Define stable XP and level semantics, including save migration.
- Add a campaign map that shows locked, ready, active, and completed scenarios without relying on
  color alone.

**Exit criteria**

- A new player understands what to do without reading source code.
- Progress survives application upgrades through a tested migration.
- Every new mission grades final system state.

## v0.7: Pipeline Fortress

**Goal:** demonstrate CI/CD hardening as a playable security track.

- Add a workflow parser or narrowly scoped policy checks.
- Detect mutable action references, excessive permissions, unsafe pull request triggers, untrusted
  script interpolation, and persisted credentials.
- Seed known failing and passing workflow fixtures.
- Map each objective to a concise explanation and remediation reference.
- Dogfood the same controls against GitQuest's own CI workflow.

**Exit criteria**

- At least three deterministic pipeline incidents run in the Lite profile.
- The checks do not execute workflow content.
- GitQuest's own workflow passes the controls it teaches.

## v0.8: open-source scanner adapters

**Goal:** add credible security tooling without making live data the grading source.

- Define a typed adapter contract covering success, findings, timeout, missing tool, and parse error.
- Add Gitleaks for secret-history investigation.
- Add Trivy filesystem scanning for dependency and configuration context.
- Keep deterministic fixtures as the score source; label live scanner output as enrichment.
- Cap execution time and captured output, and scrub inherited credential variables.

**Exit criteria**

- Missing tools disable only their related scenarios.
- Contract tests normalize tool-version differences.
- A reviewer can complete the entire Lite foundation without downloads after installation.

## v0.9: artifacts and containers

**Goal:** extend proof from source state to release artifacts.

- Generate a CycloneDX SBOM.
- Build an OCI image with rootless Podman.
- Verify non-root execution, minimal capabilities, and a read-only filesystem where practical.
- Scan the image with Trivy.
- Sign a local artifact with Cosign and verify its identity.
- Link the SBOM, scan, signature, and image digest in one evidence record.

**Exit criteria**

- Standard-profile missions skip clearly when Podman is unavailable.
- No scenario mounts a host container socket or requests privileged execution.
- Every reported artifact names the same digest.

## v1.0: Operation Nightfall

**Goal:** ship one memorable capstone across Git, CI, artifacts, policy, and local deployment.

The capstone combines a leaked fake secret, mutable CI dependency, unsafe release step, vulnerable
dependency fixture, weak container posture, and policy-violating deployment manifest. The player
must contain the incident and generate a coherent evidence bundle.

Optional Full-profile work may add:

- OpenTofu validation;
- Conftest policy checks;
- a one-node kind cluster;
- Kubernetes workload hardening; and
- local deployment verification.

**Release criteria**

- A clean-machine Lite setup takes less than ten minutes.
- Pull-request CI stays below ten minutes.
- Every scenario has known failing and passing fixtures.
- All path, symlink, subprocess, and browser security tests pass.
- Another person can complete the onboarding path without developer assistance.
- The release includes a wheel, source distribution, checksums, sample evidence, architecture
  documentation, threat models, and a short demo.

## Zero-cost guardrails

- No required commercial cloud account, credit card, paid API, or long-running hosted service.
- Core verification must run locally through the same Make targets used in CI.
- Hosted automation is limited to standard GitHub features and can be disabled without breaking the
  game.
- Optional tools must be free and open source.
- Optional profiles may never block the Lite campaign.
- No default workflow provisions infrastructure or deploys to a commercial cloud.

## Deliberate non-goals

- Hosted execution of player-controlled code
- Multi-user accounts and public leaderboards
- Real credentials, real malware, or production targets
- Broad cloud-provider wrappers without a playable security outcome
- Large scenario counts at the expense of deterministic tests and clear debriefs

## Portfolio proof checklist

A strong public release should let a reviewer find these artifacts quickly:

- a 30-second README explanation;
- a 90-second incident demo;
- one architecture diagram;
- one browser and one terminal screenshot;
- the scenario manifest and known-state tests;
- a sanitized Markdown evidence report;
- CI with pinned actions and least privilege;
- threat models and ADRs;
- measured setup time, test count, and CI duration; and
- honest limitations and next decisions.

Do not claim integrations, security coverage, performance, or user results until they are implemented
and measured.
