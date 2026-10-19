<p align="center">
  <img src="./GitQuest%20Mountain%20Commit%20Logo.png" alt="GitQuest" width="520">
</p>

# GitQuest

**Break it. Fix it. Prove it.**

GitQuest is a free, local-first DevSecOps incident simulator. Players inherit a compromised
repository, investigate the failure, repair the delivery controls, and generate evidence that shows
what changed and why the incident is contained.

The project is deliberately more than a command quiz. New scenarios are scored from real repository
state so a successful result can be inspected, repeated, and discussed in a portfolio interview.

## Why this project stands out

- **Real remediation:** players work in disposable Git repositories instead of selecting answers.
- **Evidence-backed scoring:** objectives total 100 points and produce Markdown plus JSON reports.
- **Security-conscious runtime:** managed workspaces use safety markers, path containment, and
  symlink defenses.
- **Two interfaces, one engine:** the terminal and browser console call the same application
  services.
- **Zero required cloud cost:** the Lite campaign needs only Python and Git and runs locally.
- **Portfolio-grade delivery:** automated tests, linting, package builds, pinned GitHub Actions, and
  Dependabot are part of the product story.

## Current release: v0.4

The current playable vertical slice is **Supply Chain Siege**. It seeds an intentionally unsafe,
offline repository and asks the player to:

1. remove an exposed fake credential from the current tree;
2. pin a third-party workflow action to an immutable commit;
3. harden the release script against unsafe shell execution; and
4. create a remediation commit that records the response.

Verification scores the resulting repository and writes portfolio-safe reports without copying
secret values or file contents.

### Implemented

- Legacy Git learning campaign with XP, levels, quizzes, and sandbox missions
- Capability diagnostics through Lite, Standard, and Full runtime profiles
- Validated, versioned JSON scenario manifests
- Safety-marked disposable scenario workspaces
- Deterministic Git and file-state checks
- Supply Chain Siege incident scenario
- Markdown and JSON incident evidence reports
- Terminal workflow and localhost-only browser console
- Monochrome, responsive browser interface using the GitQuest logo
- Unit and integration test suite
- Make-based local workflow
- GitHub Actions CI and weekly Dependabot updates

## Quick start

### Requirements

- Python 3.9 or newer
- Git
- GNU Make for the shortcut commands (preinstalled on macOS and most Linux systems)

No cloud account, payment method, Node.js toolchain, container runtime, or external API is required
for the current Lite scenario.

### First-time setup on macOS or Linux

Clone the repository, create one virtual environment, activate it, and install the application with
its development tools:

    git clone https://github.com/ST10437403-JamesMaherry/GitQuest.git
    cd GitQuest
    python3 -m venv .venv
    source .venv/bin/activate
    make install-dev PYTHON=python

Confirm that the installation works:

    gitquest --version
    make doctor PYTHON=python

The installation step is normally required only after cloning, after deleting the virtual
environment, or after pulling changes to the dependencies in <code>pyproject.toml</code>.

### First-time setup on Windows PowerShell

Create and activate the environment, then install the project:

    git clone https://github.com/ST10437403-JamesMaherry/GitQuest.git
    cd GitQuest
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    python -m pip install -e ".[dev]"

Confirm that the installation works:

    gitquest --version
    python -m gitquest doctor

GNU Make is optional on Windows. The direct <code>python -m gitquest</code> commands work from
PowerShell; Make can also be used from WSL or Git Bash.

### Every time you return to the project

Open a terminal in the repository and reactivate the same virtual environment.

On macOS or Linux:

    cd /path/to/GitQuest
    source .venv/bin/activate

On Windows PowerShell:

    cd C:\path\to\GitQuest
    .venv\Scripts\Activate.ps1

You should now see <code>(.venv)</code> at the beginning of the terminal prompt.

### Start the browser game

With the virtual environment active:

    make web PYTHON=python

GitQuest opens <http://127.0.0.1:8000/>. If it does not open automatically, visit that address
manually. Use another port when 8000 is occupied:

    make web PYTHON=python PORT=8765

Stop the server with <kbd>Ctrl</kbd>+<kbd>C</kbd>.

Without Make, use:

    python -m gitquest web
    python -m gitquest web --port 8765
    python -m gitquest web --no-open

### Start the terminal game

With Make:

    make run PYTHON=python

Without Make:

    python -m gitquest play

The installed console command is equivalent:

    gitquest play

### Minimal installation for players

If you only want to play and do not need Ruff, pytest, or the packaging tools:

    python -m pip install -e .
    python -m gitquest web

## Play Supply Chain Siege

Check the local runtime and inspect the available scenarios:

    make doctor PYTHON=python
    make scenarios PYTHON=python

Create a fresh incident workspace:

    make scenario-start PYTHON=python

GitQuest prints the managed workspace path. Read its <code>INCIDENT.md</code>, investigate the
repository, make the remediation, and verify it:

    make scenario-verify PYTHON=python

The default scenario can be overridden:

    make scenario-start PYTHON=python SCENARIO=another-scenario-id

Starting a scenario again resets only its GitQuest-marked workspace. Personal repositories and
unmarked directories are rejected by the cleanup guard.

Generated incident reports are written beneath:

    artifacts/reports/

Generated practice repositories are written beneath:

    sandboxes/.gitquest/

Both locations are ignored by Git.

## Complete local workflow

A typical development or portfolio-demo session is:

    source .venv/bin/activate
    make doctor PYTHON=python
    make scenarios PYTHON=python
    make scenario-start PYTHON=python
    make web PYTHON=python

After editing the generated incident repository, stop the browser server if necessary and verify the
remediation:

    make scenario-verify PYTHON=python

Before committing project changes, run:

    make ci PYTHON=python

Then inspect exactly what will be committed:

    git status
    git diff

## Make commands

Run <code>make</code> or <code>make help</code> to see the local workflow.

| Command | Purpose |
| --- | --- |
| <code>make install</code> | Install the application into the active Python environment |
| <code>make install-dev</code> | Install the app plus free testing, linting, and build tools |
| <code>make run</code> | Start the terminal campaign |
| <code>make web</code> | Start the localhost browser console |
| <code>make doctor</code> | Display local runtime capabilities |
| <code>make scenarios</code> | List scenario packs |
| <code>make scenario-start</code> | Initialize the selected incident |
| <code>make scenario-verify</code> | Score the selected remediation |
| <code>make test</code> | Run the dependency-free unittest suite |
| <code>make lint</code> | Run Ruff static checks |
| <code>make format-check</code> | Check Python formatting |
| <code>make build</code> | Build the source and wheel distributions |
| <code>make ci</code> | Run the complete local CI quality gate |

<code>PYTHON</code>, <code>PORT</code>, and <code>SCENARIO</code> are overridable Make variables. If
your virtual environment is activated, use <code>PYTHON=python</code> as shown above.

## Command-line reference

    gitquest                         Start the legacy terminal campaign
    gitquest play                    Start the legacy terminal campaign explicitly
    gitquest doctor                  Show runtime capability checks
    gitquest doctor --json           Emit machine-readable diagnostics
    gitquest scenario list           List installed incident scenarios
    gitquest scenario start ID       Create or reset a managed scenario workspace
    gitquest scenario verify ID      Score a remediation and write reports
    gitquest scenario verify ID --json
                                     Emit the verification result as JSON
    gitquest web                     Start the browser console on port 8000
    gitquest web --port 8765         Use a different local port
    gitquest web --no-open           Do not open a browser automatically

## Architecture

    Browser console --+
                      +--> application services --> domain rules
    Terminal CLI -----+             |
                                    +--> managed workspace runtime
                                    +--> Git and tool adapters
                                    +--> evidence reporting

The domain contains scenario and scoring rules but does not know about HTTP, Rich, subprocesses, or
filesystem cleanup. Both interfaces reuse the same catalog, runtime, verifier, and reporting
services.

    gitquest/
    |-- Makefile                    # Local developer and player shortcuts
    |-- pyproject.toml              # Package metadata and dependency policy
    |-- src/gitquest/
    |   |-- application/            # Use cases and orchestration
    |   |-- domain/                 # Pure mission, scenario, and scoring rules
    |   |-- runtime/                # Safe disposable workspace lifecycle
    |   |-- adapters/               # Git and future security-tool integrations
    |   |-- persistence/            # Local player progress
    |   |-- reporting/              # Evidence report generation
    |   |-- interfaces/             # Terminal and localhost HTTP adapters
    |   +-- web/                    # Dependency-free browser assets
    |-- scenarios/                  # Versioned incident packs and fixtures
    |-- policies/                   # Future policy-as-code controls
    |-- tests/                      # Unit, contract, integration, scenario tests
    |-- docs/                       # Architecture, decisions, threats, roadmap
    |-- .github/workflows/ci.yml    # Read-only CI quality gate
    |-- .github/dependabot.yml      # Python and Actions update policy
    |-- artifacts/                  # Generated evidence; ignored by Git
    +-- sandboxes/                  # Generated practice repositories; ignored by Git

More detail is available in
[docs/architecture/project-structure.md](docs/architecture/project-structure.md).

## Security model

GitQuest intentionally handles disposable repositories, so safe execution is a product feature:

- the HTTP server binds to <code>127.0.0.1</code> and rejects unexpected Host headers;
- mutating browser requests require a custom local verification header;
- static assets are local and the Content Security Policy blocks third-party execution;
- dynamic browser content is inserted through text APIs rather than HTML injection;
- scenario IDs, manifest paths, regexes, and objective totals are validated;
- workspaces must remain beneath a managed root and carry a GitQuest safety marker;
- symlinked workspace or fixture entries are rejected;
- Git commands use argument arrays, timeouts, captured output, and disabled prompts;
- fixtures contain only inert, explicitly fake credentials; and
- evidence reports record normalized outcomes, not credential values or source contents.

This development server is not a multi-user service and must not be exposed to a network.

See [the browser threat model](docs/threat-model/browser-interface.md) and
[the runtime threat model](docs/threat-model/scenario-runtime.md).

## Quality and dependency automation

GitHub Actions runs <code>make ci</code> on pushes to <code>main</code>, pull requests, and manual
dispatches. The job tests Python 3.9 and 3.13, uses read-only repository permissions, disables
persisted checkout credentials, applies a ten-minute timeout, and pins actions to full commit SHAs.

Dependabot checks the Python and GitHub Actions ecosystems every Monday. Production Python
dependencies, development dependencies, and Actions updates are grouped separately so changes stay
reviewable. Dependabot opens pull requests; it does not merge or deploy anything automatically.

Run the same gate locally before committing:

    make ci PYTHON=python

## Troubleshooting

### The <code>gitquest</code> command is not found

Activate the virtual environment and reinstall the project from the repository root:

    source .venv/bin/activate
    python -m pip install -e .

You can always bypass the console entry point with:

    python -m gitquest web

On Windows, activate with <code>.venv\Scripts\Activate.ps1</code> instead.

### Pip says that <code>-e</code> requires an argument

Editable installation needs the current-directory argument:

    python -m pip install -e .

Do not omit the final period.

### Python reports <code>No module named python</code>

Use Python once before <code>-m</code>:

    python -m pip install -e .

Do not run <code>python -m python -m pip</code>.

### Pip cannot install the editable project

Upgrade pip inside the active virtual environment, then retry:

    python -m pip install --upgrade pip
    python -m pip install -e ".[dev]"

Also confirm that the command is being run from the directory containing
<code>pyproject.toml</code>.

### Port 8000 is already in use

Choose another local port:

    make web PYTHON=python PORT=8765

Or:

    python -m gitquest web --port 8765

### Scenario verification cannot find a workspace

Initialize the scenario before verifying it:

    make scenario-start PYTHON=python
    make scenario-verify PYTHON=python

### Tests fail while binding a localhost port

The browser integration tests require permission to open an ephemeral loopback socket. Run them in a
normal local terminal rather than a restricted sandbox:

    make test PYTHON=python

## Product roadmap

### Now: trustworthy Lite foundation

- [x] Safe managed workspaces and runtime diagnostics
- [x] Data-driven scenario manifests and deterministic scoring
- [x] First end-to-end supply-chain incident
- [x] Markdown and JSON evidence
- [x] Terminal and browser delivery
- [x] Local/CI parity through Make
- [x] CI and dependency update automation

### Next: deeper evidence and progression

- [ ] Persist scenario attempts, scores, and evidence metadata in SQLite
- [ ] Connect incident scenarios to a unified campaign and skill progression model
- [ ] Add hint tiers, debriefs, prerequisites, and estimated completion time to manifests
- [ ] Add evidence browsing and export actions to the browser console
- [ ] Add keyboard/browser end-to-end and accessibility checks
- [ ] Publish a sample sanitized report for recruiters who do not install the project

### Then: DevSecOps breadth

- [ ] Add a Gitleaks adapter and deterministic secret-history scenario
- [ ] Add CI workflow policy checks and a Pipeline Fortress campaign
- [ ] Add SBOM and dependency-risk evidence
- [ ] Add rootless container build, scan, and signing missions
- [ ] Add OpenTofu and policy-as-code scenarios
- [ ] Add an optional local Kubernetes capstone using kind

### Explicitly out of scope for v1

- Paid cloud resources or required cloud accounts
- A hosted service that executes untrusted player code
- Real malware, real credentials, or live production targets
- Multi-user accounts, leaderboards, or social features
- More command trivia without a verifiable operational outcome

The detailed sequencing and release criteria live in [docs/roadmap.md](docs/roadmap.md).

## Free-tool policy

The core campaign must stay usable after installation without a payment method. Optional later
profiles may integrate free, open-source tools such as Gitleaks, Trivy, Conftest, Podman, OpenTofu,
Cosign, kubectl, and kind. Missing optional tools disable only the related scenarios and should
never block the Lite campaign.

GitHub-hosted automation is a repository convenience, not a runtime dependency. Every important
quality check also has a local Make target.

## Author

Built by **James Maherry** as a portfolio project focused on cloud engineering, cybersecurity, and
DevSecOps.
