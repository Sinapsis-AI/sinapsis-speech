# -*- coding: utf-8 -*-
from elevenlabs_tts_app import ElevenlabsTTSApp
from sinapsis_core.utils.env_var_keys import AGENT_CONFIG_PATH, GRADIO_SHARE_APP, SINAPSIS_CACHE_DIR

CONFIG_PATH = (
    AGENT_CONFIG_PATH or "packages/sinapsis_elevenlabs/src/sinapsis_elevenlabs/configs/elevenlabs_voice_creation.yaml"
)
GENERIC_KEY = "ElevenLabsVoiceGeneration"

if __name__ == "__main__":
    """
    The main entry point for launching the ElevenLabs TTS application.

    Initializes an `ElevenlabsTTSApp` instance with the provided configuration file and framework name.
    Then launches the Gradio interface for text-to-speech conversion.
    """
    sinapsis_tts = ElevenlabsTTSApp(CONFIG_PATH, GENERIC_KEY, "Elevenlabs", "Voice Generation")
    sinapsis_tts().launch(share=GRADIO_SHARE_APP, allowed_paths=[SINAPSIS_CACHE_DIR])
