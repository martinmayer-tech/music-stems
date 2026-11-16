# Build report - 0000014-model-ensemble-options

Run speed: standard.

## Phases

| Phase | Wall clock (minutes) | Agents | Model tier |
|-------|----------------------|--------|------------|
| P0: Discovery | 11 | 0 | primary |
| P1: Plan | 0 | 0 | primary |
| P2: Implement | 30 | 0 | primary |
| P3: Validate and Accept | 1 | 0 | primary |
| P4: Ship | 0 | 0 | primary |

Most of P2 went to waiting for the full pack suite in a clean clone, which took about 22 minutes.

## Parallelism

None. The five units run in order, as the plan states, because later units import the allowlists or describe the finished code.

## Self-corrections

- A line in `separation.py` ran over the lint limit. Avoidable: yes, by running `ruff check` at the unit. The agent fixed it in the next commit.
- The existing `stems models` test counted exactly two lines and failed when the listing grew. Avoidable: yes, if the test impact scan looked for output counts. Backlog entry 0000022 holds the change.
- Several plan records failed the prose check on a passive verb or a long sentence. Avoidable: yes, by running `prose-check.mjs` before each commit.

## Improvement suggestions

- P1: the test impact scan could name tests that count the lines of a listing. Backlog entry 0000022 holds it.
- P2: the docs unit had no RED line. A test of the docs would have given one at the unit.

## Postmortems

Postmortems: none

Retrospective: `plan/retrospectives/0000014-model-ensemble-options-2026-11-16.md`

## Inherited failures

61 suites fail on the base commit. The list is in `baseline-failures.md` in this folder. The step files no backlog entry for them, because they predate the initiative.

## Workflow governance

| Metric | Value | Threshold | Result |
|--------|-------|-----------|--------|
| Rework loops per requirement (highest) | 0 | 2 | ok |
| `Blocked:` stops | 0 | 1 | ok |
| Mid-pipeline design changes | 0 | 1 | ok |
| Human corrections at gates | 0 | 2 | ok |
| Longest CI run (seconds) | 166 (run 43795218773) | 420 | ok |

Breaches: 0. The gate reports and does not block. Counts come from marker lines only.

## Dispatch by class and tier

| Class | Tier | Units | Rework |
|-------|------|-------|--------|
| content | inline | 5 | 0 |
