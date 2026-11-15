# Decisions index

> Living document. Index of all ADRs across all features. Update it in place.

Last updated: 0000004-separation-core

## All architecture decision records

| ADR | Title | Feature | Status | Summary |
|-----|-------|---------|--------|---------|
| [ADR-0001](adr/0001-python-tooling.md) | Python tooling and layout | 0000002-python-scaffold | active | One root `pyproject.toml` with `pytest` and `ruff`, and one package folder for each component |
| [ADR-0002](adr/0002-separator-injection-and-pin.md) | Separator injection, lazy import, and a pinned extra | 0000004-separation-core | active | `split()` builds its separator through a factory, and the library installs from a pinned extra |

## Status definitions

| Status | Meaning |
|--------|---------|
| active | Decision stands, and implementation follows it |
| superseded | A later ADR replaced it |
| amended | The core decision stands, but conditions or scope changed |
