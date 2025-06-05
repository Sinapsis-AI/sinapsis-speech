# -*- coding: utf-8 -*-

import gradio as gr
from helpers import add_logos_and_title
from sinapsis.webapp.agent_gradio_helper import css_header
from sinapsis.webapp.tts_base import TTSAppAudioFromGeneric
from sinapsis_core.utils.env_var_keys import AGENT_CONFIG_PATH, GRADIO_SHARE_APP, SINAPSIS_CACHE_DIR

CONFIG_PATH = (
    AGENT_CONFIG_PATH or "packages/sinapsis_elevenlabs/src/sinapsis_elevenlabs/configs/elevenlabs_tts_demo.yaml"
)
GENERIC_KEY = "ElevenLabsTTS"


class ElevenLabsTTSApp(TTSAppAudioFromGeneric):
    def __call__(self) -> gr.Blocks:
        with gr.Blocks(css=css_header()) as tts_interface:
            add_logos_and_title(f"Sinapsis {self.framework} {self.task} demo")
            self.inner_tts_functionality()
        return tts_interface


if __name__ == "__main__":
    """
    Launches the ElevenLabs TTS application via Gradio.

    Initializes a `TTSAppAudioFromGeneric` instance with the configuration file,
    a generic app key, and the framework name ("Elevenlabs"), then starts the
    Gradio web interface for text-to-speech conversion.

    The app can optionally be shared publicly and limits file access to the cache directory.
    """
    sinapsis_tts = ElevenLabsTTSApp(CONFIG_PATH, GENERIC_KEY, "ElevenLabs")
    sinapsis_tts.launch(share=GRADIO_SHARE_APP, allowed_paths=[SINAPSIS_CACHE_DIR])
