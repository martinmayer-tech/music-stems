# stem-core: risk and scope

Risk level: medium. The fake separator in the unit tests can drift from the real one. The `slow` test covers the real output.

In scope: `split()`, the two models, WAV output, `STEMS_MODEL_DIR`, and the pinned `separation` extra.
In scope also: the `stems` command with `split`, `env`, and `models`, the console script, and `python -m stem_core`.
In scope also: the model options, which are the pass 2 model, the ensemble preset, and the single stem.
Out of scope: a pass 1 model choice, a free model name, and a model upload.

Risks of the options:

- A preset may change the pass 1 stem names, so `split()` finds no vocals file. The job then fails with the error that names the file.
- A single stem deletes the other stems. The option names the stem to keep.
