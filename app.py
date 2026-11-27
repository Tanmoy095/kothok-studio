"""Kothok browser UI entry point."""

from __future__ import annotations

import os

from core.engines.mock import MockEngine

# Gradio's anonymous analytics conflicts with Kothok's offline privacy promise.
os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"


def build_ui():
    """Build the starter UI around the offline mock until a verified engine lands."""
    import gradio as gr

    engine = MockEngine()

    def render(text: str) -> str:
        if not text.strip():
            raise gr.Error("Enter Bangla text to create a synthetic preview.")
        path = "output/mock-preview.wav"
        from pathlib import Path

        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_bytes(engine.speak(text, None, {}))
        return path

    with gr.Blocks(title="Kothok — Bangla Voice Studio") as ui:
        gr.Markdown(
            "# Kothok · Bangla Voice Studio\n"
            "Offline scaffold preview (synthetic tone only)."
        )
        text = gr.Textbox(label="Bangla text", lines=4)
        button = gr.Button("Create synthetic preview", variant="primary")
        audio = gr.Audio(label="Preview", type="filepath")
        button.click(render, inputs=text, outputs=audio)
    return ui


if __name__ == "__main__":
    build_ui().queue().launch(server_name="127.0.0.1", share=False, inbrowser=True)
