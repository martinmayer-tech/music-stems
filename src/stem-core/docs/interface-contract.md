# stem-core: interface contract

The `stem_core` package exposes `__version__` and `split`.

## `split(mix_path, out_dir, full_stems=False, separator_factory=None, *, model=None, ensemble_preset=None, single_stem=None) -> list[str]`

| Argument | Meaning |
|----------|---------|
| `mix_path` | The audio file to split. A missing file raises `FileNotFoundError` before any model loads. |
| `out_dir` | The output folder. The function creates it when it does not exist. |
| `full_stems` | When `True`, a second pass splits the instrumental into drums, bass, and other. |
| `separator_factory` | A callable `(output_dir, output_format, model_file_dir)` that returns an object with `load_model` and `separate`. With a preset, `split()` also passes the keyword `ensemble_preset`. The default builds an `audio_separator` `Separator`. Tests pass a fake. |
| `model` | The pass 2 model. One of `htdemucs_ft.yaml` (the default), `htdemucs_6s.yaml`, or `htdemucs.yaml`. |
| `ensemble_preset` | A pass 1 ensemble preset of `audio-separator` 0.48.0. Pass 2 builds its own separator with no preset. |
| `single_stem` | The one stem to keep. `split()` deletes the other stem files and returns one path. A pass 2 stem runs pass 2 even when `full_stems` is `False`. |

The function returns absolute WAV paths in this order:

1. `vocals.wav`
2. `instrumental.wav`
3. With `full_stems`: `drums.wav`, `bass.wav`, and `other.wav`.

With `model` set to `htdemucs_6s.yaml`, pass 2 also writes `guitar.wav` and `piano.wav`, and the result lists them after `other.wav`.

Pass 1 uses `model_bs_roformer_ep_317_sdr_12.9755.ckpt`, or the models of the preset. Pass 2 uses `htdemucs_ft.yaml` unless `model` says otherwise. Both write WAV.

## Options

`stem_core.separation` holds the allowlists `PASS_TWO_MODELS`, `ENSEMBLE_PRESETS`, and `SINGLE_STEMS`. `validate_options(model=None, ensemble_preset=None, single_stem=None)` raises `ValueError` for a value outside its list. The message names the option, the value, and the allowed values. It also raises for `guitar` or `piano` with a model other than `htdemucs_6s.yaml`. `split()` calls it first, so no model loads for a bad value.

## Settings

| Variable | Default | Meaning |
|----------|---------|---------|
| `STEMS_MODEL_DIR` | `./models` | The folder where `audio-separator` keeps downloaded models |

## The `stems` command

`pip install .` installs a `stems` console script. `python -m stem_core` runs the same `main()`. Both come from `stem_core.cli`.

| Subcommand | Behaviour | Exit code |
|------------|-----------|-----------|
| `stems split FILE [--output-dir DIR] [--full-stems] [--model M] [--ensemble-preset P] [--single-stem S]` | Calls `split()` and prints one absolute path per line to standard output. The output folder defaults to `./stems-out`. The command passes an option to `split()` only when the user sets it. | 0 on success. 1 on any failure. |
| `stems env` | Prints `python: {version}`, `ffmpeg: {first line of ffmpeg -version, or not found}`, and `device: {cuda, mps, or cpu}`. | 0 |
| `stems models` | Prints `vocals-and-instrumental: {file}` and `drums-bass-other: {file}`. It then prints the lines `pass-2-models`, `ensemble-presets`, and `single-stems`, each with its allowed values. | 0 |

A failure prints one `stems: error: {message}` line to standard error and no traceback. A missing input file is a failure. A missing `audio_separator` package is a failure whose line names the `separation` extra. An argument error exits 2, as `argparse` does.

`stem_core.cli.main(argv=None, split_func=None, probes=None)` returns the exit code. Tests pass `split_func` and `probes` as fakes. `Probes` holds three functions: `python`, `ffmpeg`, and `device`.
