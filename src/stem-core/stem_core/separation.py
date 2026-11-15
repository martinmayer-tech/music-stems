"""The two-pass separation function."""

from __future__ import annotations

import os
from collections.abc import Callable
from pathlib import Path
from typing import Any

VOCALS_MODEL = "model_bs_roformer_ep_317_sdr_12.9755.ckpt"
FULL_STEMS_MODEL = "htdemucs_ft.yaml"
DEFAULT_MODEL_DIR = "./models"
MODEL_DIR_VARIABLE = "STEMS_MODEL_DIR"

PASS_ONE_NAMES = {"Vocals": "vocals", "Instrumental": "instrumental"}
PASS_ONE_KEPT = ("vocals", "instrumental")
RESIDUAL_STEM = "residual_vocals"
PASS_TWO_NAMES = {
    "Drums": "drums",
    "Bass": "bass",
    "Other": "other",
    "Vocals": RESIDUAL_STEM,
}
PASS_TWO_KEPT = ("drums", "bass", "other")


def resolve_model_dir() -> str:
    """Return the model folder from STEMS_MODEL_DIR, or the default."""
    return os.environ.get(MODEL_DIR_VARIABLE) or DEFAULT_MODEL_DIR


def default_separator_factory(output_dir: str, output_format: str, model_file_dir: str) -> Any:
    """Build an audio-separator Separator. The import runs on the first call only."""
    from audio_separator.separator import Separator

    return Separator(
        output_dir=output_dir,
        output_format=output_format,
        model_file_dir=model_file_dir,
    )


def _absolute(path: str, out_dir: Path) -> Path:
    """Return an absolute path for a file that a separator reported."""
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    in_out_dir = out_dir / candidate
    if in_out_dir.exists():
        return in_out_dir
    if candidate.exists():
        return candidate.resolve()
    return in_out_dir


def _by_stem(paths: list[Path]) -> dict[str, Path]:
    return {p.stem: p for p in paths}


def split(
    mix_path: str | os.PathLike[str],
    out_dir: str | os.PathLike[str],
    full_stems: bool = False,
    separator_factory: Callable[[str, str, str], Any] | None = None,
) -> list[str]:
    """Split a mix into stems and return absolute WAV paths.

    Pass 1 writes vocals and instrumental. With full_stems, pass 2 splits the
    instrumental into drums, bass, and other.
    """
    mix = Path(mix_path)
    if not mix.is_file():
        raise FileNotFoundError(f"mix file not found: {mix}")
    out = Path(out_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)

    factory = separator_factory or default_separator_factory
    separator = factory(str(out), "WAV", resolve_model_dir())

    separator.load_model(model_filename=VOCALS_MODEL)
    reported_first = separator.separate(str(mix), PASS_ONE_NAMES)
    first_by_stem = _by_stem([_absolute(p, out) for p in reported_first])
    missing_first = [name for name in PASS_ONE_KEPT if name not in first_by_stem]
    if missing_first:
        raise RuntimeError(f"pass 1 wrote no {', '.join(missing_first)} file")
    first = [first_by_stem[name] for name in PASS_ONE_KEPT]
    if not full_stems:
        return [str(p) for p in first]

    instrumental = first_by_stem["instrumental"]

    separator.load_model(model_filename=FULL_STEMS_MODEL)
    reported = separator.separate(str(instrumental), PASS_TWO_NAMES)
    second = _by_stem([_absolute(p, out) for p in reported])
    residual = second.pop(RESIDUAL_STEM, None)
    if residual is not None:
        residual.unlink(missing_ok=True)
    missing = [name for name in PASS_TWO_KEPT if name not in second]
    if missing:
        raise RuntimeError(f"pass 2 wrote no {', '.join(missing)} file")
    return [str(p) for p in first] + [str(second[name]) for name in PASS_TWO_KEPT]
