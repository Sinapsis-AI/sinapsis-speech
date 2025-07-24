# -*- coding: utf-8 -*-
"""Speech-To-Speech template for ElevenLabs."""

from typing import Callable, Iterator, Literal

from sinapsis_core.data_containers.data_packet import AudioPacket

from sinapsis_elevenlabs.helpers.tags import Tags
from sinapsis_elevenlabs.helpers.voice_utils import create_voice_settings, get_voice_id
from sinapsis_elevenlabs.templates.elevenlabs_base import ElevenLabsBase

ElevenLabsSTSUIProperties = ElevenLabsBase.UIProperties
ElevenLabsSTSUIProperties.tags.extend([Tags.SPEECH_TO_SPEECH, Tags.VOICE_CONVERSION])


class ElevenLabsSTS(ElevenLabsBase):
    """Template to interact with the ElevenLabs Speech-to-Speech API.

    This template takes an input audio and converts it to a new voice using
    the ElevenLabs Speech-to-Speech (STS) API.

    Usage example:

    agent:
      name: my_test_agent
    templates:
    - template_name: InputTemplate
      class_name: InputTemplate
      attributes: {}
    - template_name: ElevenLabsSTS
      class_name: ElevenLabsSTS
      template_input: InputTemplate
      attributes:
        api_key: null
        model: eleven_multilingual_sts_v2
        output_file_name: null
        output_format: mp3_44100_128
        output_folder: <WORKING_DIR>/elevenlabs/audios
        stream: false
        voice: null
        voice_settings:
            stability: null
            similarity_boost: null
            style: null
            use_speaker_boost: null
            speed: null
        streaming_latency: null

    """

    PACKET_TYPE_NAME: str = "audios"
    UIProperties = ElevenLabsSTSUIProperties

    class AttributesBaseModel(ElevenLabsBase.AttributesBaseModel):
        """Attributes specific to ElevenLabs STS API interaction.

        Attributes:
            model (Literal): The STS model to use. Options are "eleven_english_sts_v2" or "eleven_multilingual_sts_v2".
            streaming_latency (int | None): Optional latency optimization for streaming. Defaults to None.
        """

        model: Literal["eleven_english_sts_v2", "eleven_multilingual_sts_v2"] = "eleven_multilingual_sts_v2"
        streaming_latency: int | None = None

    def synthesize_speech(self, input_data: list[AudioPacket]) -> Iterator[bytes]:
        """Sends an audio input to the ElevenLabs API for speech-to-speech synthesis.

        Args:
            input_data (list[AudioPacket]): List of AudioPacket objects containing the audio to be converted.
                Only the first AudioPacket in the list is used.

        Returns:
            Iterator[bytes]: An iterator yielding audio data chunks in the output format specified.

        Raises:
            ValueError: If there is a problem with the input data or parameters.
            TypeError: If the input data or files are of incorrect type.
            KeyError: If the expected key is missing in the API response.
        """
        try:
            method: Callable[..., Iterator[bytes]] = self.client.speech_to_speech.stream  # (

            return method(
                voice_id=get_voice_id(self.client, voice=self.attributes.voice),
                audio=input_data[0].content,
                model_id=self.attributes.model,
                voice_settings=create_voice_settings(self.attributes.voice_settings, as_json=True),
                output_format=self.attributes.output_format,
                optimize_streaming_latency=self.attributes.streaming_latency,
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
