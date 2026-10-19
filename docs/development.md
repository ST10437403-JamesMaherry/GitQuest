# Developing GitQuest

## Environment

Create and activate a virtual environment, then install the development extras:

    python3 -m venv .venv
    source .venv/bin/activate
    make install-dev PYTHON=python

The Makefile intentionally uses an overridable Python command. Passing <code>PYTHON=python</code>
ensures every command uses the activated environment. Without an override, Make uses
<code>python3</code>.

## Local quality gate

Run the same gate used by GitHub Actions:

    make ci PYTHON=python

That command runs:

1. Ruff static checks;
2. Ruff's formatting check;
3. the complete unittest suite, including local HTTP and Git integration tests; and
4. wheel plus source-distribution builds.

Use focused targets while developing:

    make test PYTHON=python
    make lint PYTHON=python
    make format-check PYTHON=python
    make build PYTHON=python

The format target is intentionally check-only. Formatting source remains an explicit developer
choice rather than an unexpected Makefile mutation.

## CI design

The CI workflow runs on pushes to <code>main</code>, pull requests, and manual dispatches. It uses:

- read-only repository permissions;
- immutable commit SHAs for GitHub-authored actions;
- disabled persisted checkout credentials;
- a Python 3.9 and 3.13 test matrix;
- pip caching managed by setup-python;
- a ten-minute job timeout; and
- the same <code>make ci</code> command used locally.

After the quality gate, CI smoke-tests the installed command, doctor JSON, and scenario catalog.

## Dependency updates

Dependabot runs weekly for:

- Python production dependencies;
- Python development dependencies; and
- GitHub Actions.

Updates are grouped by purpose to reduce pull-request noise. Review and merge them like any other
code change. In particular, verify action SHA changes, changelogs, test results, and supported Python
versions before merging.

## Browser UI constraints

The incident console has no build step or remote assets. Keep it:

- black, white, and neutral gray;
- usable at 320px and wide desktop layouts;
- keyboard navigable with visible focus;
- understandable without color;
- compatible with reduced-motion preferences;
- free of inline scripts and styles so the Content Security Policy stays strict; and
- dependent only on the existing localhost JSON API.

Run <code>make web PYTHON=python</code> and inspect desktop plus mobile layouts after changing HTML,
CSS, or JavaScript.
