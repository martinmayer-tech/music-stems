## Acceptance evidence

- Checks: `ruff check .` exits 0. `pytest` gives 180 passed and 1 deselected. The full pack suite gives 0 new failures and 61 inherited failures. Self-corrections: 0.
- Security: no critical or high findings. One medium finding is open and belongs to backlog entry 0000031. See `plan/current/security-report.md`.
- Execution: the CPU image built with no cache and holds `audioread` 3.1.0. The first job in a fresh stack ended `done` with `vocals.wav` and `instrumental.wav`, with no manual install. See `plan/current/verification-report.md`.
- Needs a human decision: every job after the first in one container loses its stems, because the reused separator keeps the first job's folder. This run did not cause the fault and does not fix it. Backlog entry 0000031 holds the detail at priority high.
- Not verified: the GPU image, and a full stems job from start to end.
- Docs edit pass: three changed docs, one cycle, and `prose-check.mjs check` exits 0.
