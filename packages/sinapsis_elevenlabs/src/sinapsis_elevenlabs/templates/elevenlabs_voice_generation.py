# -*- coding: utf-8 -*-
"""Text-To-Speech template for ElevenLabs"""

import base64

from sinapsis_core.data_containers.data_packet import TextPacket

from sinapsis_elevenlabs.helpers.voice_utils import load_input_text
from sinapsis_elevenlabs.templates.elevenlabs_base import ElevenLabsBase


class ElevenLabsVoiceGeneration(ElevenLabsBase):
    """
    Template to generate a voice using ElevenLabs API.

    The template takes the voice description as an attribute and
    the prompt for the audio as a TextPacket stored in the DataContainer
    and stores the generated audio in the DataContainer.

    Usage example:

    agent:
      name: my_test_agent
    templates:
    - template_name: InputTemplate
      class_name: InputTemplate
      attributes: {}
    - template_name: ElevenLabsVoiceGeneration
      class_name: ElevenLabsVoiceGeneration
      template_input: InputTemplate
      attributes:
        voice: null
        voice_settings: null
        model: eleven_turbo_v2_5
        output_format: mp3_44100_128
        output_folder: /sinapsis/cache/dir/elevenlabs/audios
        stream: false
        voice_description: An old British male with a raspy, deep voice. Professional,
          relaxed and assertive
    """

    class AttributesBaseModel(ElevenLabsBase.AttributesBaseModel):
        """
        Attributes for voice generation in ElevenLabs API.

        Args:
            voice_description (str): A description of the voice to be used for synthesis.
        """

        voice_description: str

    def synthesize_speech(self, input_data: list[TextPacket]) -> list[bytes] | None:
        """
        Sends the text to ElevenLabs API to generate speech.

        This method communicates with the ElevenLabs API to generate the audio
        response based on the provided text, voice, and model settings.
        """

        input_text: str = load_input_text(input_data)
        if len(input_text) < 100:
            self.logger.error("The text to be spoken must be at least 100 characters long.")
            return None
        try:
            voice_previews = self.client.text_to_voice.create_previews(
                voice_description=self.attributes.voice_description,
                text=input_text,
            )

            responses: list[bytes] = [base64.b64decode(preview.audio_base_64) for preview in voice_previews.previews]

            return responses
        except ValueError as e:
            self.logger.error(f"Value error with voice description or input text: {e}")
            raise
        except TypeError as e:
            self.logger.error(f"Type error with input data or voice preview parameters: {e}")
            raise
        except KeyError as e:
            self.logger.error(f"Missing expected key in voice preview response: {e}")
            raise
