# Scenario packs

This directory holds versioned, data-driven mission packs. Scenario content stays outside the
Python package so new campaigns can be added without changing the application engine.

Each scenario contains:

- a validated `scenario.json` manifest;
- a reproducible starting fixture;
- deterministic failing and passing states;
- hints and a debrief;
- expected evidence and safety constraints.

`supply_chain/supply-chain-siege/` is the reference implementation. Its objectives use generic,
declarative check types and must total 100 points. The legacy quiz catalogue remains in
`src/gitquest/domain/missions.py` while it is migrated incrementally.

Validate all scenario behavior with:

```bash
python -m unittest discover -s tests -v
```

The equivalent repository shortcut is <code>make test PYTHON=python</code>. The planned scenario
sequence and definition of done are documented in
[`docs/roadmap.md`](../docs/roadmap.md).
