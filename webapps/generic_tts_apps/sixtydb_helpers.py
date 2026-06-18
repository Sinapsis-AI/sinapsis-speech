# -*- coding: utf-8 -*-

import gradio as gr


def add_logos_and_title(page_title: str | None = None) -> None:
    logo_path = "https://github.com/Sinapsis-AI/brand-resources/blob/main/sinapsis_logo/4x/logo.png?raw=true"
    with gr.Row():
        gr.Image(
            logo_path,
            elem_id="sinapsis-logo",
            height=50,
            show_label=False,
            show_download_button=False,
            show_fullscreen_button=False,
            scale=1,
        )
        gr.Markdown(f"# {page_title}", elem_id="title")
        gr.HTML(
            '<a href="https://60db.ai" target="_blank" '
            'style="font-size:24px;font-weight:bold;text-decoration:none;">60dB</a>'
        )
    gr.Markdown("")
