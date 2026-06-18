# -*- coding: utf-8 -*-
"""Text-To-Speech template for 60dB (single-request synthesis)."""

from sinapsis_core.data_containers.data_packet import TextPacket

from sinapsis_60db.helpers.tags import Tags
from sinapsis_60db.helpers.voice_utils import get_voice_id, load_input_text
from sinapsis_60db.templates.sixtydb_base import SixtyDBBase

SixtyDBTTSUIProperties = SixtyDBBase.UIProperties
if SixtyDBTTSUIProperties.tags is not None:
    SixtyDBTTSUIProperties.tags.extend([Tags.TEXT_TO_SPEECH])

MAX_TEXT_LENGTH = 5000


class SixtyDBTTS(SixtyDBBase):
    """Template to interact with the 60dB text-to-speech API (``POST /tts-synthesize``).

    This class generates speech from text in a single request. It allows
    customization of voice, audio settings, and output format.

    Usage example:

    agent:
      name: my_test_agent
    templates:
    - template_name: InputTemplate
      class_name: InputTemplate
      attributes: {}
    - template_name: SixtyDBTTS
      class_name: SixtyDBTTS
      template_input: InputTemplate
      attributes:
        api_key: null
        voice: null
        output_format: mp3
        enhance: true
        speed: 1.0
        stability: 50.0
        similarity: 75.0
    """

    UIProperties = SixtyDBTTSUIProperties

    def synthesize_speech(self, input_data: list[TextPacket]) -> bytes | None:
        """Sends the text to the 60dB API to generate speech.

        Returns:
            bytes | None: The decoded audio bytes, or ``None`` if the input is invalid.
        """
        input_text: str = load_input_text(input_data)
        if not input_text:
            self.logger.debug("No input text to synthesize")
            return None
        if len(input_text) > MAX_TEXT_LENGTH:
            self.logger.warning(
                f"Input text has {len(input_text)} characters; 60dB /tts-synthesize allows a maximum of "
                f"{MAX_TEXT_LENGTH}. The request may be rejected."
            )
        try:
            return self.client.text_to_speech(
                text=input_text,
                voice_id=get_voice_id(self.client, self.attributes.voice),
                output_format=self.attributes.output_format,
                enhance=self.attributes.enhance,
                speed=self.attributes.speed,
                stability=self.attributes.stability,
                similarity=self.attributes.similarity,
            )
        except ValueError as e:
            self.logger.error(f"Value error synthesizing speech: {e}")
            raise
        except TypeError as e:
            self.logger.error(f"Type error in input data or parameters: {e}")
            raise
        except KeyError as e:
            self.logger.error(f"Missing key in input data or settings: {e}")
            raise
