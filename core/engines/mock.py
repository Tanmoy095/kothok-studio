"""Deterministic offline engine used to exercise the pipeline without a model."""

from __future__ import annotations

import math
import struct
import wave
from pathlib import Path


class MockEngine:
    """Write a brief synthetic tone for each request as a model-free stand-in."""

    sample_rate = 24_000

    def load(self) -> None:
        """No model is needed; the method keeps parity with real adapters."""

    def speak(self, text: str, reference: Path | None, params: dict[str, object]) -> bytes:
        """Return a WAV tone whose duration scales with text length."""
        del reference, params
        duration = min(0.8, max(0.15, len(text) * 0.015))
        frames = int(self.sample_rate * duration)
        samples = bytearray()
        for index in range(frames):
            envelope = min(1.0, index / 240, (frames - index) / 240)
            angle = 2 * math.pi * 440 * index / self.sample_rate
            value = int(2_000 * max(0.0, envelope) * math.sin(angle))
            samples.extend(struct.pack("<h", value))
        import io

        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as output:
            output.setnchannels(1)
            output.setsampwidth(2)
            output.setframerate(self.sample_rate)
            output.writeframes(samples)
        return buffer.getvalue()


def write_mock_sentence(engine: MockEngine, text: str, destination: Path) -> Path:
    """Persist one generated sentence for pipeline tests and demos."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(engine.speak(text, None, {}))
    return destination
