# Build report - 0000002-python-scaffold

Run speed: standard.

## Phases

| Phase | Wall clock (minutes) | Agents | Model tier |
|-------|----------------------|--------|------------|
| P0 Discovery | 2 | 0 | primary |
| P1 Plan | 1 | 0 | primary |
| P2 Implement | 41 | 0 | primary |
| P3 Validate and Accept | 21 | 0 | primary |
| P4 Ship | not recorded | 0 | primary |

## Parallelism

None. The four implement units were small and ran inline in plan order, which departs from the plan's two batches.

## Self-corrections

- The gate blocked root paths in the design. The plan could not have avoided it. The `./name` form fixed it.
- The wording allowlist test failed on the manifests. A test impact entry could have avoided it. Postmortem: `plan/postmortems/2026-11-15-manifest-wording-test.md`.

## Improvement suggestions

- P1: add a tracked-file cause to the test impact scan (backlog 0000018).
- P3: the clean-clone run repeats the P2 full run. Run it once when the tree has not changed.

## Inherited failures

57 suites fail on the base commit. The list is in `baseline-failures.md` in this folder. No backlog entry is filed for them, because they predate the initiative.

Retrospective: plan/retrospectives/0000002-python-scaffold-2026-11-15.md

## Workflow governance

| Metric | Value | Threshold | Result |
|--------|-------|-----------|--------|
| Rework loops per requirement (highest) | 0 | 2 | ok |
| `Blocked:` stops | 0 | 1 | ok |
| Mid-pipeline design changes | 0 | 1 | ok |
| Human corrections at gates | 0 | 2 | ok |
| Longest CI run (seconds) | 0 | 420 | ok |

Breaches: 0. The gate reports and does not block. Counts come from marker lines only.

## Dispatch by class and tier

| Class | Tier | Units | Rework |
|-------|------|-------|--------|
| content | inline | 4 | 0 |
