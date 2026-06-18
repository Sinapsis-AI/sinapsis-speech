# -*- coding: utf-8 -*-
"""Streaming Text-To-Speech template for 60dB."""

from typing import Iterator

from sinapsis_core.data_containers.data_packet import TextPacket

from sinapsis_60db.helpers.tags import Tags
from sinapsis_60db.helpers.voice_utils import get_voice_id, load_input_text
from sinapsis_60db.templates.sixtydb_base import SixtyDBBase

SixtyDBTTSStreamUIProperties = SixtyDBBase.UIProperties
if SixtyDBTTSStreamUIProperties.tags is not None:
    SixtyDBTTSStreamUIProperties.tags.extend([Tags.TEXT_TO_SPEECH, Tags.STREAMING])


class SixtyDBTTSStream(SixtyDBBase):
    """Template to interact with the 60dB streaming TTS API (``POST /tts-stream``).

    This class generates speech from text and consumes the NDJSON streaming
    response, yielding audio chunks as they arrive. The base template joins the
    chunks into a single AudioPacket before storing it in the container.

    Usage example:

    agent:
      name: my_test_agent
    templates:
    - template_name: InputTemplate
      class_name: InputTemplate
      attributes: {}
    - template_name: SixtyDBTTSStream
      class_name: SixtyDBTTSStream
      template_input: InputTemplate
      attributes:
        api_key: null
        voice: null
        output_format: mp3
        enhance: true
        speed: 1.0
        stability: 50.0
        similarity: 75.0
        stream: true
    """

    UIProperties = SixtyDBTTSStreamUIProperties

    def synthesize_speech(self, input_data: list[TextPacket]) -> Iterator[bytes] | None:
        """Streams the synthesized speech from the 60dB API.

        Returns:
            Iterator[bytes] | None: An iterator yielding decoded audio chunks, or
                ``None`` if the input is invalid.
        """
        input_text: str = load_input_text(input_data)
        if not input_text:
            self.logger.debug("No input text to synthesize")
            return None
        try:
            return self.client.text_to_speech_stream(
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
