# Acceptance evidence - 0000008-job-queue-worker

- Checks: `ruff check .` exits 0. `pytest` gives 64 passed and 1 deselected. The full pack suite gives 0 new failures and 57 inherited failures.
- Self-corrections: 1 (the import check ran a subprocess with no `PYTHONPATH`).
- Security: no critical or high findings. Overall risk is low. See `plan/current/security-report.md`.
- Execution: a scratch run queued three jobs, mimicked a crash, recovered, and ran one worker. The jobs ran in turn, ended `done`, and loaded two models in total.
- Not verified locally: the CI run on Python 3.12, and a real `Separator` under the pool. The first CI run checks the first. The `slow` test checks the second.
- Docs edit pass: `prose-check.mjs` exits 0 on cycle 1. No subagent ran.
