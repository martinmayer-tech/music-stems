---
title: "Postmortem: 2026-11-16 - A traversal test sent a URL that the client rewrote"
summary: "The first stem test sent a plain `..` in a URL. The HTTP client removed it before the request left, so the test hit a different route. The test now sends the name encoded."
status: "closed"
---
# Postmortem: 2026-11-16 - A traversal test sent a URL that the client rewrote

> Path: `plan/postmortems/2026-11-16-url-dot-segment-in-traversal-test.md`. Written by `ravintio-postmortem`.

**Trigger:** P2 self-correction
**Feature:** 0000010-http-api
**Date:** 2026-11-16

## Summary

The test for REQ-003 asked for the stem name `..` with a plain URL. The HTTP client removed the dot segment, so the request reached `GET /jobs/{id}` and returned 200. The route was never at fault. The step changed the test to send `%2e%2e`.

## Timeline

| Time | Event | Evidence |
|------|-------|----------|
| 2026-11-16T00:47:09Z | The step wrote the stem tests, and the RED run failed 7 tests | build-log line `RED: U2-read` |
| 2026-11-16T00:47:22Z | After the routes existed, one test failed. The case with the name `..` got status 200 | `src/stem-service/tests/test_api_read.py`, `test_req_003_refuses_a_name_the_job_does_not_list` |
| 2026-11-16T00:47:22Z | The step sent the name encoded and added a comment that explains it | commit `1643082` |

First missed chance to catch it: the RED run. The `..` case sat among the 8 passing tests. A missing route also answers with an error. Nobody checked that each negative case failed for the stated reason.

## 5 whys

1. The test failed because the request for `..` returned status 200 and not 404.
2. The HTTP client removes dot segments from a URL path before it sends the request, so the path became `/jobs/{id}/`.
3. The test author assumed that the client sends the path as typed.
4. The RED run could not show it, because a missing route and a refused name both return an error status.
5. The testing standards give no guidance on how a client rewrites a URL in a path traversal test.

**Gap:** `ravintio-zero/standards/testing-standards.md` has no note that a test client normalises dot segments.

## Actions

| Type | Action | Status | Owner | Lives in | Verified by | Ref |
|------|--------|--------|-------|----------|-------------|-----|
| corrective | Send the traversal name encoded as `%2e%2e` | done | step 5 | `src/stem-service/tests/test_api_read.py` | `test_req_003_refuses_a_name_the_job_does_not_list` | commit 1643082 |
| preventive | Record the client behaviour in the component quirks, so the next test author sees it | done | step 5 | `src/stem-service/docs/quirks.md` | review of the quirks file | commit ea524cb |
| detective | none, because the test failed on its first GREEN run and showed the cause | none | none | none | none | none |
