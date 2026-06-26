# GitQuest: The Version Control Adventure

**GitQuest** is a terminal-based Python game that helps developers learn Git commands in a fun and interactive way.

Players complete missions, unlock Git commands, earn XP, level up, and move through different learning areas such as Git Basics and Branching Forest.

This project is being built as both a learning tool and a portfolio project.

---

## Current Features

* Terminal-based gameplay
* Rich terminal UI with styled menus, panels, and tables
* Player name creation
* XP and leveling system
* Mission map with different learning areas
* Git command missions
* Flexible answer checking for realistic Git commands
* Unlockable Git commands
* Local JSON save system

---

## Planned Features

Future improvements include:

* Real Git sandbox challenges
* Merge conflict missions
* Remote repository and GitHub missions
* More mission areas
* Progress bars and improved UI polish
* SQL learning path using SQLite

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
│   ├── save_system.py
│   └── ui.py
│
└── data/
    └── progress.json
```

Note: `data/progress.json` is used for local save data and is ignored by Git.

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

When the virtual environment is active, your terminal should show something like:

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

If that does not work, use:

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

The mission map contains different learning areas.

Current areas include:

* Git Basics
* Branching Forest
* Merge Conflict Dungeon
* Remote Repository Citadel

Some areas may be locked until the player reaches a higher level.

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

### Planned

* [ ] Add real Git sandbox challenges
* [ ] Add merge conflict missions
* [ ] Add remote repository missions
* [ ] Add SQLite-based SQL learning path
* [ ] Add more UI polish
* [ ] Add tests

---

## Portfolio Goals

This project demonstrates:

* Python fundamentals
* Clean project structure
* Terminal application design
* Git and GitHub workflow
* JSON file handling
* Virtual environment usage
* Dependency management with `requirements.txt`
* User interface improvements with Rich
* Iterative feature development using branches and pull requests

---

## Author

Built by **James Maherry** as a Python portfolio project and Git learning tool.
