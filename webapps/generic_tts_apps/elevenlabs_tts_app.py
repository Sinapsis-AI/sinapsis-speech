# -*- coding: utf-8 -*-

from sinapsis.webapp.tts_base import TTSAppAudioFromGeneric
from sinapsis_core.utils.env_var_keys import AGENT_CONFIG_PATH, GRADIO_SHARE_APP, SINAPSIS_CACHE_DIR

CONFIG_PATH = (
    AGENT_CONFIG_PATH or "packages/sinapsis_elevenlabs/src/sinapsis_elevenlabs/configs/elevenlabs_tts_demo.yaml"
)
GENERIC_KEY = "ElevenLabsTTS"


if __name__ == "__main__":
    """
        Launches the ElevenLabs TTS application via Gradio.

    Initializes a `TTSAppAudioFromGeneric` instance with the configuration file,
    a generic app key, and the framework name ("Elevenlabs"), then starts the
    Gradio web interface for text-to-speech conversion.

    The app can optionally be shared publicly and limits file access to the cache directory.
        """
    sinapsis_tts = TTSAppAudioFromGeneric(CONFIG_PATH, GENERIC_KEY, "ElevenLabs")
    sinapsis_tts().launch(share=GRADIO_SHARE_APP, allowed_paths=[SINAPSIS_CACHE_DIR])
