---
title: "Retrospective: 2026-11-16 - Stem separation service initiative"
summary: "A blameless review of a finished run or initiative, and the changes it files."
status: "open"  # open | closed
---
# Retrospective: 2026-11-16 - Stem separation service initiative

**Mode:** initiative
**Subject:** 0000001-stem-separation-service
**Date:** 2026-11-16

## Summary

The initiative shipped all 8 charted steps in one driver run of 7 hours 29 minutes, with no stop. Setting up the chart in a new consumer repo took more human answers than the 8 steps did.

## What helped

- One driver run merged every step with no `Blocked:` line and no resume (driver output, `Summary: merged this run: 1, 2, 3, 4, 5, 6, 7, 8` and `driver fixes: 0`).
- The `## Decisions` rows answered each fork a step met, so no step waited for the human (the step build logs in `plan/_archive/`, `Decision applied (initiative chart)` lines).
- The chart kept real models out of CI. Unit tests injected a fake separator, and the steps ran the real engine by hand (`plan/retrospectives/0000004-separation-core-2026-11-15.md`, section Keep).
- Step 8 ran one real job through the built image before its acceptance gate (`plan/retrospectives/0000016-docker-packaging-2026-11-16.md`, section Keep).

## What slowed the work

- Chart could not write `product.yml` or `ravintio-zero/version-files.txt`. `gate-write` needs a confirmed design, and Chart has none (`.claude/hooks/enforcement/gate-write.mjs`, commit `f5fe1b7`).
- The pack's version file list named the pack's own `component.yml`. The merge queue would have stopped on step 1 (`ravintio-zero/version-files.txt` before commit `f5fe1b7`).
- A PR into `main` with six commits failed `squash-before-main`, and a replacement PR followed (PR #1 and PR #2).
- The prose check blocked commits of setup-written files and of the generated backlog index (`plan/state/prose-baseline.json`, commit `40a2869`).
- Each step ran the pack suite in a clean clone two or three times. Each run took 20 to 30 minutes (the eight step retrospectives in `plan/retrospectives/`).

## Initiative questions

1. Charted versus shipped (steps, bumps, versions): the chart and the result match. All 8 steps shipped in chart order with a minor bump each. The tags run from `v0.1.0` to `v0.8.0`. The `## Merges` table in the archived `initiative.md` lists them.
2. Friction that repeated across steps: three kinds repeated.
   - The pack suite wait appeared in all 8 step retrospectives, with 57 to 59 inherited failures.
   - A subprocess test failed on `PYTHONPATH` in steps 3 and 4 (`plan/postmortems/2026-11-15-isolated-subprocess-test.md`, `plan/postmortems/2026-11-16-subprocess-import-without-pythonpath.md`).
   - `gate-write` blocked root paths in steps 1, 7, and 8 (`plan/backlog/0000024-gate-write-ignores-root-paths/entry.md`).
3. Each stop and how long each step took: no step stopped. The driver output gives these times from start to merge.

   | Step | Start | Merged | Minutes |
   |------|-------|--------|---------|
   | 1 | 20:52 | 22:00 | 68 |
   | 2 | 22:00 | 22:52 | 52 |
   | 3 | 22:53 | 23:53 | 60 |
   | 4 | 23:53 | 00:32 | 39 |
   | 5 | 00:32 | 01:29 | 57 |
   | 6 | 01:29 | 02:09 | 40 |
   | 7 | 02:09 | 03:06 | 57 |
   | 8 | 03:07 | 04:21 | 74 |

4. Initiative tooling gaps: four showed up.
   - Chart has no way to seed the version files in a new consumer repo.
   - The pack suite gives a consumer repo a long wait and no product signal.
   - Resume detection listed migrations 0007 and 0009 in every step, though neither applies (line 38 of each archived build log).
   - `initiative-activate.mjs` printed `checks failed on PR #4` while the checks were pending.

## Keep

- Take every likely fork as a `## Decisions` row at Chart. This run needed no human answer after activation (driver output, `driver fixes: 0`).
- Keep one step per component layer, in one lane. No step PR conflicted with another (the `## Merges` table in the archived `initiative.md`).

## Change

- Let Chart or Activate seed the version files in a new consumer repo (commit `f5fe1b7`).
- Give a consumer repo a short suite of its own (the eight step retrospectives).
- Record a `not applicable` migration so that resume detection stops listing it (line 38 of each archived build log).
- Make Activate wait for the first check before it watches (PR #4).

## Actions

| Change | Owner | Lives in | Verified by | Filed as |
|--------|-------|----------|-------------|----------|
| Seed the version files at Chart or Activate | Pack maintainer | `ravintio-zero/scripts/initiative-activate.mjs`, `ravintio-zero/version-files.txt` | A new consumer repo merges step 1 with no manual copy | [0000025](../backlog/0000025-chart-cannot-seed-version-files/entry.md) |
| Give a consumer repo a short suite | Pack maintainer | The pack test runner | A step's full suite ends in under 5 minutes with 0 inherited failures | [0000026](../backlog/0000026-pack-suite-cost-in-consumer-repo/entry.md) |
| Skip a migration that does not apply | Pack maintainer | `ravintio-zero/scripts/resume-detect.mjs`, `plan/state/migrations.md` | A step logs no `Migration pending:` line for 0007 or 0009 | [0000027](../backlog/0000027-resume-detect-ignores-applies-when/entry.md) |
| Wait for the first check in Activate | Pack maintainer | `ravintio-zero/scripts/initiative-activate.mjs` | Activation merges its PR in one run | [0000028](../backlog/0000028-activate-reports-pending-checks-as-failed/entry.md) |
