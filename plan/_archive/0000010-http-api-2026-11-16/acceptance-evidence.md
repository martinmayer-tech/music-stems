# Acceptance evidence - 0000010-http-api

- Checks: `ruff check .` exits 0. `pytest` gives 102 passed and 1 deselected, with 38 new tests for the API. The full pack suite gives 0 new failures and 59 inherited failures.
- Self-corrections: 1. The first stem test sent `..` in a URL, and the HTTP client collapsed it. The test now sends it encoded as `%2e%2e`, and the route still looks every name up in the job's outputs.
- Security: no critical or high findings. Overall risk is medium, because the service has no login by decision. See `plan/current/security-report.md`. `pip-audit` reports no known vulnerabilities.
- Execution: a live uvicorn server on `127.0.0.1` took an upload and ran the job to `done` with a fake `split` function. All 5 stems downloaded as `audio/wav`. A `.txt` upload, an oversized upload, an unknown job, and an unknown stem returned 415, 413, 404, and 404. `python -m stem_service` bound to `127.0.0.1:8765` and answered `GET /jobs`.
- Not verified locally: the CI run on Python 3.12 with the new `service` extra, and a real `Separator` under the API. The first CI run checks the first. The `slow` test checks the second.
- Docs edit pass: `prose-check.mjs` exits 0 on cycle 1. No subagent ran.
