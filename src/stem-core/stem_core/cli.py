"""The stems command: split a mix, report the environment, list the models."""

from __future__ import annotations

import argparse
import platform
import shutil
import subprocess
import sys
from collections.abc import Callable, Sequence
from typing import Any, NamedTuple

from stem_core.separation import (
    ENSEMBLE_PRESETS,
    FULL_STEMS_MODEL,
    PASS_TWO_MODELS,
    SINGLE_STEMS,
    VOCALS_MODEL,
)

DEFAULT_OUTPUT_DIR = "./stems-out"
FFMPEG_TIMEOUT_SECONDS = 10


class Probes(NamedTuple):
    """Functions that read one fact each about the machine. Tests inject fakes."""

    python: Callable[[], str]
    ffmpeg: Callable[[], str | None]
    device: Callable[[], str]


def probe_python() -> str:
    """Return the Python version."""
    return platform.python_version()


def probe_ffmpeg() -> str | None:
    """Return the first line of `ffmpeg -version`, or None when FFmpeg is absent."""
    binary = shutil.which("ffmpeg")
    if binary is None:
        return None
    try:
        result = subprocess.run(
            [binary, "-version"],
            capture_output=True,
            text=True,
            timeout=FFMPEG_TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    lines = result.stdout.splitlines()
    return lines[0] if lines else None


def probe_device() -> str:
    """Return cuda, mps, or cpu. The torch import runs here and never fails the command."""
    try:
        import torch

        if torch.cuda.is_available():
            return "cuda"
        mps = getattr(torch.backends, "mps", None)
        if mps is not None and mps.is_available():
            return "mps"
    except Exception:
        pass
    return "cpu"


DEFAULT_PROBES = Probes(python=probe_python, ffmpeg=probe_ffmpeg, device=probe_device)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="stems", description="Split a mix into stems.")
    sub = parser.add_subparsers(dest="command", required=True)

    split_parser = sub.add_parser("split", help="split a mix and print one output path per line")
    split_parser.add_argument("file", help="the audio file to split")
    split_parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help=f"the output folder (default: {DEFAULT_OUTPUT_DIR})",
    )
    split_parser.add_argument(
        "--full-stems",
        action="store_true",
        help="also split the instrumental into drums, bass, and other",
    )
    split_parser.add_argument(
        "--model",
        help=f"the pass 2 model, one of: {', '.join(PASS_TWO_MODELS)}",
    )
    split_parser.add_argument(
        "--ensemble-preset",
        help=f"the pass 1 ensemble preset, one of: {', '.join(ENSEMBLE_PRESETS)}",
    )
    split_parser.add_argument(
        "--single-stem",
        help=f"write only this stem and delete the others, one of: {', '.join(SINGLE_STEMS)}",
    )

    sub.add_parser("env", help="report the Python version, FFmpeg, and the device")
    sub.add_parser("models", help="list the models that split uses")
    return parser


def _error(message: object) -> int:
    first_line = (str(message).splitlines() or [""])[0]
    print(f"stems: error: {first_line}", file=sys.stderr)
    return 1


def _run_split(args: argparse.Namespace, split_func: Callable[..., list[str]] | None) -> int:
    if split_func is None:
        from stem_core.separation import split as split_func
    try:
        options = {
            name: value
            for name, value in (
                ("model", args.model),
                ("ensemble_preset", args.ensemble_preset),
                ("single_stem", args.single_stem),
            )
            if value is not None
        }
        paths = split_func(args.file, args.output_dir, full_stems=args.full_stems, **options)
    except ModuleNotFoundError as error:
        return _error(f"{error}. Install the separation extra: pip install '.[separation]'")
    except Exception as error:
        return _error(error)
    for path in paths:
        print(path)
    return 0


def _run_env(probes: Probes) -> int:
    print(f"python: {probes.python()}")
    print(f"ffmpeg: {probes.ffmpeg() or 'not found'}")
    print(f"device: {probes.device()}")
    return 0


def _run_models() -> int:
    print(f"vocals-and-instrumental: {VOCALS_MODEL}")
    print(f"drums-bass-other: {FULL_STEMS_MODEL}")
    print(f"pass-2-models: {', '.join(PASS_TWO_MODELS)}")
    print(f"ensemble-presets: {', '.join(ENSEMBLE_PRESETS)}")
    print(f"single-stems: {', '.join(SINGLE_STEMS)}")
    return 0


def main(
    argv: Sequence[str] | None = None,
    split_func: Callable[..., list[str]] | None = None,
    probes: Probes | None = None,
) -> int:
    """Run the stems command and return its exit code."""
    args: Any = build_parser().parse_args(argv)
    if args.command == "split":
        return _run_split(args, split_func)
    if args.command == "env":
        return _run_env(probes or DEFAULT_PROBES)
    return _run_models()
