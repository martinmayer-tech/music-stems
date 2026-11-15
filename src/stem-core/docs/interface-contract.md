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

Later steps add the `stems` command.
