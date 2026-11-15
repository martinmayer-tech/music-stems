# stem-core: risk and scope

Risk level: medium. The fake separator in the unit tests can drift from the real one. The `slow` test covers the real output.

In scope: `split()`, the two models, WAV output, `STEMS_MODEL_DIR`, and the pinned `separation` extra.
In scope also: the `stems` command with `split`, `env`, and `models`, the console script, and `python -m stem_core`.
Out of scope: caller model choice and ensembles. Step 7 adds them and extends `stems models`.
