# Build report - 0000012-web-front-end

Run speed: standard.

## Phases

| Phase | Wall clock (minutes) | Agents | Model tier |
|-------|----------------------|--------|------------|
| P0 Discovery | 1 | 0 | primary |
| P1 Plan | 2 | 0 | primary |
| P2 Implement | 24 | 0 | primary |
| P3 Validate and Accept | 3 | 0 | primary |
| P4 Ship | 1 | 0 | primary |

Most of P2 went to waiting for the full pack suite in a clean clone, which took about 20 minutes.

## Parallelism

None. The four units edit the same files, so each waited for the one before it, as the plan states. The baseline run ran beside the P0 work.

## Self-corrections

- The REQ-003 polling test expected a literal `2000` and the script names it `POLL_MS`. Avoidable: yes, by testing the rule and not the spelling. Postmortem: `plan/postmortems/2026-11-16-page-tests-matched-source-text-too-tightly.md`.
- The REQ-004 done-branch test expected the `audio` element inside the branch, but a helper builds it. Avoidable: yes. Same postmortem.
- The wording allowlist suite flagged a banned word in two stem-web files. Avoidable: yes, by running the suite at the unit. Postmortem: `plan/postmortems/2026-11-16-banned-word-in-new-component-docs.md`.

## Improvement suggestions

- P0: the baseline recorder accepted output from a run that had not ended. Backlog entry 0000021 holds the fix.
- P1: the test impact scan could name the wording allowlist suite. Backlog entry 0000018 holds it.

## Postmortems

- `plan/postmortems/2026-11-16-page-tests-matched-source-text-too-tightly.md`
- `plan/postmortems/2026-11-16-banned-word-in-new-component-docs.md`

Retrospective: `plan/retrospectives/0000012-web-front-end-2026-11-16.md`

## Inherited failures

59 suites fail on the base commit. The list is in `baseline-failures.md` in this folder. The step files no backlog entry for them, because they predate the initiative.

## Workflow governance

| Metric | Value | Threshold | Result |
|--------|-------|-----------|--------|
| Rework loops per requirement (highest) | 1 (REQ-003) | 2 | ok |
| `Blocked:` stops | 0 | 1 | ok |
| Mid-pipeline design changes | 0 | 1 | ok |
| Human corrections at gates | 0 | 2 | ok |
| Longest CI run (seconds) | 0 | 420 | ok |

Breaches: 0. The gate reports and does not block. Counts come from marker lines only.

## Dispatch by class and tier

| Class | Tier | Units | Rework |
|-------|------|-------|--------|
| content | inline | 4 | 0 |
| unclassified | unclassified | 0 | 2 |
