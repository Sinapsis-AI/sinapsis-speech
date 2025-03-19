# -*- coding: utf-8 -*-

from helpers.base_tts_app import BaseTTSApp
from sinapsis_core.data_containers.data_packet import DataContainer
from sinapsis_core.utils.env_var_keys import AGENT_CONFIG_PATH, GRADIO_SHARE_APP, SINAPSIS_CACHE_DIR

CONFIG_PATH = AGENT_CONFIG_PATH or "packages/sinapsis_elevenlabs/src/sinapsis_elevenlabs/configs/elevenlabs_tts.yaml"
GENERIC_KEY = "ElevenLabsTTS"


class ElevenlabsTTSApp(BaseTTSApp):
    """
    A subclass of BaseTTSApp for implementing text-to-speech functionality using ElevenLabs.

    This class overrides the abstract methods from BaseTTSApp to provide specific preprocessing
    and postprocessing steps for the ElevenLabs TTS application.
    """

    @staticmethod
    def _postprocess_output(container: DataContainer, generic_key: str | None) -> str | None:
        """
        Post-processes the output of the ElevenLabs TTS agent to extract the audio file path.

        This method checks the `generic_data` of the provided container to find the audio file path
        associated with the given `generic_key`. If the key is found and the audio path exists,
        it is returned. Otherwise, `None` is returned.

        Args:
            container (DataContainer): The container returned by the TTS agent containing the output
                                       data, including the audio file path stored under the `generic_key`.
            generic_key (str | None): An optional key used to retrieve the audio path from the `generic_data`
                                      of the container.

        Returns:
            str | None: The path to the generated audio file if the key exists and contains the audio path;
                        otherwise, None if no valid path is found.
        """
        audio_path = container.generic_data.get(generic_key, None)
        return audio_path[0] if audio_path else audio_path


if __name__ == "__main__":
    """
    The main entry point for launching the ElevenLabs TTS application.

    Initializes an `ElevenlabsTTSApp` instance with the provided configuration file and framework name.
    Then launches the Gradio interface for text-to-speech conversion.
    """
    sinapsis_tts = ElevenlabsTTSApp(CONFIG_PATH, GENERIC_KEY, "Elevenlabs")
    sinapsis_tts().launch(share=GRADIO_SHARE_APP, allowed_paths=[SINAPSIS_CACHE_DIR])
