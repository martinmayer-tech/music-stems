# Build report - 0000010-http-api

Run speed: standard.

## Phases

| Phase | Wall clock (minutes) | Agents | Model tier |
|-------|----------------------|--------|------------|
| P0 Discovery | 11 | 0 | primary |
| P1 Plan | 2 | 0 | primary |
| P2 Implement | 33 | 0 | primary |
| P3 Validate and Accept | 1 | 0 | primary |
| P4 Ship | 0 | 0 | primary |

P0 includes the wait for the baseline suite to start. Most of P2 went to waiting for the full pack suite in a clean clone. The baseline run and the final run each took about 25 minutes, and they ran side by side.

## Parallelism

None. The four units were small and ran inline. Each unit waited for the one before it, as the plan states. The baseline run and the unit work ran side by side.

## Self-corrections

- The traversal test sent a plain `..` in a URL, and the HTTP client removed it before the request left. The step sent the name encoded as `%2e%2e`. Avoidable: yes, with a note in the testing standards. Postmortem: `plan/postmortems/2026-11-16-url-dot-segment-in-traversal-test.md`.

## Improvement suggestions

- P2: the testing standards could say how a test client rewrites a URL, and that a negative test needs a RED run that fails for the stated reason. Backlog entry 0000020 holds it.
- P0: the baseline run and the final run each take about 25 minutes. A filter for the suites that a step touches would shorten the loop.

## Postmortems

- `plan/postmortems/2026-11-16-url-dot-segment-in-traversal-test.md`

Retrospective: `plan/retrospectives/0000010-http-api-2026-11-16.md`

## Inherited failures

59 suites fail on the base commit. The list is in `baseline-failures.md` in this folder. The step files no backlog entry for them, because they predate the initiative.

## Workflow governance

| Metric | Value | Threshold | Result |
|--------|-------|-----------|--------|
| Rework loops per requirement (highest) | 1 (REQ-003) | 2 | ok |
| `Blocked:` stops | 0 | 1 | ok |
| Mid-pipeline design changes | 0 | 1 | ok |
| Human corrections at gates | 0 | 2 | ok |
| Longest CI run (seconds) | 131 (run 43785840591) | 420 | ok |

Breaches: 0. The gate reports and does not block. Counts come from marker lines only.

## Dispatch by class and tier

| Class | Tier | Units | Rework |
|-------|------|-------|--------|
| content | inline | 4 | 0 |
| unclassified | unclassified | 0 | 1 |
