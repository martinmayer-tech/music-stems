# Build report - 0000016-docker-packaging

Run speed: standard.

## Phases

| Phase | Wall clock (minutes) | Agents | Model tier |
|-------|----------------------|--------|------------|
| P0: Discovery | 1 | 0 | primary |
| P1: Plan | 1 | 0 | primary |
| P2: Implement | 52 | 0 | primary |
| P3: Validate and Accept | 1 | 0 | primary |
| P4: Ship | 0 | 0 | primary |

Most of P2 went to waiting for the clean-clone runs of the pack suite. The baseline run and the full run took about 30 and 20 minutes.

## Parallelism

None. The four units run in order, as the plan states, because the compose file builds the image and the docs describe the finished files.

## Self-corrections

- The first image build failed because `diffq` has no wheel and needs `gcc`. Avoidable: yes, by a local build before the Dockerfile test. The agent added `gcc` to the install layer.
- The second build failed because `gcc` needs `libc6-dev` for `stdlib.h`. Avoidable: yes, by the same local build. The agent added the package.
- Two plan records failed the prose check on a passive verb or a long sentence. Avoidable: yes, by running `prose-check.mjs` before each commit.

## Improvement suggestions

- P0: the `gate-write` hook skips a component path with no slash, so a root file needed a `./` prefix. Backlog entry 0000024 holds the change.
- P2: build the image once before the first commit of a Dockerfile, because a test that reads text cannot show a missing compiler.
- P3: a job in the image fails on `audioread`. A run of one real job caught it. Backlog entry 0000023 holds the fix.

## Postmortems

Postmortems: none

Retrospective: `plan/retrospectives/0000016-docker-packaging-2026-11-16.md`

## Inherited failures

62 suites fail on the base commit. The list is in `baseline-failures.md` in this folder. The step files no backlog entry for them, because they predate the initiative.

## Workflow governance

| Metric | Value | Threshold | Result |
|--------|-------|-----------|--------|
| Rework loops per requirement (highest) | 0 | 2 | ok |
| `Blocked:` stops | 0 | 1 | ok |
| Mid-pipeline design changes | 0 | 1 | ok |
| Human corrections at gates | 0 | 2 | ok |
| Longest CI run (seconds) | 333 (run 43801776434) | 420 | ok |

Breaches: 0. The gate reports and does not block. Counts come from marker lines only.

## Dispatch by class and tier

| Class | Tier | Units | Rework |
|-------|------|-------|--------|
| content | inline | 4 | 0 |
