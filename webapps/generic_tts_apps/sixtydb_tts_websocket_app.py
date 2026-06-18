# -*- coding: utf-8 -*-

import gradio as gr
from sinapsis.webapp.agent_gradio_helper import css_header
from sinapsis.webapp.tts_base import TTSAppAudioFromGeneric
from sinapsis_core.utils.env_var_keys import AGENT_CONFIG_PATH, GRADIO_SHARE_APP, SINAPSIS_CACHE_DIR
from sixtydb_helpers import add_logos_and_title

CONFIG_PATH = (
    AGENT_CONFIG_PATH or "packages/sinapsis_60db/src/sinapsis_60db/configs/sixtydb_tts_websocket_demo.yaml"
)
GENERIC_KEY = "SixtyDBTTSWebSocket"


class SixtyDBTTSWebSocketApp(TTSAppAudioFromGeneric):
    def __call__(self) -> gr.Blocks:
        with gr.Blocks(css=css_header()) as tts_interface:
            add_logos_and_title(f"Sinapsis {self.framework} {self.task} demo")
            self.inner_tts_functionality()
        return tts_interface


if __name__ == "__main__":
    """Launches the 60dB websocket TTS application via Gradio."""
    sinapsis_tts = SixtyDBTTSWebSocketApp(CONFIG_PATH, GENERIC_KEY, "60dB")
    sinapsis_tts.launch(share=GRADIO_SHARE_APP, allowed_paths=[SINAPSIS_CACHE_DIR])
