# -*- coding: utf-8 -*-
"""Text-To-Speech template for ElevenLabs Voice Cloning."""

from elevenlabs import Voice
from sinapsis_core.data_containers.data_packet import AudioPacket, DataContainer

from sinapsis_elevenlabs.templates.elevenlabs_tts import ElevenLabsTTS


class ElevenLabsVoiceClone(ElevenLabsTTS):
    """Template to clone a voice using the ElevenLabs API.

    This template allows you to create a new custom voice in ElevenLabs by providing
    one or more audio samples. The cloned voice can then be used for subsequent
    text-to-speech synthesis within the Sinapsis pipeline.

    Usage example:

    agent:
    name: my_test_agent
    templates:
    - template_name: InputTemplate
      class_name: InputTemplate
      attributes: {}
    - template_name: ElevenLabsVoiceClone
      class_name: ElevenLabsVoiceClone
      template_input: InputTemplate
      attributes:
        api_key: null
        model: eleven_turbo_v2_5
        output_file_name: null
        output_format: mp3_44100_128
        output_folder: ~/.cache/sinapsis/elevenlabs/audios
        stream: false
        voice: null
        voice_settings:
            stability: null
            similarity_boost: null
            style: null
            use_speaker_boost: null
            speed: null
        name: null
        description: null
        remove_background_noise: false

    """

    class AttributesBaseModel(ElevenLabsTTS.AttributesBaseModel):
        """Attributes specific to the ElevenLabsVoiceClone class.

        Attributes:
            name (str | None): Name for the cloned voice. If None, a default name may be used.
            description (str | None): Description for the cloned voice. Optional.
            remove_background_noise (bool): Whether to remove background noise from samples. Defaults to False.
        """

        name: str | None = None
        description: str | None = None
        remove_background_noise: bool = False

    def clone_voice(self, input_data: list[AudioPacket]) -> Voice:
        """Clones a voice using the provided audio files.

        Args:
            input_data (list[AudioPacket]): List of AudioPacket objects containing the audio samples
                to be used for voice cloning. Each AudioPacket's `content` should be a file-like object
                or bytes representing the audio data.
                **NOTE:** All provided audio packets are used as reference for a single cloned voice.

        Returns:
            Voice: The cloned Voice object as returned by the ElevenLabs API.

        Raises:
            ValueError: If there is a problem with the input data or parameters.
            TypeError: If the input data or files are of incorrect type.
            KeyError: If the expected key is missing in the API response.
        """
        files = [audio.content for audio in input_data]
        try:
            clone_response = self.client.voices.ivc.create(
                name=self.attributes.name,
                files=files,
                description=self.attributes.description,
                remove_background_noise=self.attributes.remove_background_noise,
            )
            cloned_voice = self.client.voices.get(clone_response.voice_id)
            self.logger.info(f"Voice cloned successfully with IVC: {cloned_voice.name}")
            return cloned_voice
        except ValueError as e:
            self.logger.error(f"Value error in input data or parameters: {e}")
            raise
        except TypeError as e:
            self.logger.error(f"Type error with input data or files: {e}")
            raise
        except KeyError as e:
            self.logger.error(f"Missing expected key in API response: {e}")
            raise

    def execute(self, container: DataContainer) -> DataContainer:
        """Executes the voice cloning process and generates the speech output.

        Args:
            container (DataContainer): The input DataContainer, expected to contain
                one or more AudioPacket objects in the `audios` attribute.

        Returns:
            DataContainer: The updated DataContainer. If cloning is successful,
                the cloned voice is set in `self.attributes.voice` and the parent
                TTS execution is performed using the new voice.

        Side Effects:
            - Updates `self.attributes.voice` with the cloned Voice object.
            - May log errors or info messages.
        """
        audios = container.audios
        if not audios:
            self.logger.debug("No audios provided to clone voice")
            return container
        self.attributes.voice = self.clone_voice(audios)

        container = super().execute(container)

        return container
