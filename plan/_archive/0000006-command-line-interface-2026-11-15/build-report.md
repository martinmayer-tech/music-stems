# Build report - 0000006-command-line-interface

Run speed: standard.

## Phases

| Phase | Wall clock (minutes) | Agents | Model tier |
|-------|----------------------|--------|------------|
| P0 Discovery | 1 | 0 | primary |
| P1 Plan | 1 | 0 | primary |
| P2 Implement | 48 | 0 | primary |
| P3 Validate and Accept | 0 | 0 | primary |
| P4 Ship | 0 | 0 | primary |

Most of P2 went to waiting for the full pack suite in a clean clone, which took about 28 minutes.

## Parallelism

None. The three units were small and ran inline. Unit U2-entry waited for U1-cli, as the plan states. The baseline run and the unit work ran side by side.

## Self-corrections

- The subprocess test ran Python with `-I`, which ignores `PYTHONPATH`. The step removed the flag. Postmortem: `plan/postmortems/2026-11-15-isolated-subprocess-test.md`.

## Improvement suggestions

- P2: the testing standards could note that `python -I` ignores `PYTHONPATH`. The cause was a gap in a standard.
- P0: the baseline run and the final run each take about 10 minutes or more. A filter for the suites that the step touches would shorten the loop.

## Inherited failures

57 suites fail on the base commit. The list is in `baseline-failures.md` in this folder. No backlog entry is filed for them, because they predate the initiative.

CI duration: 118s for the `python` job run, with all checks green.
## Workflow governance

| Metric | Value | Threshold | Result |
|--------|-------|-----------|--------|
| Rework loops per requirement (highest) | 1 (REQ-004) | 2 | ok |
| `Blocked:` stops | 0 | 1 | ok |
| Mid-pipeline design changes | 0 | 1 | ok |
| Human corrections at gates | 0 | 2 | ok |
| Longest CI run (seconds) | 118 (run 43776548959) | 420 | ok |

Breaches: 0. The gate reports and does not block. Counts come from marker lines only.

## Dispatch by class and tier

| Class | Tier | Units | Rework |
|-------|------|-------|--------|
| content | inline | 3 | 0 |
| unclassified | unclassified | 0 | 1 |

Retrospective: plan/retrospectives/0000006-command-line-interface-2026-11-15.md
