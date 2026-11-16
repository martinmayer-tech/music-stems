---
title: "Verification Report - 0000012-web-front-end"
summary: "What the agent ran and observed for each acceptance criterion."
---
# Verification Report - 0000012-web-front-end

## Setup

The agent started `create_app()` under uvicorn on `127.0.0.1:8765` with a fake `split` function and an empty data folder. It opened the page in a browser, uploaded a WAV file, and ticked the full stems box.

## Criteria

| Criterion | Method | Outcome | Evidence |
|-----------|--------|---------|----------|
| `GET /` returns the page | `curl` and a browser load | verified | Status 200 with `text/html`. The page title read "Stem separation". The only console error was a 404 for `/favicon.ico` |
| The page uploads a file with the full stems option | Browser click-through | verified | The status line read "The job is queued." and `GET /jobs` held one job with `full_stems` true |
| The page polls a job until it is `done` or `failed` | Browser click-through | verified | The job list moved to `done` with no reload |
| A finished job shows one player and one download link per stem | Browser DOM count | verified | 5 `audio` elements and 5 `a[download]` links for 5 stems. `GET` of one stem returned 200 with `audio/wav` |
| The empty list reads "No jobs yet." | Browser load | verified | The snapshot held that list item |
| The API refuses a bad upload and the page shows the detail text | Unit test only | verified by test | `test_req_002_script_shows_the_error_detail_with_text_content` reads the script. No browser run observed it |

## Notes

The service has no favicon route. The 404 is harmless and out of scope.
