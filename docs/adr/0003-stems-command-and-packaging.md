---
title: "ADR 0003: The stems command and the stem_core package install"
summary: "The stems command uses argparse, keeps probes injectable, and installs through a console script that needs stem_core packaged."
status: "proposed"
component: "stem-core"
version: "0.3.0"
---
# ADR-0003 - The stems command and the stem_core package install

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000006-command-line-interface
**Component:** stem-core
**File:** `docs/adr/0003-stems-command-and-packaging.md`
**Date:** 2026-11-15

## Context

Later steps call the command from scripts and from the Docker image. `pyproject.toml` sets `packages = []`, so `pip install .` installs no code today. A console script needs an importable `stem_core` package. The `env` subcommand reads facts that differ per machine, and unit tests must not depend on them.

## Decision

The command lives in `stem_core/cli.py` as `main(argv=None, split_func=split, probes=None)`. It uses `argparse` with three subcommands. `[project.scripts]` maps `stems` to `stem_core.cli:main`. `pyproject.toml` packages `stem_core` from `src/stem-core` with `package-dir`. `stem_core/__main__.py` calls the same `main()`. `split_func` and `probes` are arguments, so tests inject fakes. The `env` probes import `torch` late and never load a model.

## Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|-------------|
| `click` or `typer` | Less parsing code | A new dependency | The chart pre-approves `argparse` and no dependency |
| Run the command only as `python -m stem_core` | No packaging change | No `stems` name on the path | The entry says the command is named `stems` |
| Patch `shutil.which` and `torch` in tests | No new argument | Tests couple to import paths | Injected probes are explicit, as with the separator factory in ADR-0002 |

## Affected Components

| Component | Impact |
|-----------|--------|
| stem-core | Gains `cli.py`, `__main__.py`, and the console script |
| stem-service | Later steps import `stem_core` from the installed package |

## Consequences

**Positive:**
- `pip install .` gives the `stems` command.
- The command tests run with no model and no tool on the machine.

**Negative:**
- The root `pyproject.toml` now names one component's package. Later steps add their own packages there.
- The CI install step builds the package, so a packaging error fails CI.

**Risks:**
- Packaging settings may not match the `pythonpath` the tests use. CI runs both and shows a mismatch.

## Related ADRs

- ADR-0001 sets the tooling and layout.
- ADR-0002 sets the injected separator that `stems split` reuses.

## Supersedes

- None.

## Superseded By

- None.
