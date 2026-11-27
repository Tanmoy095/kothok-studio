"""Checks the Gradio entry point can be built in the app environment."""

import gradio as gr

from app import build_ui


def test_build_ui_returns_gradio_blocks() -> None:
    assert isinstance(build_ui(), gr.Blocks)
