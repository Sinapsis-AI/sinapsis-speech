# -*- coding: utf-8 -*-

from sinapsis.webapp.tts_base import TTSAppAudioFromPacket
from sinapsis_core.utils.env_var_keys import (
    AGENT_CONFIG_PATH,
    GRADIO_SHARE_APP,
    SINAPSIS_CACHE_DIR,
)

CONFIG_PATH = AGENT_CONFIG_PATH or "packages/sinapsis_orpheus_cpp/src/sinapsis_orpheus_cpp/configs/orpheus_tts_app.yaml"
BASE_AUDIO_PATH = f"{SINAPSIS_CACHE_DIR}/webapp/audios"

if __name__ == "__main__":
    """
    Entry point for launching the F5TTS application.

    Instantiates the `TTSAppAudioFromPacket` with the specified configuration and framework name,
    then launches the Gradio web interface for real-time text-to-speech conversion.

    The app can optionally be shared publicly and restricts file access to the
    designated Sinapsis cache directory.
    """
    sinapsis_tts = TTSAppAudioFromPacket(CONFIG_PATH, BASE_AUDIO_PATH, "OrpheusTTS")
    sinapsis_tts.launch(share=GRADIO_SHARE_APP, allowed_paths=[SINAPSIS_CACHE_DIR])
