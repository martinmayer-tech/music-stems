## Acceptance evidence

- Checks: `ruff check .` exits 0. `pytest` gives 156 passed and 1 deselected. `pip-audit` reports no known vulnerabilities. The full pack suite gives 394 passed, 61 inherited failures, and 0 new failures. Self-corrections: 2.
- Security: no critical or high findings. One medium finding stays open by decision, because the service has no login. See `plan/current/security-report.md`.
- Execution: a live service accepted a job with `htdemucs_6s.yaml` and full stems, and the job listed guitar and piano stems. A job with an unlisted model got 422 and loaded no model. A browser upload showed 7 players and 7 download links. See `plan/current/verification-report.md`.
- Not run with a real model: every preset and the real stem names. Fake separators cover them.
- Not run in a browser: the command flags. Unit tests cover them.
- Docs edit pass: `prose-check.mjs check` exits 0 on cycle 1.
- CI criteria: none for this step.
