# stem-core: interface contract

The `stem_core` package exposes `__version__` and `split`.

## `split(mix_path, out_dir, full_stems=False, separator_factory=None) -> list[str]`

| Argument | Meaning |
|----------|---------|
| `mix_path` | The audio file to split. A missing file raises `FileNotFoundError` before any model loads. |
| `out_dir` | The output folder. The function creates it when it does not exist. |
| `full_stems` | When `True`, a second pass splits the instrumental into drums, bass, and other. |
| `separator_factory` | A callable `(output_dir, output_format, model_file_dir)` that returns an object with `load_model` and `separate`. The default builds an `audio_separator` `Separator`. Tests pass a fake. |

The function returns absolute WAV paths in this order:

1. `vocals.wav`
2. `instrumental.wav`
3. With `full_stems`: `drums.wav`, `bass.wav`, and `other.wav`.

Pass 1 uses `model_bs_roformer_ep_317_sdr_12.9755.ckpt`. Pass 2 uses `htdemucs_ft.yaml`. Both write WAV.

## Settings

| Variable | Default | Meaning |
|----------|---------|---------|
| `STEMS_MODEL_DIR` | `./models` | The folder where `audio-separator` keeps downloaded models |

## The `stems` command

`pip install .` installs a `stems` console script. `python -m stem_core` runs the same `main()`. Both come from `stem_core.cli`.

| Subcommand | Behaviour | Exit code |
|------------|-----------|-----------|
| `stems split FILE [--output-dir DIR] [--full-stems]` | Calls `split()` and prints one absolute path per line to standard output. The output folder defaults to `./stems-out`. | 0 on success. 1 on any failure. |
| `stems env` | Prints `python: {version}`, `ffmpeg: {first line of ffmpeg -version, or not found}`, and `device: {cuda, mps, or cpu}`. | 0 |
| `stems models` | Prints `vocals-and-instrumental: {file}` and `drums-bass-other: {file}`. | 0 |

A failure prints one `stems: error: {message}` line to standard error and no traceback. A missing input file is a failure. A missing `audio_separator` package is a failure whose line names the `separation` extra. An argument error exits 2, as `argparse` does.

`stem_core.cli.main(argv=None, split_func=None, probes=None)` returns the exit code. Tests pass `split_func` and `probes` as fakes. `Probes` holds three functions: `python`, `ffmpeg`, and `device`.
