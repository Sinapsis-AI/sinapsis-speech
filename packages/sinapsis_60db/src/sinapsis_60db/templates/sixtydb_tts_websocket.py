# -*- coding: utf-8 -*-
"""WebSocket Text-To-Speech template for 60dB."""

from typing import Iterable, Literal

import numpy as np
from sinapsis_core.data_containers.data_packet import TextPacket
from sinapsis_generic_data_tools.helpers.audio_encoder import audio_bytes_to_numpy

from sinapsis_60db.helpers.tags import Tags
from sinapsis_60db.helpers.voice_utils import get_voice_id, load_input_text
from sinapsis_60db.templates.sixtydb_base import SixtyDBBase

SixtyDBTTSWebSocketUIProperties = SixtyDBBase.UIProperties
if SixtyDBTTSWebSocketUIProperties.tags is not None:
    SixtyDBTTSWebSocketUIProperties.tags.extend([Tags.TEXT_TO_SPEECH, Tags.WEBSOCKET, Tags.STREAMING])

RAW_PCM_ENCODINGS = ("LINEAR16", "PCM")

MAX_TEXT_LENGTH = 50000


class SixtyDBTTSWebSocket(SixtyDBBase):
    """Template to interact with the 60dB WebSocket TTS API (``wss://.../ws/tts``).

    This class opens a synthesis context over a WebSocket connection, sends the
    text, and collects the streamed ``audio_chunk`` messages into a single
    AudioPacket.

    Because the WebSocket API can emit headerless raw PCM (``LINEAR16``/``PCM``),
    this template decodes those formats directly using the configured sample rate.
    Container formats (``OGG_OPUS``) are decoded with the standard audio decoder.

    Usage example:

    agent:
      name: my_test_agent
    templates:
    - template_name: InputTemplate
      class_name: InputTemplate
      attributes: {}
    - template_name: SixtyDBTTSWebSocket
      class_name: SixtyDBTTSWebSocket
      template_input: InputTemplate
      attributes:
        api_key: null
        voice: null
        audio_encoding: OGG_OPUS
        sample_rate_hertz: 48000
        speed: 1.0
        stability: 50.0
        similarity: 75.0
    """

    UIProperties = SixtyDBTTSWebSocketUIProperties

    class AttributesBaseModel(SixtyDBBase.AttributesBaseModel):
        """Attributes specific to the 60dB WebSocket TTS API.

        Attributes:
            audio_encoding (Literal): The audio encoding requested over the socket.
                One of LINEAR16, PCM, MULAW, ULAW, OGG_OPUS.
            sample_rate_hertz (Literal): The requested sample rate. One of 8000,
                16000, 24000, 48000.
            context_id (str): The session/context identifier.
        """

        audio_encoding: Literal["LINEAR16", "PCM", "MULAW", "ULAW", "OGG_OPUS"] = "OGG_OPUS"
        sample_rate_hertz: Literal[8000, 16000, 24000, 48000] = 48000
        context_id: str = "sinapsis"

    attributes: AttributesBaseModel

    def synthesize_speech(self, input_data: list[TextPacket]) -> bytes | None:
        """Synthesizes speech over the WebSocket connection and returns the audio bytes."""
        input_text: str = load_input_text(input_data)
        if not input_text:
            self.logger.debug("No input text to synthesize")
            return None
        if len(input_text) > MAX_TEXT_LENGTH:
            self.logger.warning(
                f"Input text has {len(input_text)} characters; the 60dB WebSocket API allows a cumulative "
                f"maximum of {MAX_TEXT_LENGTH}. The request may be rejected."
            )
        voice_id = get_voice_id(self.client, self.attributes.voice)
        if not voice_id:
            self.logger.error("The 60dB WebSocket API requires a voice_id but none could be resolved.")
            return None
        try:
            return self.client.text_to_speech_websocket(
                text=input_text,
                voice_id=voice_id,
                audio_encoding=self.attributes.audio_encoding,
                sample_rate_hertz=self.attributes.sample_rate_hertz,
                speed=self.attributes.speed,
                stability=self.attributes.stability,
                similarity=self.attributes.similarity,
                context_id=self.attributes.context_id,
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

    def _process_audio_output(self, response: Iterable | bytes) -> tuple[np.ndarray, int]:
        """Decodes the audio, handling headerless raw PCM directly."""
        result = self._generate_audio_stream(response)
        if self.attributes.audio_encoding in RAW_PCM_ENCODINGS:
            audio_np = np.frombuffer(result, dtype=np.int16).astype(np.float32) / 32768.0
            return audio_np, self.attributes.sample_rate_hertz
        return audio_bytes_to_numpy(result)
