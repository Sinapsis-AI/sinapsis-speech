# -*- coding: utf-8 -*-

from sinapsis.webapp.tts_base import TTSAppAudioFromPacket
from sinapsis_core.utils.env_var_keys import (
    AGENT_CONFIG_PATH,
    GRADIO_SHARE_APP,
    SINAPSIS_CACHE_DIR,
)

CONFIG_PATH = AGENT_CONFIG_PATH or "packages/sinapsis_f5_tts/src/sinapsis_f5_tts/configs/f5_tts_app.yaml"
GENERIC_KEY = "F5TTSInference"


class F5TTSApp(TTSAppAudioFromPacket):
    """
    A specialized TTS application class for the F5TTS framework.

    Inherits from `TTSAppAudioFromPacket` and sets a base path for storing
    generated audio files within the Sinapsis cache directory.
    """

    BASE_AUDIO_PATH = f"{SINAPSIS_CACHE_DIR}/webapp/audios"


if __name__ == "__main__":
    """
    Entry point for launching the F5TTS application.

    Instantiates the `F5TTSApp` with the specified configuration and framework name,
    then launches the Gradio web interface for real-time text-to-speech conversion.

    The app can optionally be shared publicly and restricts file access to the
    designated Sinapsis cache directory.
    """
    sinapsis_tts = F5TTSApp(CONFIG_PATH, GENERIC_KEY, "F5TTS")
    sinapsis_tts().launch(share=GRADIO_SHARE_APP, allowed_paths=[SINAPSIS_CACHE_DIR])
