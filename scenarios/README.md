# Scenario packs

This directory will hold versioned, data-driven mission packs. Keep scenario content outside
the Python package so new campaigns can be added without changing the application engine.

Each scenario should eventually contain:

- a validated mission manifest;
- a reproducible starting fixture;
- deterministic failing and passing states;
- hints and a debrief;
- expected evidence and safety constraints.

The current Python mission catalogue remains in `src/gitquest/domain/missions.py` until the
manifest loader is created.
