# Open Source Stem Separation Guide

**Date:** 2026-11-14
**Purpose:** Self-hosted, scriptable replacement for lalal.ai (non-commercial use)

## 1. The pick

**`audio-separator` (python-audio-separator) running a BS-Roformer model.**

- Highest-quality open models, exposed through a Python API and a CLI.
- No UI dependency, so you can build your own front end on top.
- Model files download automatically on first use.

## 2. Why not the others

| Option | Reason to skip |
|---|---|
| Raw Demucs | Original repo archived 2025-01-01; fork gets fixes only. Beaten on quality by Roformer models. |
| Ultimate Vocal Remover | Same models, but GUI-first. Unneeded if you build your own UI. |
| StemRoller / StemDeck | GUI wrappers; less control. |
| Spleeter | Older, lower quality. |

Quality evidence (SDR, higher is better):

- Published comparison: BS-RoFormer 11.99 dB average vs HT Demucs 9.27 dB.
- MVSEP Multisong, vocals: BS Roformer (viperx) 10.87 dB vs htdemucs_ft 8.33 dB.

## 3. Pipeline

```
mix
 └─► BS-Roformer ──► vocals
                 └─► instrumental
                       └─► htdemucs_ft ──► drums / bass / other   (optional)
```

- Pass 1 gives the best vocal/instrumental split.
- You only need pass 2 if you want drums, bass and other.
- Producers report the two-pass approach. No formal benchmark covers it. Test on your own material.

## 4. Requirements

- Python 3.10 or newer (avoid 3.14.1).
- FFmpeg on the path.
- Nvidia GPU strongly recommended for speed. CPU works but is slow.

## 5. Install

```bash
# Nvidia GPU (CUDA)
pip install "audio-separator[gpu]"

# CPU or Apple Silicon
pip install "audio-separator[cpu]"

# FFmpeg
sudo apt-get install -y ffmpeg     # Debian/Ubuntu
brew install ffmpeg                # macOS

# Verify the environment
audio-separator --env_info
```

A Docker image is also available if you prefer a container.

## 6. CLI usage

```bash
# Pass 1: vocals + instrumental
audio-separator mix.wav \
  --model_filename model_bs_roformer_ep_317_sdr_12.9755.ckpt \
  --output_dir ./out \
  --output_format WAV

# Pass 2: drums / bass / other from the instrumental
audio-separator "./out/<instrumental-file>.wav" \
  --model_filename htdemucs_ft.yaml \
  --output_dir ./out/stems \
  --output_format WAV
```

Useful flags:

- `--list_models` : show all supported models.
- `--list_filter=vocals --list_limit=5` : top models for a given stem.
- `--single_stem=Instrumental` : write one stem only.
- `--model_file_dir` : where the tool caches model files (default `/tmp/audio-separator-models/`). Set a persistent path.

Note: the CLI defaults to FLAC output and the Python class defaults to WAV. Set the format explicitly.

## 7. Python API

```python
from audio_separator.separator import Separator

MODELS = "/opt/models/audio-separator"

def split(mix_path: str, out_dir: str, full_stems: bool = False) -> list[str]:
    sep = Separator(
        output_dir=out_dir,
        output_format="WAV",
        model_file_dir=MODELS,
    )

    # Pass 1: vocals + instrumental
    sep.load_model(model_filename="model_bs_roformer_ep_317_sdr_12.9755.ckpt")
    outputs = sep.separate(
        mix_path,
        {"Vocals": "vocals", "Instrumental": "instrumental"},
    )
    if not full_stems:
        return outputs

    # Pass 2: drums / bass / other from the instrumental
    sep.load_model(model_filename="htdemucs_ft.yaml")
    stems = sep.separate(f"{out_dir}/instrumental.wav")
    return outputs + stems
```

Notes:

- `separate()` returns a list of output file paths.
- The second argument renames stems. Unnamed stems keep default names.
- Passing a list or folder runs a batch. Failures surface together as `BatchSeparationError`.
- Check whether returned paths are absolute or relative in your installed version before joining them.

## 8. Model choices

| Need | Model filename |
|---|---|
| Vocals / instrumental (default) | `model_bs_roformer_ep_317_sdr_12.9755.ckpt` |
| Drums / bass / other | `htdemucs_ft.yaml` |
| Guitar and piano as well | `htdemucs_6s.yaml` (those two stems are weaker) |
| Faster, lower quality 4-stem | `htdemucs.yaml` |

- Run `audio-separator -l --list_filter=vocals --list_limit=5` periodically. Newer Roformer checkpoints appear regularly.
- De-reverb and de-noise models are also available if you need clean-up passes.

## 9. Squeezing out more quality

- **Ensembles:** combine models with `-m` plus `--extra_models`, and choose a method with `--ensemble_algorithm`. Presets: `--list_presets`, `--ensemble_preset`.
- **Lossless in, lossless out:** feed WAV or FLAC, not MP3.
- **Listen as well as reading SDR:** models trade "fullness" against "bleed" differently.

## 10. Building your own service

- Load each model once per worker and reuse it. Model loading is the slow part.
- Queue jobs. Run one GPU job at a time per card unless VRAM allows more.
- Persist `model_file_dir` on a volume so containers do not re-download.
- Pin the `audio-separator` version. The API and defaults have changed between releases.

## 11. Sources

- audio-separator: https://pypi.org/project/audio-separator/
- Demucs (archived): https://github.com/facebookresearch/demucs
- MVSEP quality tables: https://www.mvsep.com/algorithms
- SDR comparison table: https://arxiv.org/pdf/2603.09187
