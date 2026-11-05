# GitQuest 100-commit execution plan

This is the proposed path from the reset baseline to a portfolio-ready Git and GitHub learning
game. Each numbered item is intended to be one small, reviewable commit. The sequence is a planning
tool: combine or split an item when the code proves that is cleaner, but keep each commit focused,
tested, documented, and runnable.

## Working rules

- Work on `dev`; merge tested milestones to `main`.
- Start every item from a green `make ci PYTHON=python`.
- Use Conventional Commit subjects with an imperative verb.
- Put the test for new behavior in the same commit.
- Never mix broad formatting with functional changes.
- Do not add paid services, required accounts, or remote runtime dependencies.
- Do not accept arbitrary shell commands from the browser.
- Demonstrate the product after commits 10, 25, 40, 60, 75, 90, and 100.

## Phase 1 — Establish the product core (commits 1–10)

1. `refactor(product): reset GitQuest to Git learning core` — land this stripped baseline.
2. `test(domain): cover every existing answer pattern` — lock down current quiz behavior.
3. `test(domain): cover mission map progress rules` — protect area counts and unlocks.
4. `refactor(domain): replace mission dictionaries with typed models` — introduce immutable types.
5. `refactor(domain): add curriculum repository interface` — separate content from global lists.
6. `refactor(application): extract player session service` — remove session work from terminal UI.
7. `refactor(application): extract mission completion service` — centralise XP and replay rules.
8. `refactor(application): return typed gameplay outcomes` — stop application logic from printing.
9. `refactor(interface): adapt terminal campaign to services` — preserve behavior over new seams.
10. `docs(architecture): record shared gameplay service boundary` — confirm the milestone design.

**Milestone:** the terminal remains playable and its game rules no longer depend on terminal input.

## Phase 2 — Define the learning system (commits 11–20)

11. `feat(domain): add lesson learning objectives` — state what the learner will be able to do.
12. `feat(domain): add concept explanation blocks` — support short pre-challenge teaching.
13. `feat(domain): add prediction prompts` — ask what will change before an action.
14. `feat(domain): add reflection prompts` — reinforce why the observed state changed.
15. `feat(domain): add prerequisites and lesson ordering` — replace level-only progression.
16. `feat(domain): add difficulty and estimated duration` — set learner expectations.
17. `feat(domain): add command reference metadata` — syntax, examples, and common mistakes.
18. `feat(domain): add retry feedback model` — distinguish hints from final explanations.
19. `feat(domain): add curriculum validation` — reject duplicate IDs and broken prerequisites.
20. `docs(curriculum): publish the complete learning outcomes` — map every planned Git skill.

**Milestone:** content is a validated learning curriculum, not a loose collection of quizzes.

## Phase 3 — Make sandboxes dependable (commits 21–30)

21. `test(runtime): cover workspace marker requirements` — prevent deletion of unmarked paths.
22. `test(runtime): cover path traversal rejection` — prove containment at workspace boundaries.
23. `test(runtime): cover symlink escape rejection` — prevent indirection outside the sandbox.
24. `refactor(runtime): introduce sandbox lifecycle service` — create, inspect, reset, and remove.
25. `feat(runtime): generate deterministic repository fixtures` — make histories repeatable.
26. `feat(adapter): expose structured Git status` — parse porcelain output into domain state.
27. `feat(adapter): expose structured commit history` — return commits and parent relationships.
28. `feat(adapter): expose branch and HEAD state` — support detached and unborn HEADs.
29. `feat(adapter): expose staged and unstaged diffs` — provide safe visualisation data.
30. `feat(runtime): configure isolated author identity` — avoid changing global Git configuration.

**Milestone:** GitQuest can create and inspect reproducible repositories without risking user data.

## Phase 4 — Build the browser lesson shell (commits 31–40)

31. `feat(web): add lesson detail route` — provide a stable URL for each lesson.
32. `feat(web): add curriculum navigation state` — preserve route and back-button behavior.
33. `feat(web): add lesson explanation view` — render objective, concept, and prerequisites.
34. `feat(web): add prediction interaction` — collect a choice before enabling an action.
35. `feat(web): add repository state panel` — show working tree, stage, HEAD, and branches.
36. `feat(web): add typed action API schema` — define allow-listed gameplay operations.
37. `feat(web): add local request verification` — protect mutation routes from simple cross-origin requests.
38. `feat(web): add bounded JSON request parsing` — validate size, type, and fields.
39. `feat(web): add accessible command console` — show generated commands and output safely.
40. `test(web): cover the complete browser lesson shell` — exercise routes, state, and security headers.

**Milestone:** a learner can open a lesson, predict an outcome, and inspect a safe repository.

## Phase 5 — Teach everyday Git foundations (commits 41–55)

41. `feat(lessons): teach Git configuration scope` — system, global, local, and identity.
42. `feat(lessons): teach repository initialization` — `.git`, working tree, and unborn branch.
43. `feat(lessons): teach untracked and tracked files` — explain Git's file lifecycle.
44. `feat(lessons): teach status reading` — decode every section of concise status output.
45. `feat(lessons): teach working-tree diffs` — inspect changes before staging.
46. `feat(lessons): teach selective staging` — stage files and hunks intentionally.
47. `feat(lessons): teach staged diffs` — review exactly what the next commit contains.
48. `feat(lessons): teach meaningful commits` — create focused history with useful messages.
49. `feat(lessons): teach logs and commit identity` — hashes, parents, authors, and dates.
50. `feat(lessons): teach file removal and movement` — compare filesystem and Git-aware actions.
51. `feat(lessons): teach ignore rules` — root, directory, negation, and already-tracked files.
52. `feat(lessons): teach amend safely` — distinguish local cleanup from shared-history rewriting.
53. `feat(lessons): teach restore from working tree` — recover a file without losing the mental model.
54. `feat(lessons): add foundations checkpoint` — solve a multi-step repository task unaided.
55. `test(curriculum): cover foundations completion path` — run all lessons in order.

**Milestone:** the browser course teaches the complete daily edit-stage-commit-inspect loop.

## Phase 6 — Teach branches and integration (commits 56–70)

56. `feat(graph): add commit graph domain model` — represent parents, refs, and HEAD.
57. `feat(web): render an accessible commit graph` — pair visual lines with a text alternative.
58. `feat(lessons): teach branch pointers` — show that a branch is a movable name.
59. `feat(lessons): teach branch creation and switching` — compare `switch` and legacy checkout.
60. `feat(lessons): teach divergent history` — create commits on two branches.
61. `feat(lessons): teach fast-forward merges` — predict pointer movement.
62. `feat(lessons): teach three-way merges` — inspect merge bases and merge commits.
63. `feat(lessons): teach conflict anatomy` — base, ours, theirs, and conflict markers.
64. `feat(lessons): teach conflict resolution` — edit, stage, verify, and complete a merge.
65. `feat(lessons): teach merge abort` — return safely to the pre-merge state.
66. `feat(lessons): teach rebase mental model` — copy commits onto a new base.
67. `feat(lessons): teach interactive rebase planning` — reorder, squash, and reword locally.
68. `feat(lessons): teach safe branch deletion` — merged checks and force-delete consequences.
69. `feat(lessons): add branching checkpoint` — integrate a feature with one conflict.
70. `test(curriculum): cover branching completion path` — verify deterministic histories.

**Milestone:** learners can explain and resolve common branch integration workflows.

## Phase 7 — Teach recovery and advanced history (commits 71–80)

71. `feat(lessons): teach restore versus reset` — separate file recovery from ref movement.
72. `feat(lessons): teach soft mixed and hard reset` — visualise index and working-tree effects.
73. `feat(lessons): teach revert` — undo shared history with a new commit.
74. `feat(lessons): teach reflog recovery` — recover an apparently lost commit.
75. `feat(lessons): teach cherry-pick` — copy a focused change between branches.
76. `feat(lessons): teach tags` — annotated tags and release points.
77. `feat(lessons): teach detached HEAD` — experiment and preserve useful work.
78. `feat(lessons): teach stash intentionally` — save, inspect, apply, pop, and resolve.
79. `feat(lessons): add recovery checkpoint` — repair a deliberately damaged local history.
80. `test(curriculum): cover recovery completion path` — prove every escape route.

**Milestone:** learners can recover from mistakes instead of deleting repositories and starting over.

## Phase 8 — Connect Git to GitHub workflows (commits 81–90)

81. `feat(simulator): add local GitHub repository model` — owners, visibility, and default branch.
82. `feat(lessons): teach remotes and tracking branches` — names, URLs, and upstreams.
83. `feat(lessons): teach clone fetch pull and push` — separate data transfer from integration.
84. `feat(simulator): add issue workflow` — create, label, assign, and close an issue.
85. `feat(simulator): add fork workflow` — distinguish origin and upstream.
86. `feat(simulator): add pull request workflow` — base, compare, commits, and changed files.
87. `feat(simulator): add review workflow` — comments, approvals, and requested changes.
88. `feat(simulator): add merge strategy lesson` — merge, squash, and rebase outcomes.
89. `feat(simulator): add release workflow` — tags, notes, and published artifacts conceptually.
90. `test(curriculum): cover GitHub collaboration journey` — complete issue-to-release flow offline.

**Milestone:** learners understand how local Git concepts map onto the GitHub web interface.

## Phase 9 — Finish the learning product (commits 91–100)

91. `feat(progress): persist lesson attempts and mastery` — store outcomes locally without telemetry.
92. `feat(progress): add resumable learning dashboard` — show next lesson and completed skills.
93. `feat(progress): add command reference notebook` — collect concepts unlocked by the learner.
94. `feat(accessibility): complete keyboard and screen-reader pass` — meet WCAG-oriented checks.
95. `feat(accessibility): add reduced-motion and high-contrast validation` — test preference modes.
96. `test(e2e): add first-run to checkpoint journey` — cover the primary browser experience.
97. `perf(web): enforce local asset and response budgets` — keep startup and navigation fast.
98. `docs(case-study): explain product and architecture decisions` — create interview-ready evidence.
99. `docs(demo): add a five-minute portfolio walkthrough` — show the problem, design, and outcomes.
100. `release: publish GitQuest 1.0 learning game` — tag the tested, documented, free release.

**Milestone:** GitQuest is a coherent, demonstrable learning product rather than a collection of
features.

## Suggested first implementation slice

After committing the reset as item 1, complete items 2–10 before adding new lessons. That work is
less visually exciting, but it creates the shared application boundary required for a genuinely
browser-based game without duplicating the terminal engine.
