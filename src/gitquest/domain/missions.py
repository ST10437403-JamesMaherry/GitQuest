# All GitQuest missions are stored in this list.
#
# Each mission is a dictionary that tells the game:
# - which area it belongs to
# - what title/story/question to show
# - which answers should be accepted
# - how much XP to award
# - which command gets unlocked
# - whether the mission is a normal quiz or a sandbox mission
#
# Important:
# Try not to change mission IDs after players have already made progress,
# because completed missions are stored by ID inside progress.json.

MISSIONS = [
    # ============================================================
    # GIT BASICS MISSIONS
    # ============================================================

    {
        "id": 1,
        "area": "git_basics",
        "title": "The Empty Repository",
        "story": "You find an empty project folder. To begin your journey, you must turn it into a Git repository.",
        "question": "Which Git command initializes a new repository?",
        "accepted_answers": [
            "git init"
        ],
        "accepted_patterns": [],
        "xp": 50,
        "command_unlocked": "git init",
        "hint": "This command creates a new Git repository in the current folder."
    },
    {
        "id": 2,
        "area": "git_basics",
        "title": "The Watchful Eye",
        "story": "You need to inspect the current state of your repository before making changes.",
        "question": "Which Git command shows the status of your working directory?",
        "accepted_answers": [
            "git status"
        ],
        "accepted_patterns": [],
        "xp": 50,
        "command_unlocked": "git status",
        "hint": "This command shows staged files, unstaged files, and untracked files."
    },
    {
        "id": 3,
        "area": "git_basics",
        "title": "Preparing the Scroll",
        "story": "You changed a file and now need to stage it before committing.",
        "question": "Which Git command stages all changed files?",
        "accepted_answers": [
            "git add .",
            "git add --all",
            "git add -A"
        ],
        "accepted_patterns": [],
        "xp": 75,
        "command_unlocked": "git add .",
        "hint": "This command moves file changes into the staging area."
    },
    {
        "id": 4,
        "area": "git_basics",
        "title": "Sealing History",
        "story": "Your staged changes are ready to be saved into Git history.",
        "question": "Which Git command creates a commit with a message?",
        "accepted_answers": [
            "git commit -m"
        ],
        "accepted_patterns": [
            r"git\s+commit\s+-m\s+\".+\"",
            r"git\s+commit\s+-m\s+'.+'",
            r"git\s+commit\s+-am\s+\".+\"",
            r"git\s+commit\s+-am\s+'.+'"
        ],
        "xp": 75,
        "command_unlocked": "git commit -m",
        "hint": "Use git commit with the -m option followed by a message in quotes."
    },
    {
        "id": 5,
        "area": "git_basics",
        "title": "Reading the Timeline",
        "story": "The kingdom's history is written in commits. You need to inspect the commit timeline.",
        "question": "Which Git command shows the commit history?",
        "accepted_answers": [
            "git log",
            "git log --oneline"
        ],
        "accepted_patterns": [],
        "xp": 75,
        "command_unlocked": "git log",
        "hint": "This command displays previous commits."
    },

    # ============================================================
    # BRANCHING FOREST QUIZ MISSIONS
    # ============================================================

    {
        "id": 6,
        "area": "branching_forest",
        "title": "Creating a New Path",
        "story": "A new feature must be developed safely without changing the main timeline.",
        "question": "Which Git command creates and switches to a new branch?",
        "accepted_answers": [
            "git switch -c feature/new-feature",
            "git checkout -b feature/new-feature"
        ],
        "accepted_patterns": [
            r"git\s+switch\s+-c\s+[\w\-/]+",
            r"git\s+checkout\s+-b\s+[\w\-/]+"
        ],
        "xp": 100,
        "command_unlocked": "git switch -c",
        "hint": "Use git switch -c followed by the new branch name, for example: git switch -c feature/new-feature."
    },
    {
        "id": 7,
        "area": "branching_forest",
        "title": "Checking Your Path",
        "story": "You need to see which branch you are currently standing on.",
        "question": "Which Git command lists your local branches?",
        "accepted_answers": [
            "git branch"
        ],
        "accepted_patterns": [],
        "xp": 75,
        "command_unlocked": "git branch",
        "hint": "This command shows all local branches and marks the current one with an asterisk."
    },
    {
        "id": 8,
        "area": "branching_forest",
        "title": "Changing Trails",
        "story": "You need to move from your current branch to another existing branch.",
        "question": "Which Git command switches to an existing branch called feature/login?",
        "accepted_answers": [
            "git switch feature/login",
            "git checkout feature/login"
        ],
        "accepted_patterns": [
            r"git\s+switch\s+[\w\-/]+",
            r"git\s+checkout\s+[\w\-/]+"
        ],
        "xp": 100,
        "command_unlocked": "git switch",
        "hint": "Use git switch followed by the branch name."
    },
    {
        "id": 12,
        "area": "branching_forest",
        "title": "Planting a Branch",
        "story": "You want to create a new branch, but you do not want to switch to it yet.",
        "question": "Which Git command creates a new branch called feature/profile without switching to it?",
        "accepted_answers": [
            "git branch feature/profile"
        ],
        "accepted_patterns": [
            r"git\s+branch\s+[\w\-/]+"
        ],
        "xp": 100,
        "command_unlocked": "git branch <branch-name>",
        "hint": "Use git branch followed by the new branch name."
    },
    {
        "id": 13,
        "area": "branching_forest",
        "title": "Returning to Main",
        "story": "Your experiment is finished. Before merging, you need to return to the main branch.",
        "question": "Which Git command switches back to the main branch?",
        "accepted_answers": [
            "git switch main",
            "git checkout main",
            "git switch master",
            "git checkout master"
        ],
        "accepted_patterns": [
            r"git\s+switch\s+(main|master)",
            r"git\s+checkout\s+(main|master)"
        ],
        "xp": 100,
        "command_unlocked": "git switch main",
        "hint": "Use git switch main. Some older repositories may use master instead of main."
    },
    {
        "id": 14,
        "area": "branching_forest",
        "title": "Removing an Old Trail",
        "story": "A finished feature branch is no longer needed. You want to delete it safely.",
        "question": "Which Git command safely deletes a local branch called feature/old-menu?",
        "accepted_answers": [
            "git branch -d feature/old-menu"
        ],
        "accepted_patterns": [
            r"git\s+branch\s+-d\s+[\w\-/]+"
        ],
        "xp": 125,
        "command_unlocked": "git branch -d",
        "hint": "Use git branch with the lowercase -d option for a safe local branch delete."
    },
    {
        "id": 15,
        "area": "branching_forest",
        "title": "Forcing the Path Closed",
        "story": "A broken branch was never merged, but you still want to remove it from your local repository.",
        "question": "Which Git command force deletes a local branch called feature/broken-test?",
        "accepted_answers": [
            "git branch -D feature/broken-test"
        ],
        "accepted_patterns": [
            r"git\s+branch\s+-D\s+[\w\-/]+"
        ],
        "xp": 125,
        "command_unlocked": "git branch -D",
        "hint": "Use uppercase -D when you want to force delete a local branch."
    },
    {
        "id": 16,
        "area": "branching_forest",
        "title": "Joining Two Paths",
        "story": "Your feature branch is complete. You are standing on main and want to bring the feature work into it.",
        "question": "Which Git command merges a branch called feature/login into your current branch?",
        "accepted_answers": [
            "git merge feature/login"
        ],
        "accepted_patterns": [
            r"git\s+merge\s+[\w\-/]+"
        ],
        "xp": 150,
        "command_unlocked": "git merge",
        "hint": "First switch to the branch receiving the changes, then run git merge followed by the branch you want to merge in."
    },
    {
        "id": 17,
        "area": "branching_forest",
        "title": "Seeing Every Trail",
        "story": "You want to inspect both local and remote branches before deciding where to work next.",
        "question": "Which Git command lists all local and remote branches?",
        "accepted_answers": [
            "git branch -a",
            "git branch --all"
        ],
        "accepted_patterns": [
            r"git\s+branch\s+(-a|--all)"
        ],
        "xp": 100,
        "command_unlocked": "git branch -a",
        "hint": "Use git branch with -a or --all to show both local and remote branches."
    },

    # ============================================================
    # SANDBOX MISSIONS
    # ============================================================

    {
        "id": 9,
        "area": "git_basics",
        "title": "Sandbox Trial: Awaken the Repository",
        "story": "You have entered a real practice folder. Your task is to initialize it as a Git repository using the terminal.",
        "question": "Run the required Git command inside the sandbox folder. When you are done, return here and press Enter.",
        "accepted_answers": [],
        "accepted_patterns": [],
        "xp": 125,
        "command_unlocked": "git init",
        "hint": "Open the sandbox folder in your terminal and run: git init",
        "mission_type": "sandbox",
        "sandbox_validation": "is_git_repository"
    },
    {
        "id": 10,
        "area": "git_basics",
        "title": "Sandbox Trial: First Commit",
        "story": "Your repository has awakened, but it has no history. Create a file, stage it, and make your first commit.",
        "question": "Inside the sandbox folder, initialize Git, create any file, stage it, and make at least one commit. When you are done, return here and press Enter.",
        "accepted_answers": [],
        "accepted_patterns": [],
        "xp": 150,
        "command_unlocked": "git commit",
        "hint": "Run git init, create a file, run git add ., then run git commit -m \"First commit\".",
        "mission_type": "sandbox",
        "sandbox_validation": "has_commit"
    },
    {
        "id": 11,
        "area": "branching_forest",
        "title": "Sandbox Trial: Forge a New Branch",
        "story": "A dangerous change is ahead. You must protect the main path by creating a separate feature branch.",
        "question": "Inside the sandbox folder, initialize Git and create a branch called feature/sandbox-practice. When you are done, return here and press Enter.",
        "accepted_answers": [],
        "accepted_patterns": [],
        "xp": 150,
        "command_unlocked": "git switch -c",
        "hint": "Run git init, then run git switch -c feature/sandbox-practice.",
        "mission_type": "sandbox",
        "sandbox_validation": "has_branch",
        "expected_branch": "feature/sandbox-practice"
    }
]