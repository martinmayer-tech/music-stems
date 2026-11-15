"""Real-model smoke test (REQ-003). Run it with `pytest -m slow`."""

import math
import struct
import wave
from pathlib import Path

import pytest
from stem_core import split

pytestmark = pytest.mark.slow


def write_mix(path: Path, seconds: int = 3, rate: int = 44100) -> None:
    frames = bytearray()
    for i in range(seconds * rate):
        value = int(12000 * math.sin(2 * math.pi * 220 * i / rate))
        frames += struct.pack("<hh", value, value)
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(2)
        handle.setsampwidth(2)
        handle.setframerate(rate)
        handle.writeframes(bytes(frames))


def frames(path: Path) -> int:
    with wave.open(str(path), "rb") as handle:
        return handle.getnframes()


def peak(path: Path) -> int:
    with wave.open(str(path), "rb") as handle:
        data = handle.readframes(handle.getnframes())
    samples = struct.unpack(f"<{len(data) // 2}h", data)
    return max(abs(s) for s in samples)


def test_req_003_real_model_writes_vocals_and_instrumental_with_sound(tmp_path):
    pytest.importorskip("audio_separator")
    mix = tmp_path / "mix.wav"
    write_mix(mix)
    result = split(mix, tmp_path / "out")
    assert len(result) == 2
    names = {Path(p).name for p in result}
    assert names == {"vocals.wav", "instrumental.wav"}
    by_name = {Path(p).name: Path(p) for p in result}
    assert all(frames(p) > 0 for p in by_name.values())
    # A pure tone has no voice, so only the instrumental must hold sound.
    assert peak(by_name["instrumental.wav"]) > 0
