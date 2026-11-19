# Build report - 0000029-add-audioread

Run speed: standard.

## Phases

| Phase | Wall clock (minutes) | Agents | Model tier |
|-------|----------------------|--------|------------|
| P0: Discovery | 187 | 0 | primary |
| P1: Plan | 1 | 0 | primary |
| P2: Implement | 23 | 0 | primary |
| P3: Validate and Accept | 1 | 0 | primary |
| P4: Ship | 0 | 0 | primary |

Most of P0 went to waiting for the design confirmation. Most of P2 went to waiting for the clean-clone run of the pack suite. The image build and the real jobs ran during that wait.

## Parallelism

None. The docs unit describes the files of the pin unit, so the two ran in order.

## Self-corrections

None. One commit failed the prose check on a passive verb in the build log. Avoidable: yes, by running `prose-check.mjs` before the commit.

## Improvement suggestions

- P0: a light run for a filed entry could take the entry's observable condition as its acceptance check with no further question.
- P3: run several jobs in one container, not one. The second and third jobs exposed the fault in backlog entry 0000031.

## Postmortems

Postmortems: none

Retrospective: `plan/retrospectives/0000029-add-audioread-2026-11-18.md`

## Inherited failures

61 suites fail on the base commit. The list is in `baseline-failures.md` in this folder. The run files no backlog entry for them, because they belong to the pack. Backlog entry 0000026 covers the cost of that suite.

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
| content | inline | 2 | 0 |
