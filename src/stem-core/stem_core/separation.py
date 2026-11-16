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

SIX_STEM_MODEL = "htdemucs_6s.yaml"
SIX_STEM_EXTRAS = {"Guitar": "guitar", "Piano": "piano"}
PASS_TWO_MODELS = (FULL_STEMS_MODEL, SIX_STEM_MODEL, "htdemucs.yaml")
# The presets of audio-separator 0.48.0, from its ensemble_presets.json.
ENSEMBLE_PRESETS = (
    "instrumental_clean",
    "instrumental_full",
    "instrumental_balanced",
    "instrumental_low_resource",
    "vocal_balanced",
    "vocal_clean",
    "vocal_full",
    "vocal_rvc",
    "karaoke",
)
SINGLE_STEMS = PASS_ONE_KEPT + PASS_TWO_KEPT + tuple(SIX_STEM_EXTRAS.values())


def resolve_model_dir() -> str:
    """Return the model folder from STEMS_MODEL_DIR, or the default."""
    return os.environ.get(MODEL_DIR_VARIABLE) or DEFAULT_MODEL_DIR


def _reject(option: str, value: str, allowed: tuple[str, ...]) -> ValueError:
    return ValueError(f"unknown {option} {value!r}. Allowed values: {', '.join(allowed)}")


def validate_options(
    model: str | None = None,
    ensemble_preset: str | None = None,
    single_stem: str | None = None,
) -> None:
    """Raise ValueError for an option outside its allowlist. Load no model."""
    if model is not None and model not in PASS_TWO_MODELS:
        raise _reject("model", model, PASS_TWO_MODELS)
    if ensemble_preset is not None and ensemble_preset not in ENSEMBLE_PRESETS:
        raise _reject("ensemble preset", ensemble_preset, ENSEMBLE_PRESETS)
    if single_stem is not None:
        if single_stem not in SINGLE_STEMS:
            raise _reject("single stem", single_stem, SINGLE_STEMS)
        if single_stem in SIX_STEM_EXTRAS.values() and (model or FULL_STEMS_MODEL) != SIX_STEM_MODEL:
            raise ValueError(f"single stem {single_stem!r} needs the model {SIX_STEM_MODEL}")


def default_separator_factory(
    output_dir: str,
    output_format: str,
    model_file_dir: str,
    ensemble_preset: str | None = None,
) -> Any:
    """Build an audio-separator Separator. The import runs on the first call only."""
    from audio_separator.separator import Separator

    options: dict[str, Any] = {}
    if ensemble_preset is not None:
        options["ensemble_preset"] = ensemble_preset
    return Separator(
        output_dir=output_dir,
        output_format=output_format,
        model_file_dir=model_file_dir,
        **options,
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
    separator_factory: Callable[..., Any] | None = None,
    *,
    model: str | None = None,
    ensemble_preset: str | None = None,
    single_stem: str | None = None,
) -> list[str]:
    """Split a mix into stems and return absolute WAV paths.

    Pass 1 writes vocals and instrumental. With full_stems, pass 2 splits the
    instrumental into drums, bass, and other. The options pick the pass 2 model,
    a pass 1 ensemble preset, and the one stem to keep. A bad option raises
    ValueError before any model loads.
    """
    validate_options(model, ensemble_preset, single_stem)
    mix = Path(mix_path)
    if not mix.is_file():
        raise FileNotFoundError(f"mix file not found: {mix}")
    out = Path(out_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)

    pass_two_model = model or FULL_STEMS_MODEL
    pass_two_kept = PASS_TWO_KEPT
    pass_two_names = dict(PASS_TWO_NAMES)
    if pass_two_model == SIX_STEM_MODEL:
        pass_two_kept = PASS_TWO_KEPT + tuple(SIX_STEM_EXTRAS.values())
        pass_two_names.update(SIX_STEM_EXTRAS)
    if single_stem is None:
        run_pass_two = full_stems
    else:
        run_pass_two = single_stem not in PASS_ONE_KEPT

    factory = separator_factory or default_separator_factory
    if ensemble_preset is None:
        separator = factory(str(out), "WAV", resolve_model_dir())
    else:
        separator = factory(
            str(out), "WAV", resolve_model_dir(), ensemble_preset=ensemble_preset
        )

    separator.load_model(model_filename=VOCALS_MODEL)
    reported_first = separator.separate(str(mix), PASS_ONE_NAMES)
    first_by_stem = _by_stem([_absolute(p, out) for p in reported_first])
    missing_first = [name for name in PASS_ONE_KEPT if name not in first_by_stem]
    if missing_first:
        raise RuntimeError(f"pass 1 wrote no {', '.join(missing_first)} file")
    kept = {name: first_by_stem[name] for name in PASS_ONE_KEPT}
    if run_pass_two:
        instrumental = first_by_stem["instrumental"]
        if ensemble_preset is not None:
            separator = factory(str(out), "WAV", resolve_model_dir())
        separator.load_model(model_filename=pass_two_model)
        reported = separator.separate(str(instrumental), pass_two_names)
        second = _by_stem([_absolute(p, out) for p in reported])
        residual = second.pop(RESIDUAL_STEM, None)
        if residual is not None:
            residual.unlink(missing_ok=True)
        missing = [name for name in pass_two_kept if name not in second]
        if missing:
            raise RuntimeError(f"pass 2 wrote no {', '.join(missing)} file")
        kept.update({name: second[name] for name in pass_two_kept})
    if single_stem is not None:
        for name, path in kept.items():
            if name != single_stem:
                path.unlink(missing_ok=True)
        return [str(kept[single_stem])]
    return [str(path) for path in kept.values()]
