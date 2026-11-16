# stem-core: purpose

stem-core holds the two-pass separation function and the `stems` command. The function exists. Step 3 adds the command.

`split(mix_path, out_dir, full_stems=False)` splits a mix into stems with `audio-separator`. The service and the command line call it.

This component owns no data, so it has no data contract.
