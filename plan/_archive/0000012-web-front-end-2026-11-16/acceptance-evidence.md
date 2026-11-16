## Acceptance evidence

- Checks: `ruff check .` exits 0. `pytest` gives 119 passed and 1 deselected. `pip-audit` reports no known vulnerabilities. The full pack suite gives 393 passed, 59 inherited failures, and 0 new failures. Self-corrections: 3.
- Security: no critical or high findings. One medium finding stays open by decision, because the service has no login. See `plan/current/security-report.md`.
- Execution: a browser run against a live service uploaded a file with the full stems option. The job reached `done`, and the page showed 5 players and 5 download links. One stem answered 200 with `audio/wav`. See `plan/current/verification-report.md`.
- Not run in a browser: the error text for a refused upload. A unit test covers it.
- Docs edit pass: `prose-check.mjs check` exits 0 on cycle 1.
- CI criteria: none for this step.
