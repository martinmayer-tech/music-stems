---
title: "Postmortem: 2026-11-16 - Two page tests matched the exact shape of the script"
summary: "Two tests for the page script failed on their first GREEN run because they matched code shape and not behaviour. Each test now checks the stated rule."
status: "closed"
---
# Postmortem: 2026-11-16 - Two page tests matched the exact shape of the script

> Path: `plan/postmortems/2026-11-16-page-tests-matched-source-text-too-tightly.md`. Written by `ravintio-postmortem`.

**Trigger:** P2 self-correction
**Feature:** 0000012-web-front-end
**Date:** 2026-11-16

## Summary

The tests for REQ-003 and REQ-004 read `app.js` as text. The REQ-003 test looked for a literal `2000` inside the timer call, but the script names the delay `POLL_MS`. The REQ-004 test looked for the `audio` element inside the done branch, but a helper builds it. Neither failure showed a defect in the page. Each test now checks the rule that its requirement states.

## Timeline

| Time | Event | Evidence |
|------|-------|----------|
| 2026-11-16T01:34:54Z | The REQ-003 polling test failed after the script existed | build-log line `Rework: REQ-003` |
| 2026-11-16T01:35:16Z | The REQ-004 done-branch test failed after the render code existed | build-log line `Rework: REQ-004` |
| 2026-11-16T01:35:16Z | The step changed both tests to check the constant, the timer call, and the one call site | `src/stem-web/tests/test_page_script.py`, `src/stem-web/tests/test_stem_links.py` |

First missed chance to catch it: the test design. The step has no browser test by decision, so both tests read source text. Nobody wrote down which text forms the script must keep.

## 5 whys

1. Each test failed because it expected one spelling of the code.
2. The test author wrote the expected text before the code existed.
3. The requirement states a behaviour, such as polling every two seconds, and not a spelling.
4. With no browser test, the only available check reads source text, which couples the test to spelling.
5. The testing standards give no guidance on how to test browser code without a browser.

**Gap:** `ravintio-zero/standards/testing-standards.md` has no rule for text-based checks of script code. It does not say to expose the logic as a pure function and run it under `node`.

## Actions

| Type | Action | Status | Owner | Lives in | Verified by | Ref |
|------|--------|--------|-------|----------|-------------|-----|
| corrective | Check the constant and the call site, and run `stemLinks` under `node` | done | step 6 | `src/stem-web/tests/test_page_script.py` | `test_req_003_script_reads_the_job_list_and_polls_every_two_seconds` | commit after 0000012 U2 |
| preventive | Record that script tests read text, so a rename needs a test change | done | step 6 | `src/stem-web/docs/test-coverage.md` | review of the coverage file | commit of U4-docs |
| detective | none, because both tests failed on their first GREEN run and showed the cause | none | none | none | none | none |
