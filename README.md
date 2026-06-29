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

Sandbox folders are created locally inside:

```text
sandboxes/
```

The `sandboxes/` folder is ignored by Git so practice repositories are not pushed to GitHub.

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
* VS Code

---

## Project Structure

```text
gitquest/
│
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── game/
│   ├── __init__.py
│   ├── answer_checker.py
│   ├── engine.py
│   ├── mission_map.py
│   ├── missions.py
│   ├── player.py
│   ├── sandbox_manager.py
│   ├── save_system.py
│   └── ui.py
│
├── data/
│   └── .gitkeep
│
└── sandboxes/
```

Notes:

* `data/progress.json` is created locally when the player saves progress.
* `data/progress.json` is ignored by Git.
* `sandboxes/` is created locally for real Git practice missions.
* `sandboxes/` is ignored by Git.

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
pip install -r requirements.txt
```

---

### 4. Run the Game

On macOS/Linux:

```bash
python main.py
```

If needed, use:

```bash
python3 main.py
```

On Windows:

```bash
python main.py
```

---

## How to Play

When the game starts, enter your developer name.

You can then choose from the main menu:

```text
1. Open mission map
2. View player stats
3. View learned commands
4. Save and exit
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

### Planned

* [ ] Add more sandbox missions
* [ ] Add first commit sandbox challenge
* [ ] Add branch sandbox challenge
* [ ] Add merge conflict missions
* [ ] Add remote repository missions
* [ ] Add SQLite-based SQL learning path
* [ ] Add tests

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
* Dependency management with `requirements.txt`
* User interface improvements with Rich
* Running and validating real Git commands from Python
* Iterative feature development

---

## Author

Built by **James Maherry as a Python portfolio project and Git learning tool.
