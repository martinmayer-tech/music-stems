# Acceptance evidence - 0000004-separation-core

- Checks: `ruff check .` exits 0. `pytest` gives 21 passed and 1 deselected. The full pack suite gives 0 new failures and 57 inherited failures.
- Self-corrections: 2 (path order from the real separator, and the silent vocals of a pure tone).
- Security: no critical or high findings. Overall risk is low. See `plan/current/security-report.md`.
- Execution: the real models ran on Python 3.13. `split` returned 2 paths, and 5 with `full_stems=True`.
- Not verified locally: the CI install on Python 3.12. The first CI run checks it.
- Docs edit pass: `prose-check.mjs` exits 0 on cycle 1. No subagent ran.
