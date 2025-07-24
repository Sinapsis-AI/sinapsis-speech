# -*- coding: utf-8 -*-
"""Text-To-Speech template for ElevenLabs"""

from typing import Callable, Iterator, Literal

from sinapsis_core.data_containers.data_packet import TextPacket

from sinapsis_elevenlabs.helpers.tags import Tags
from sinapsis_elevenlabs.helpers.voice_utils import (
    create_voice_settings,
    get_voice_id,
    load_input_text,
)
from sinapsis_elevenlabs.templates.elevenlabs_base import ElevenLabsBase

ElevenLabsTTSUIProperties = ElevenLabsBase.UIProperties
ElevenLabsTTSUIProperties.tags.extend([Tags.TEXT_TO_SPEECH])


class ElevenLabsTTS(ElevenLabsBase):
    """Template to interact with ElevenLabs text-to-speech API.

    This class provides an implementation to generate speech from text using the
    ElevenLabs text-to-speech API. It allows customization of voice, model settings,
    and audio output format.

    Usage example:

    agent:
      name: my_test_agent
    templates:
    - template_name: InputTemplate
      class_name: InputTemplate
      attributes: {}
    - template_name: ElevenLabsTTS
      class_name: ElevenLabsTTS
      template_input: InputTemplate
      attributes:
        voice: null
        voice_settings: null
        model: eleven_turbo_v2_5
        output_format: mp3_44100_128
        output_folder: <WORKING_DIR>/elevenlabs/audios
        stream: false

    """

    class AttributesBaseModel(ElevenLabsBase.AttributesBaseModel):
        """Attributes specific to ElevenLabs TTS API interaction.

        This class overrides the base attributes of `ElevenLabsBase` to define
        default models specific to the ElevenLabs TTS system.
        """

        model: Literal[
            "eleven_turbo_v2_5",
            "eleven_multilingual_v2",
            "eleven_turbo_v2",
            "eleven_monolingual_v1",
            "eleven_multilingual_v1",
        ] = "eleven_turbo_v2_5"

    def synthesize_speech(self, input_data: list[TextPacket]) -> Iterator[bytes]:
        """
        Sends the text to ElevenLabs API to generate speech.

        This method communicates with the ElevenLabs API to generate the audio
        response based on the provided text, voice, and model settings.
        """
        input_text: str = load_input_text(input_data)
        try:
            method: Callable[..., Iterator[bytes]] = self.client.text_to_speech.stream

            return method(
                text=input_text,
                voice_id=get_voice_id(self.client, self.attributes.voice),
                model_id=self.attributes.model,
                voice_settings=create_voice_settings(self.attributes.voice_settings),
                output_format=self.attributes.output_format,
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
