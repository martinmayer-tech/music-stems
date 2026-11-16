# stem-core: risk and scope

Risk level: medium. The fake separator in the unit tests can drift from the real one. The `slow` test covers the real output.

In scope: `split()`, the two models, WAV output, `STEMS_MODEL_DIR`, and the pinned `separation` extra.
Out of scope: the `stems` command, caller model choice, and ensembles. Step 3 and step 7 add them.
