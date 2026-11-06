# Developing GitQuest

## Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
make install-dev PYTHON=python
```

The `PYTHON` Make variable ensures every command uses the active environment.

## Quality gate

```bash
make ci PYTHON=python
```

This runs Ruff static checks, Ruff formatting checks, all unit and integration tests, and Python
package builds. CI runs the same command on every pull request.

## Commit discipline

- Make one observable change per commit.
- Use imperative Conventional Commit subjects, such as `feat(lessons): add status prediction`.
- Keep tests in the same commit as the behavior they protect.
- Do not mix mechanical renames with behavior changes.
- Keep the application runnable and the quality gate green after every commit.
- Update documentation when a command, route, learning objective, or boundary changes.

The planned sequence is in [`execution-plan.md`](execution-plan.md). It is a guide, not permission
to preserve a poor decision just to keep the original numbering.

## Browser constraints

The browser has no build step or remote assets. Keep it responsive at 320px, keyboard navigable,
understandable without color, compatible with reduced-motion preferences, and compliant with its
strict Content Security Policy.

Browser controls must never pass arbitrary commands or paths to a shell. Add typed, allow-listed
application operations and repository-state validators instead.

## Definition of done for a lesson

A lesson is complete only when it includes a learning objective, short explanation, prediction,
safe setup, authentic action, deterministic validation, helpful retry state, completion summary,
automated tests, and curriculum documentation.
