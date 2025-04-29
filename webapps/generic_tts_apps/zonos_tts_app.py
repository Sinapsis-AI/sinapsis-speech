# -*- coding: utf-8 -*-

from sinapsis.webapp.tts_base import TTSAppAudioFromGeneric
from sinapsis_core.utils.env_var_keys import AGENT_CONFIG_PATH, GRADIO_SHARE_APP, SINAPSIS_CACHE_DIR

CONFIG_PATH = AGENT_CONFIG_PATH or "packages/sinapsis_zonos/src/sinapsis_zonos/configs/zonos_tts_demo.yaml"
GENERIC_KEY = "ZonosTTS"


if __name__ == "__main__":
    """
    Entry point for launching the Zonos TTS application.

    Initializes a `TTSAppAudioFromGeneric` instance with the specified configuration path,
    generic app key, and the "Zonos" framework name. Then launches the Gradio interface
    for performing text-to-speech synthesis.

    The app can optionally be shared publicly, and access is restricted to the specified
    cache directory for security and file management.
    """
    sinapsis_tts = TTSAppAudioFromGeneric(CONFIG_PATH, GENERIC_KEY, "Zonos")
    sinapsis_tts().launch(share=GRADIO_SHARE_APP, allowed_paths=[SINAPSIS_CACHE_DIR])
