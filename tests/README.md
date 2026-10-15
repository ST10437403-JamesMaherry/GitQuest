# Test suites

- `unit/` tests pure domain and application behavior.
- `contract/` checks that every external-tool adapter returns the same result shape.
- `integration/` exercises real local tools such as Git.
- `scenarios/` proves each scenario has a known failing and passing state.

Run the dependency-free test suite from the repository root:

```bash
python -m unittest discover -s tests -v
```

If the optional development dependencies are installed, `pytest` can run the same tests:

```bash
pytest
```
