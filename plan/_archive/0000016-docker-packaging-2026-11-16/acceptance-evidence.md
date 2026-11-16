## Acceptance evidence

- Checks: `ruff check .` exits 0. `pytest` gives 174 passed and 1 deselected. The full pack suite gives 0 new failures and 62 inherited failures. Self-corrections: 2, both for the image build (`gcc`, then `libc6-dev`).
- Security: no critical or high findings. One medium finding stays open by decision, because the service has no login. See `plan/current/security-report.md`.
- Execution: the CPU image built. The stack served the page and ran as a non-root user. It kept the job list and a model across a restart and a down and up. See `plan/current/verification-report.md`.
- Needs a human decision: a job fails in the image with `No module named 'audioread'`. The agent added no library the chart omits. Backlog entry 0000023 holds the fix, which the agent checked by hand.
- Not verified: the GPU image. No GPU host was available.
- CI criterion: the CPU image build counts as validated after the first CI run.
- Docs edit pass: `prose-check.mjs check` exits 0 on cycle 1.
