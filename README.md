<p align="center">
  <img src="./GitQuest%20Mountain%20Commit%20Logo.png" alt="GitQuest" width="520">
</p>

# GitQuest

**Learn Git by doing.**

GitQuest is a free, local-first learning game for Git and GitHub. It combines clear explanations,
guided challenges, and disposable repositories so learners can build a real mental model instead of
memorising commands.

This repository is currently at a deliberate product reset. The terminal campaign is playable; the
browser presents the curriculum and project direction. Interactive browser labs and GitHub workflow
simulations will be built in small, reviewable increments listed in
[`docs/execution-plan.md`](docs/execution-plan.md).

## Product promise

GitQuest will teach three connected skills:

1. **Git concepts** — working tree, staging area, commits, branches, merge bases, remotes, and refs.
2. **Git command-line practice** — real commands inside safe, generated repositories.
3. **GitHub workflows** — repositories, issues, pull requests, reviews, forks, releases, and common
   collaboration patterns in a guided web simulation.

The core game will remain free. It needs no paid API, cloud account, telemetry service, remote font,
or commercial dependency.

## What works now

- A terminal campaign with XP, levels, quizzes, and saved progress
- Real sandbox missions for repository initialization, commits, and branches
- A local browser curriculum at `/`, `/learn`, and `/guide`
- A read-only curriculum API at `/api/curriculum`
- Local environment diagnostics with `gitquest doctor`
- A monochrome, responsive, keyboard-friendly interface
- Unit and integration tests, Ruff checks, package builds, CI, and Dependabot

## Requirements

- Python 3.9 or newer
- Git
- GNU Make on macOS/Linux for the shortcut commands (optional)

## First-time setup

### macOS or Linux

```bash
git clone https://github.com/ST10437403-JamesMaherry/GitQuest.git
cd GitQuest
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
make install-dev PYTHON=python
```

Confirm the install:

```bash
gitquest --version
gitquest doctor
```

### Windows PowerShell

```powershell
git clone https://github.com/ST10437403-JamesMaherry/GitQuest.git
cd GitQuest
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Confirm the install:

```powershell
gitquest --version
gitquest doctor
```

## Every time you return

Activate the same environment; you do not need to reinstall on every run.

macOS or Linux:

```bash
cd /path/to/GitQuest
source .venv/bin/activate
```

Windows PowerShell:

```powershell
cd C:\path\to\GitQuest
.venv\Scripts\Activate.ps1
```

## Run GitQuest

Start the browser-based experience with one command:

```bash
make start
```

GitQuest opens [http://127.0.0.1:8000](http://127.0.0.1:8000). Stop the local server with
`Ctrl+C`. The installed command and Python module use the browser by default:

```bash
gitquest
python -m gitquest
```

Use another port when 8000 is occupied:

```bash
make start PORT=8765
python -m gitquest web --port 8765 --no-open
```

The original terminal campaign remains available while its gameplay services are moved behind the
browser interface:

```bash
make run PYTHON=python
gitquest play
python -m gitquest play
```

## Development workflow

Run the same quality gate used by CI:

```bash
make ci PYTHON=python
```

Focused commands:

| Command | Purpose |
| --- | --- |
| `make install` | Install the player application |
| `make install-dev` | Install the app and free development tools |
| `make start` | Start the browser-based GitQuest experience |
| `make run` | Start the terminal campaign |
| `make web` | Alias for `make start` |
| `make doctor` | Check Python, Git, and workspace readiness |
| `make test` | Run the test suite |
| `make lint` | Run Ruff static checks |
| `make format-check` | Check formatting without changing files |
| `make build` | Build the wheel and source distribution |
| `make ci` | Run lint, format, tests, and build |

## Safety

Some future lessons will teach destructive or history-rewriting commands. GitQuest must execute
those commands only inside marked disposable workspaces. Never point a GitQuest exercise at a
personal or work repository.

## Project documentation

- [Execution plan](docs/execution-plan.md) — the proposed sequence of 100 small commits
- [Roadmap](docs/roadmap.md) — product phases and release outcomes
- [Architecture](docs/architecture/project-structure.md) — current boundaries and target shape
- [Development guide](docs/development.md) — local workflow and contribution rules
- [Browser threat model](docs/threat-model/browser-interface.md) — local interface security boundary

## License

GitQuest is released under the [MIT License](LICENSE).
