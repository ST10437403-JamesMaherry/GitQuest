# GitQuest roadmap

## North star

GitQuest should make a learner capable of explaining Git, recovering from common mistakes, and
participating confidently in a GitHub pull-request workflow. Every lesson should follow the same
loop: explain one idea, predict what will happen, perform a real action, inspect the result, and
reflect on why it happened.

## Release 0.5 — Reset baseline

- Remove the abandoned incident-response product direction.
- Keep the working terminal campaign and disposable workspace protections.
- Reduce the browser to an honest curriculum and setup guide.
- Establish one source of truth for the Git learning path.
- Publish a sequence of small, reversible implementation commits.

## Release 0.6 — Browser learning shell

- Add lesson, challenge, result, and progress domain models.
- Introduce a browser lesson route and accessible command console.
- Run allow-listed Git actions against isolated local repositories.
- Display working-tree, staging-area, commit, branch, and remote state visually.

## Release 0.7 — Git foundations

- Cover configuration, initialization, status, diffs, staging, commits, logs, and `.gitignore`.
- Require predictions before key actions and explanations after them.
- Add deterministic validators and retry-friendly feedback.

## Release 0.8 — Branching, merging, and recovery

- Teach branches, merges, conflicts, rebases, restore, reset, revert, reflog, and cherry-pick.
- Use generated repositories with known histories and safe reset markers.
- Add visual commit graphs and compare expected state with actual repository state.

## Release 0.9 — GitHub collaboration

- Teach remotes, clone, fetch, pull, push, forks, issues, pull requests, reviews, and releases.
- Simulate GitHub web flows locally so the core course remains free and deterministic.
- Add optional real-GitHub extension points only after the offline experience is complete.

## Release 1.0 — Portfolio-ready course

- Complete onboarding, progress, accessibility, curriculum coverage, and recovery guidance.
- Add end-to-end tests, packaging smoke tests, and performance budgets.
- Publish an architecture case study and a concise product demonstration.
- Validate the course with first-time Git learners and incorporate their feedback.

## Explicit non-goals

- DevSecOps incident response, cloud labs, and security scanning
- Paid APIs or required cloud accounts
- Running arbitrary shell commands from browser input
- Replacing GitHub or duplicating every Git hosting feature
- Gamification that rewards guessing instead of understanding
