# -*- coding: utf-8 -*-
"""Base template for ElevenLabs speech synthesis"""

import abc
import os
import uuid
from io import BytesIO
from typing import IO, Iterator, Literal

from elevenlabs import Voice, VoiceSettings, save
from elevenlabs.client import ElevenLabs, VoiceId, VoiceName
from sinapsis_core.data_containers.data_packet import AudioPacket, DataContainer, Packet
from sinapsis_core.template_base.template import (
    Template,
    TemplateAttributes,
    TemplateAttributeType,
)
from sinapsis_core.utils.env_var_keys import SINAPSIS_CACHE_DIR

from sinapsis_elevenlabs.helpers.env_var_keys import ELEVENLABS_API_KEY

RESPONSE_TYPE = Iterator[bytes] | list[bytes] | list[Iterator[bytes]] | None


class ElevenLabsBase(Template, abc.ABC):
    """
    Base template to perform audio generation tasks using the Elevenlabs package.

    The template takes as attributes the elevenlabs api key, the voice for the generated audio,
    settings associated with the audio (such as stability, style, etc.), the model to be used,
    the format for the audio, the path, etc. It implements methods to process the
    DataContainer, initialize the Elevenlabs client, perform the inference,
    and store the audio.

    """

    PACKET_TYPE_NAME: str = "texts"

    class AttributesBaseModel(TemplateAttributes):
        """
        Attributes for ElevenLabs Base Class.
        Args:
            api_key (str): The API key to authenticate with ElevenLabs' API.
            voice (str|elevenlabs.Voice): The voice to use for speech synthesis. This can be a voice ID (str),
                a voice name (str) or an elevenlabs voice object (Voice).
            voice_settings (VoiceSettings): A dictionary of settings that control the behavior of the voice.
                - stability (float)
                - similarity_boost (float)
                - style (float)
                - use_speaker_boost (bool)
            model (Literal): The model identifier to use for speech synthesis.
            output_format (Literal): The output audio format and quality. Options include:
                ["mp3_22050_32", "mp3_44100_32", "mp3_44100_64", "mp3_44100_96", "mp3_44100_128",
                "mp3_44100_192", "pcm_16000", "pcm_22050", "pcm_24000", "pcm_44100", "ulaw_8000"]
            output_folder (str): The folder where generated audio files will be saved.
            stream (bool): If True, the audio is returned as a stream; otherwise, saved to a file.
        """

        api_key: str | None = None
        voice: VoiceId | VoiceName | Voice = None
        voice_settings: VoiceSettings | None = None
        model: Literal[
            "eleven_turbo_v2_5",
            "eleven_multilingual_v2",
            "eleven_turbo_v2",
            "eleven_monolingual_v1",
            "eleven_multilingual_v1",
            "eleven_english_sts_v2",
            "eleven_multilingual_sts_v2",
        ] = "eleven_turbo_v2_5"
        output_format: Literal[
            "mp3_22050_32",
            "mp3_44100_32",
            "mp3_44100_64",
            "mp3_44100_96",
            "mp3_44100_128",
            "mp3_44100_192",
            "pcm_16000",
            "pcm_22050",
            "pcm_24000",
            "pcm_44100",
            "ulaw_8000",
        ] = "mp3_44100_128"
        output_folder: str = os.path.join(SINAPSIS_CACHE_DIR, "elevenlabs", "audios")
        stream: bool = False

    def __init__(self, attributes: TemplateAttributeType) -> None:
        """Initializes the ElevenLabs API client with the given attributes."""
        super().__init__(attributes)
        os.makedirs(self.attributes.output_folder, exist_ok=True)
        self.client = self.init_elevenlabs_client()

    def init_elevenlabs_client(self) -> ElevenLabs:
        """Resets client object"""
        key = self.attributes.api_key if self.attributes.api_key else ELEVENLABS_API_KEY
        return ElevenLabs(api_key=key)

    def reset_state(self) -> None:
        """Resets state of model"""
        self.client = self.init_elevenlabs_client()

    @abc.abstractmethod
    def synthesize_speech(self, input_data: list[Packet]) -> RESPONSE_TYPE:
        """Abstract method for ElevenLabs speech synthesis."""

    def _save_audio(self, response: Iterator[bytes] | bytes, file_format: str) -> str:
        """Saves the audio to a file and returns the file path."""
        output_file = os.path.join(self.attributes.output_folder, f"{uuid.uuid4()}.{file_format}")
        try:
            save(response, output_file)
            self.logger.info(f"Audio saved to: {output_file}")
            return output_file
        except OSError as e:
            self.logger.error(f"File system error while saving speech to file: {e}")
            raise

    def _generate_audio_stream(self, response: Iterator[bytes] | bytes) -> IO[bytes]:
        """Generates and returns the audio stream."""
        audio_stream = BytesIO()
        try:
            if isinstance(response, Iterator):
                for chunk in response:
                    if chunk:
                        audio_stream.write(chunk)
            elif isinstance(response, bytes):
                audio_stream.write(response)
            else:
                raise TypeError(f"Unsupported response type: {type(response)}")

            audio_stream.seek(0)
            self.logger.info("Returning audio stream")
            return audio_stream
        except IOError as e:
            self.logger.error(f"I/O error while processing the audio stream: {e}")
            raise
        except ValueError as e:
            self.logger.error(f"Value error while processing audio chunks: {e}")
            raise

    def _process_audio_output(self, response: Iterator[bytes] | bytes) -> str | IO[bytes]:
        """Processes a single audio output (either stream or file)."""
        if self.attributes.stream:
            return self._generate_audio_stream(response)
        else:
            file_format = "mp3" if "mp3" in self.attributes.output_format else "wav"
            return self._save_audio(response, file_format)

    def generate_speech(self, input_data: list[Packet]) -> list[str | IO[bytes]] | None:
        """Generates speech and saves it to a file."""
        responses: RESPONSE_TYPE = self.synthesize_speech(input_data)
        if not responses:
            return None

        if isinstance(responses, Iterator):
            responses = [responses]

        audio_outputs = [self._process_audio_output(response) for response in responses]
        return audio_outputs

    def _handle_streaming_output(self, audio_outputs: list[str | IO[bytes]]) -> list[AudioPacket]:
        """Handles audio stream output by adding it to the container as AudioPackets."""
        generated_audios: list[AudioPacket] = []
        sample_rate = int(self.attributes.output_format.split("_")[1])
        for audio_output in audio_outputs:
            audio_packet = AudioPacket(
                content=audio_output,
                sample_rate=sample_rate,
            )
            generated_audios.append(audio_packet)
        return generated_audios

    def _handle_audio_outputs(self, audio_outputs: list[str | IO[bytes]], container: DataContainer) -> None:
        """Handles the audio outputs by appending to the container based on the output type (stream or file)."""
        if self.attributes.stream:
            container.audios = container.audios or []
            container.audios.extend(self._handle_streaming_output(audio_outputs))
        else:
            self._set_generic_data(container, audio_outputs)

    def execute(self, container: DataContainer) -> DataContainer:
        """
        Processes the input data and generates a speech output.
        Depending on the configuration, either a file or a stream of audio is
        generated and added to the provided `container`.
        """

        if ELEVENLABS_API_KEY is None and self.attributes.api_key is None:
            self.logger.error("Api key was not provided")
            return container

        data_packet = getattr(container, self.PACKET_TYPE_NAME)

        if not data_packet:
            self.logger.debug("No query to enter")
            return container

        audio_outputs = self.generate_speech(data_packet)
        if not audio_outputs:
            self.logger.error("Unable to generate speech")
            return container

        self._handle_audio_outputs(audio_outputs, container)

        return container
