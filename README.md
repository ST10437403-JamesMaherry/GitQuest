# GitQuest: The Version Control Adventure

**GitQuest** is a terminal-based Python learning game designed to help developers master Git commands in a fun, interactive, and story-driven way.

Instead of memorizing Git commands from a cheat sheet, players progress through missions, unlock commands, earn XP, level up, and eventually complete real Git challenges inside sandbox repositories.

This project is being built as both a learning tool and a portfolio project.

---

## Project Vision

Git is one of the most important tools for developers, but it can feel confusing when learned only through documentation or tutorials.

GitQuest turns Git practice into a game.

The player enters a fictional developer world where broken repositories, corrupted timelines, branching paths, and merge conflicts become part of the story. To progress, the player must learn and use real Git commands.

Future learning paths may include SQL, Docker, APIs, and backend development concepts.

---

## Current Features

The current version includes:

* Terminal-based gameplay
* Player name creation
* XP and leveling system
* Mission-based Git command challenges
* Save and load progress using JSON
* Unlockable Git commands
* Simple interactive menu system

---

## Planned Features

GitQuest is still in early development. Planned improvements include:

### Better Input Checking

The game will accept more realistic command answers.

For example, instead of only accepting:

```bash
git commit -m
```

It should also accept answers like:

```bash
git commit -m "Add first mission"
git commit -m 'Create player system'
```

---

### Mission Map

Instead of only playing the next mission in order, players will eventually choose areas from a mission map, such as:

* Git Basics
* Branching Forest
* Merge Conflict Dungeon
* Remote Repository Citadel
* Time Travel Tower
* Stash Cave

---

### Rich Terminal Styling

The game will use the Python `rich` library to create a more polished terminal experience, including:

* Styled text
* Panels
* Tables
* Progress bars
* Better menus
* Color-coded feedback

---

### Real Git Sandbox Challenges

Future versions will include real Git practice missions.

The game may create temporary sandbox folders where players must run actual Git commands to complete objectives.

Example:

```bash
git init
git status
git add .
git commit -m "Complete mission"
```

The game can then check whether the repository is in the correct state.

---

### SQL Learning Path

GitQuest may eventually expand into a broader developer learning game.

A future SQL path could use SQLite to teach concepts like:

```sql
SELECT
WHERE
ORDER BY
JOIN
GROUP BY
INSERT
UPDATE
DELETE
CREATE TABLE
```

This would allow players to practice real SQL queries inside the game.

---

## Project Structure

```text
gitquest/
│
├── main.py
├── README.md
├── requirements.txt
│
├── game/
│   ├── __init__.py
│   ├── player.py
│   ├── missions.py
│   ├── engine.py
│   └── save_system.py
│
└── data/
    └── progress.json
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/ST10437403-JamesMaherry/GitQuest.git
cd GitQuest
```

---

### 2. Run the Game

```bash
python main.py
```

Depending on your system, you may need:

```bash
python3 main.py
```

---

## How to Play

When the game starts, enter your developer name.

You can then choose from the main menu:

```text
1. Start next mission
2. View player stats
3. View learned commands
4. Save and exit
```

Each mission teaches a Git command through a short story challenge.

Example:

```text
MISSION 1: The Empty Repository

You find an empty project folder. To begin your journey, you must turn it into a Git repository.

Which Git command initializes a new repository?
> git init
```

Correct answers reward XP and unlock commands.

---

## Example Git Commands Covered

GitQuest will teach commands such as:

```bash
git init
git status
git add .
git commit -m "message"
git log
git branch
git switch
git checkout
git merge
git stash
git reset
git revert
git remote
git push
git pull
```

---

## Learning Goals

By building and playing GitQuest, the goal is to become comfortable with:

* Using Git from the terminal
* Understanding Git workflow basics
* Staging and committing changes
* Reading repository status
* Creating and switching branches
* Merging branches
* Resolving conflicts
* Working with remote repositories
* Building a structured Python project
* Saving and loading data with JSON
* Eventually working with SQLite and SQL

---

## Tech Stack

Current stack:

* Python
* JSON for save data
* Git and GitHub
* VS Code

Planned additions:

* Rich for terminal UI
* SQLite for SQL missions and save data
* Real Git sandbox validation
* Possible web dashboard in the future

---

## Why This Project?

This project is designed to be more than a simple quiz app.

GitQuest is a practical learning game that combines:

* Developer education
* Game mechanics
* Terminal practice
* Python programming
* Portfolio-ready project structure

It is also being built using Git from the start, which means the development process itself reinforces the skills the game is teaching.

---

## Development Roadmap

### Phase 1: First Playable Prototype

* [x] Create project structure
* [x] Add terminal game loop
* [x] Add player system
* [x] Add XP and levels
* [x] Add basic Git missions
* [x] Add JSON save system

### Phase 2: Improve Gameplay

* [ ] Improve answer validation
* [ ] Add command aliases and flexible accepted answers
* [ ] Add mission categories
* [ ] Add mission map
* [ ] Add more Git basics missions

### Phase 3: Improve Presentation

* [ ] Add Rich terminal styling
* [ ] Add styled menus
* [ ] Add ASCII art
* [ ] Add progress bars
* [ ] Improve feedback messages

### Phase 4: Real Git Practice

* [ ] Create sandbox repositories
* [ ] Check real Git command results
* [ ] Add branch challenges
* [ ] Add merge conflict challenges
* [ ] Add remote repository simulations

### Phase 5: SQL Expansion

* [ ] Add SQLite database
* [ ] Add SQL learning path
* [ ] Add SQL missions
* [ ] Add query validation
* [ ] Add database-themed story area

---

## Portfolio Goals

This project aims to demonstrate:

* Python fundamentals
* Clean project organization
* File handling
* JSON data persistence
* Terminal application design
* Git and GitHub workflow
* Future SQL integration
* Creative problem solving
* Ability to build a project iteratively

---

## Contributing

This is currently a personal learning project, but suggestions and ideas are welcome.

---

## License

This project is open source. A license may be added later.

---

## Author

Built by James Maherry as a Python portfolio project and Git learning tool.