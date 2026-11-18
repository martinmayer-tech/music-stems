# Acceptance evidence - 0000006-command-line-interface

- Checks: `ruff check .` exits 0. `pytest` gives 38 passed and 1 deselected. The full pack suite gives 0 new failures and 57 inherited failures.
- Self-corrections: 1 (the subprocess test used `python -I`, which ignores `PYTHONPATH`).
- Security: no critical or high findings. Overall risk is low. See `plan/current/security-report.md`.
- Execution: the installed `stems` script ran `models`, `env`, and `split` on a missing file, which exited 1 with one error line. A fake-separator run printed 2 paths, and 5 with `--full-stems`.
- Not verified locally: the CI install on Python 3.12. The first CI run checks it.
- Docs edit pass: `prose-check.mjs` exits 0 on cycle 1. No subagent ran.
