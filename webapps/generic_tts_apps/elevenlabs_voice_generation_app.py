# -*- coding: utf-8 -*-
from typing import Any

import gradio as gr
from helpers import add_logos_and_title
from sinapsis.webapp.agent_gradio_helper import css_header
from sinapsis.webapp.tts_base import TTSAppAudioFromGeneric
from sinapsis_core.data_containers.data_packet import DataContainer, TextPacket
from sinapsis_core.utils.env_var_keys import (
    AGENT_CONFIG_PATH,
    GRADIO_SHARE_APP,
    SINAPSIS_CACHE_DIR,
)

CONFIG_PATH = (
    AGENT_CONFIG_PATH or "packages/sinapsis_elevenlabs/src/sinapsis_elevenlabs/configs/voice_generation_demo.yaml"
)
GENERIC_KEY = "ElevenLabsVoiceGeneration"


class ElevenLabsTTSAppWithVoiceDescription(TTSAppAudioFromGeneric):
    def text_to_speech(
        self,
        initialized: bool,
        voice_description: str,
        text_to_convert: str,
    ) -> tuple[Any | None, str | None]:
        if initialized:
            if len(voice_description) < 20 or len(text_to_convert) < 100:
                gr.Warning(
                    "The voice description and text to convert must be atleast 20 and 100 characters long respectively."
                )
                return None, "Please provide a valid voice description and text to convert"
            self.agent.update_template_attribute(f"{GENERIC_KEY}", "voice_description", voice_description)
            container = DataContainer(texts=[TextPacket(content=text_to_convert)])
            output_container = self.agent(container)
            audio_path = self._postprocess_output(output_container, self.generic_key_or_base_path)
            if audio_path:
                return gr.Audio(audio_path, visible=True), None
            raise gr.Error("Unable to generate speech")
        return None, "#### Model not ready! Please wait..."

    def inner_tts_functionality(self) -> None:
        initialized_state = gr.State(True)

        voice_description = gr.Textbox(
            label="Voice description:",
            value=(
                "A clear and professional British middle-aged male voice, smooth and well-spoken. "
                "Perfect for narrations, audiobooks, and corporate content, offering a balanced and engaging delivery."
            ),
        )
        text_to_convert = gr.Textbox(
            submit_btn=True,
            label="Text to convert:",
            value=(
                "The Sinapsis platform aims to democratize artificial intelligence by offering a flexible template "
                "system that ensures modularity and compatibility between models and tools widely used by the community"
            ),
        )
        status_msg = gr.Markdown("#### Initializing model...")
        initialized_state.change(self.update_status_msg, outputs=[status_msg])

        audio_generated = gr.Audio(label="Audio generated:", visible=False)

        text_to_convert.submit(
            self.text_to_speech,
            inputs=[initialized_state, voice_description, text_to_convert],
            outputs=[audio_generated, status_msg],
        )

    def __call__(self) -> gr.Blocks:
        with gr.Blocks(css=css_header()) as tts_interface:
            add_logos_and_title("Sinapsis ElevenLabs Voice Generation demo")
            self.inner_tts_functionality()
        return tts_interface


if __name__ == "__main__":
    """
    The main entry point for launching the ElevenLabs TTS application.

    Initializes an `ElevenlabsTTSApp` instance with the provided configuration file and framework name.
    Then launches the Gradio interface for text-to-speech conversion.
    """
    sinapsis_tts = ElevenLabsTTSAppWithVoiceDescription(CONFIG_PATH, GENERIC_KEY, "ElevenLabs", "Voice Generation")
    sinapsis_tts.launch(share=GRADIO_SHARE_APP, allowed_paths=[SINAPSIS_CACHE_DIR])
