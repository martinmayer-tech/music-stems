# stem-core: purpose

stem-core holds the two-pass separation function and the `stems` command. Both exist.

`split(mix_path, out_dir, full_stems=False)` splits a mix into stems with `audio-separator`. The service and the command line call it. Three optional arguments pick the pass 2 model, a pass 1 ensemble preset, and one stem to keep. The component rejects any value outside its allowlists.

The `stems` command has three subcommands. `stems split FILE` prints one output path per line. `stems env` reports the Python version, FFmpeg, and the device. `stems models` lists the models that `split()` uses and the allowed option values.

This component owns no data, so it has no data contract.
