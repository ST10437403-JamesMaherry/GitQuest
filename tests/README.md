# Test suites

- `unit/` tests pure domain and application behavior.
- `contract/` checks that every external-tool adapter returns the same result shape.
- `integration/` exercises real local tools such as Git.
- `scenarios/` proves each scenario has a known failing and passing state.

Run the dependency-free test suite from the repository root:

```bash
python -m unittest discover -s tests -v
```

The browser integration tests bind an ephemeral localhost port. Run them in an environment that
allows loopback sockets.

If the optional development dependencies are installed, `pytest` can run the same tests:

```bash
pytest
```
