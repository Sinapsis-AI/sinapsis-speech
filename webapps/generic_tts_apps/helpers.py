# -*- coding: utf-8 -*-

import gradio as gr


def add_logos_and_title(page_title: str | None = None) -> None:
    logo_path = "https://github.com/Sinapsis-AI/brand-resources/blob/main/sinapsis_logo/4x/logo.png?raw=true"
    elevenlabs_logo_path = "https://storage.googleapis.com/eleven-public-cdn/images/elevenlabs-grants-logo.png"
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
            f'<a href="https://elevenlabs.io/text-to-speech" target="_blank">'
            f'<img src="{elevenlabs_logo_path}" alt="Text to Speech" style="height:50px;"></a>'
        )
    gr.Markdown("")
