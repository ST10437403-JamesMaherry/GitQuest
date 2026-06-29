MISSIONS = [
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
        "hint": "Use git switch with the -c option to create and move to a new branch."
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
}
]