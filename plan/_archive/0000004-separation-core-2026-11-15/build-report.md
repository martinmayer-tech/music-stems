# Build report - 0000004-separation-core

Run speed: standard.

## Phases

| Phase | Wall clock (minutes) | Agents | Model tier |
|-------|----------------------|--------|------------|
| P0 Discovery | 1 | 0 | primary |
| P1 Plan | 1 | 0 | primary |
| P2 Implement | 39 | 0 | primary |
| P3 Validate and Accept | 0 | 0 | primary |
| P4 Ship | 1 | 0 | primary |

## Parallelism

None. The four units were small and ran inline in plan order, which departs from the plan's three batches.

## Self-corrections

- The real separator listed the instrumental first. A real-library run in P1 or early P2 could have caught it. Postmortem: `plan/postmortems/2026-11-15-real-separator-differences.md`.
- The vocals stem of a pure tone is silent, so the real-model test checks sound in the instrumental only. The plan could not have avoided it.

## Improvement suggestions

- P0: the baseline run read a partial output and recorded no failures. The agent re-recorded it from a finished run of the base commit.
- P2: run the real model once while the code takes shape, when unit tests inject a fake.

## Inherited failures

57 suites fail on the base commit. The list is in `baseline-failures.md` in this folder. No backlog entry is filed for them, because they predate the initiative.

Retrospective: plan/retrospectives/0000004-separation-core-2026-11-15.md
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
