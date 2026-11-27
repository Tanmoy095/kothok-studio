"""Model-free checks for the scaffold engine."""

import wave
from pathlib import Path

from core.engines.mock import MockEngine, write_mock_sentence


def test_mock_engine_writes_short_wav_per_sentence(tmp_path: Path) -> None:
    result = write_mock_sentence(
        MockEngine(), "এটি একটি পরীক্ষা।", tmp_path / "folder with spaces" / "voice.wav"
    )

    assert result.is_file()
    with wave.open(str(result), "rb") as audio:
        assert audio.getnchannels() == 1
        assert audio.getframerate() == 24_000
        assert 0 < audio.getnframes() < audio.getframerate()
