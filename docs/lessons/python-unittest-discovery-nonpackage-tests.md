# Python Unittest Discovery For Non-package Tests

## Summary

This repository's `tests/` directory is not a Python package. Run its tests with unittest discovery or direct file execution instead of dotted names such as `tests.test_visual_output_contract`.

## Lookup Hints

- Keywords: `ModuleNotFoundError`, `tests.test_`, `python -m unittest`, `unittest discover`, non-package tests, missing `tests/__init__.py`.
- Typical error: `No module named 'tests.test_m_continue_contract'`.
- Quick checks:
  - verify whether `tests/__init__.py` exists
  - run `python -m unittest discover -s tests`
  - use `-p "test_*contract.py"` for focused contract discovery

## Symptoms

- A test file exists and runs through discovery, but dotted module invocation fails to import it.
- `python -m unittest tests.test_name` reports `ModuleNotFoundError`.
- Skill validation succeeds while the planned focused unittest command fails before any assertion runs.

## Impact

The failure can be misclassified as a product or contract regression even though no test body executed. It also wastes repair cycles when the real issue is only the runner entry point.

## Trigger Conditions

- The repository keeps test files in `tests/` without `tests/__init__.py`.
- A plan copies Python package-style unittest syntax without checking repository topology.
- Focused tests are selected by dotted module name rather than discovery pattern.

## Root Cause

Python dotted unittest names require importable modules. Without `tests/__init__.py`, `tests.test_name` is not an importable package module in this repository's normal execution context.

## Investigation Trail

1. Both affected Skill validators passed.
2. The first focused unittest command failed with two `ModuleNotFoundError` import errors.
3. Confirmed that `tests/` is not a Python package.
4. Replaced dotted module invocation with discovery from the `tests` start directory.
5. The 13 focused contract tests and later all 32 repository tests passed.

## Resolution

Use:

```powershell
python -m unittest discover -s tests -p "test_*contract.py"
```

For the whole suite, use:

```powershell
python -m unittest discover -s tests
```

## Prevention / Guardrails

- Inspect test package topology before recording a command in `plan.md`.
- Prefer the repository's established test command when one exists.
- Treat import-loader failures separately from assertion failures.
- Do not add `tests/__init__.py` merely to make one planned command work unless package semantics are intentionally desired.

## Related Docs

- [m-continue change archive](../change/2026-07-17_m-continue-loop.md)
- [m-continue archived plan](../plan/2026-07-17_m-continue-loop.md)
- [m-autoflow workflow spec](../specs/m-autoflow-skill.md)
