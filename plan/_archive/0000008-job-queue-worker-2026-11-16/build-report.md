# Build report - 0000008-job-queue-worker

Run speed: standard.

## Phases

| Phase | Wall clock (minutes) | Agents | Model tier |
|-------|----------------------|--------|------------|
| P0 Discovery | 1 | 0 | primary |
| P1 Plan | 1 | 0 | primary |
| P2 Implement | 24 | 0 | primary |
| P3 Validate and Accept | 0 | 0 | primary |
| P4 Ship | 0 | 0 | primary |

Most of P2 went to waiting for the full pack suite in a clean clone. The baseline run and the final run each took about 25 minutes, and they ran side by side.

## Parallelism

None. The three units were small and ran inline. Unit U2-worker waited for U1-store, as the plan states. The baseline run and the unit work ran side by side.

## Self-corrections

- The import check ran a subprocess with no `PYTHONPATH`, so it failed on the import. The step passed the package folder in the child environment. The same failure hit step 3, and its postmortem filed no preventive action. Avoidable: yes, with a note in the testing standards. Postmortem: `plan/postmortems/2026-11-16-subprocess-import-without-pythonpath.md`.

## Improvement suggestions

- P2: the testing standards could say how a child process finds the packages under test. The gap repeated across two steps.
- P0: the baseline run and the final run each take about 25 minutes. A filter for the suites that a step touches would shorten the loop.

## Postmortems

- `plan/postmortems/2026-11-16-subprocess-import-without-pythonpath.md`

## Inherited failures

57 suites fail on the base commit. The list is in `baseline-failures.md` in this folder. The step files no backlog entry for them, because they predate the initiative.

CI duration: 144s for the run on the PR head, with all checks green.

## Workflow governance

| Metric | Value | Threshold | Result |
|--------|-------|-----------|--------|
| Rework loops per requirement (highest) | 1 (REQ-004) | 2 | ok |
| `Blocked:` stops | 0 | 1 | ok |
| Mid-pipeline design changes | 0 | 1 | ok |
| Human corrections at gates | 0 | 2 | ok |
| Longest CI run (seconds) | 144 (run 43780075147) | 420 | ok |

Breaches: 0. The gate reports and does not block. Counts come from marker lines only.

## Dispatch by class and tier

| Class | Tier | Units | Rework |
|-------|------|-------|--------|
| content | inline | 3 | 0 |
| unclassified | unclassified | 0 | 1 |

Retrospective: plan/retrospectives/0000008-job-queue-worker-2026-11-16.md
