# GitQuest: The Version Control Adventure

**GitQuest** is a terminal-based Python learning game that helps developers practice Git commands in a fun, interactive, and story-driven way.

Players complete missions, unlock commands, earn XP, level up, explore mission areas, and complete real Git challenges inside sandbox folders.

This project is being built as both a learning tool and a portfolio project.

---

## Current Features

* Terminal-based gameplay
* Rich terminal UI with styled menus, panels, and tables
* Player name creation
* XP and leveling system
* Mission map with different learning areas
* Git command quiz missions
* Flexible answer checking for realistic Git commands
* Real Git sandbox missions
* Safety-marked disposable mission workspaces
* `gitquest doctor` capability diagnostics
* Lite, Standard, and Full runtime profiles for gradual DevSecOps expansion
* Data-driven security scenario packs with declarative scoring
* Supply Chain Siege incident-response scenario
* Markdown and JSON evidence reports for portfolio demonstrations
* Local JSON save system
* Unlockable Git commands
* `.gitignore` for virtual environments, cache files, save data, and sandbox folders

---

## Mission Areas

Current and planned mission areas include:

* Git Basics
* Branching Forest
* Merge Conflict Dungeon
* Remote Repository Citadel

Some areas may be locked until the player reaches a higher level.

---

## Real Git Sandbox Challenges

GitQuest includes sandbox missions where the game creates a temporary practice folder.

The player then runs real Git commands inside that folder.

Example:

```bash
git init
```

The game checks the sandbox folder to confirm whether the task was completed successfully.

Sandbox folders are created locally inside a dedicated managed directory:

```text
sandboxes/.gitquest/
```

GitQuest only resets workspaces containing its own safety marker. It refuses path traversal,
symbolic-link workspaces, and unmarked directories. The entire `sandboxes/` folder is ignored by
Git so practice repositories are not pushed to GitHub.

---

## Planned Features

Future improvements include:

* More real Git sandbox missions
* Create your first commit challenge
* Branch creation challenges
* Merge conflict missions
* Remote repository and GitHub missions
* More UI polish
* SQLite-based SQL learning path
* Automated tests

---

## Tech Stack

* Python
* Rich terminal UI
* JSON for local save data
* Git and GitHub
* Modern `pyproject.toml` packaging

---

## Project Structure

```text
gitquest/
|-- pyproject.toml
|-- README.md
|-- requirements.txt
|-- src/gitquest/
|   |-- application/     # Game and mission orchestration
|   |-- domain/          # Core rules, player model, and current missions
|   |-- runtime/         # Disposable mission workspaces
|   |-- adapters/        # Git and future security-tool integrations
|   |-- persistence/     # Progress and future evidence storage
|   |-- interfaces/      # Terminal presentation
|   `-- reporting/       # Future evidence reports
|-- scenarios/           # Versioned security scenario packs and fixtures
|-- policies/            # Future policy-as-code checks
|-- tests/               # Unit, contract, integration, and scenario tests
|-- docs/                # Architecture, ADRs, and threat models
|-- data/                 # Local progress data
|-- artifacts/            # Generated local evidence reports
`-- sandboxes/            # Generated practice repositories
```

Notes:

* The Python package uses a `src/` layout and is installed as the `gitquest` command.
* `data/progress.json` is created locally when the player saves progress.
* `data/progress.json` is ignored by Git.
* `sandboxes/` is created locally for real Git practice missions.
* `sandboxes/` is ignored by Git.
* See `docs/architecture/project-structure.md` for package responsibilities and dependency direction.

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/ST10437403-JamesMaherry/GitQuest.git
cd GitQuest
```

---

### 2. Create a Virtual Environment

On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

When the virtual environment is active, the terminal should show something like:

```text
(.venv)
```

---

### 3. Install Dependencies

```bash
python -m pip install -e .
```

For development tools such as pytest and Ruff:

```bash
python -m pip install -e ".[dev]"
```

---

### 4. Run the Game

```bash
gitquest
```

The explicit form is also available:

```bash
gitquest play
```

You can also run the installed package directly:

```bash
python -m gitquest
```

### 5. Check Your Environment

Run the built-in diagnostics before starting missions:

```bash
gitquest doctor
```

For CI scripts or other automation, request JSON output:

```bash
gitquest doctor --json
```

The current campaign uses the **Lite** profile, which needs only Python and Git. Standard and Full
list optional free, open-source tools planned for later DevSecOps missions; missing tools do not
prevent the Lite campaign from running.

### 6. Run the Security Scenario

List the available scenario packs:

```bash
gitquest scenario list
```

Create a fresh copy of the first incident repository:

```bash
gitquest scenario start supply-chain-siege
```

GitQuest prints the disposable workspace path and the objectives. Read `INCIDENT.md` inside that
workspace, perform the Git and workflow remediation, and then run:

```bash
gitquest scenario verify supply-chain-siege
```

Verification scores the response out of 100 and writes portfolio-safe Markdown and JSON reports to
`artifacts/reports/`. Starting the scenario again safely resets only that marked scenario workspace.

---

## How to Play

When the game starts, enter your developer name.

You can then choose from the main menu:

```text
1. Open mission map
2. View player stats
3. View learned commands
4. Reset progress
5. Save and exit
```

Each mission teaches or tests a Git command.

Some missions are quiz-based. Others create real sandbox folders where you must run actual Git commands.

---

## Example Commands Covered

GitQuest teaches commands such as:

```bash
git init
git status
git add .
git add --all
git commit -m "message"
git log
git branch
git switch -c feature/new-feature
git switch feature/login
git checkout -b feature/new-feature
```

More commands will be added as the game grows.

---

## Virtual Environment Notes

This project uses a Python virtual environment called `.venv`.

The `.venv` folder is not pushed to GitHub because it is local to each computer.

To activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

To deactivate it:

```bash
deactivate
```

You do not need to deactivate it every time, but it is good practice when you are finished working on the project.

---

## Local Save Data

Player progress is stored locally in:

```text
data/progress.json
```

This file is ignored by Git so each player has their own save data.

If the file does not exist, GitQuest creates it automatically when progress is saved.

---

## Development Roadmap

### Completed

* [x] Create first playable prototype
* [x] Add player system
* [x] Add XP and levels
* [x] Add JSON save system
* [x] Add flexible answer checking
* [x] Add mission map
* [x] Add Rich terminal UI
* [x] Add `.gitignore`
* [x] Add local data folder placeholder
* [x] Add real Git sandbox mission support
* [x] Add safety-marked disposable workspaces
* [x] Add environment diagnostics and runtime profiles
* [x] Add the first unit and integration test suite
* [x] Add validated data-driven scenario manifests
* [x] Add the Supply Chain Siege incident-response scenario
* [x] Add scored Markdown and JSON evidence reports

### Planned

* [ ] Add more sandbox missions
* [ ] Add first commit sandbox challenge
* [ ] Add branch sandbox challenge
* [ ] Add merge conflict missions
* [ ] Add remote repository missions
* [ ] Add SQLite-based SQL learning path
* [ ] Add security-tool contract tests
* [ ] Add pipeline and cloud-native scenario packs

---

## Portfolio Goals

This project demonstrates:

* Python fundamentals
* Clean project structure
* Terminal application design
* Git and GitHub workflow
* Branch-based development
* Pull request workflow
* JSON file handling
* Local save data
* Virtual environment usage
* Modern Python packaging and dependency management with `pyproject.toml`
* User interface improvements with Rich
* Running and validating real Git commands from Python
* Defensive filesystem handling and safe disposable environments
* Capability detection for progressive DevSecOps tooling
* Automated unit and integration testing
* Schema validation and declarative security controls
* Reproducible incident-response labs and evidence reporting
* Iterative feature development

---

## Author

Built by **James Maherry** as a Python portfolio project and Git learning tool.
