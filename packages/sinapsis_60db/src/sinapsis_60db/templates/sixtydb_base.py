# -*- coding: utf-8 -*-
"""Base template for 60dB speech synthesis."""

import abc
from typing import Generator, Iterable, Iterator, Literal, cast

import numpy as np
from sinapsis_core.data_containers.data_packet import AudioPacket, DataContainer, Packet
from sinapsis_core.template_base.base_models import (
    OutputTypes,
    TemplateAttributes,
    TemplateAttributeType,
    UIPropertiesMetadata,
)
from sinapsis_core.template_base.template import Template
from sinapsis_generic_data_tools.helpers.audio_encoder import audio_bytes_to_numpy

from sinapsis_60db.helpers.client import DEFAULT_BASE_URL, DEFAULT_WS_URL, SixtyDBClient
from sinapsis_60db.helpers.env_var_keys import SIXTYDB_API_KEY
from sinapsis_60db.helpers.tags import Tags

RESPONSE_TYPE = Iterator[bytes] | list[bytes] | bytes | None


class SixtyDBBase(Template, abc.ABC):
    """
    Base template to perform audio generation tasks using the 60dB speech API.

    The template takes as attributes the 60dB api key, the voice for the generated
    audio, the audio settings (enhance, speed, stability, similarity), the output
    format, etc. It implements methods to process the DataContainer, initialize the
    60dB client, perform the inference, and store the generated audio.

    This mirrors the structure of the ElevenLabs base template so both vendors can
    be used interchangeably inside a Sinapsis pipeline.
    """

    PACKET_TYPE_NAME: str = "texts"

    class AttributesBaseModel(TemplateAttributes):
        """
        Attributes for the 60dB base class.

        Args:
            api_key (str | None): The API key used to authenticate with 60dB's API. If
                ``None``, the ``SIXTYDB_API_KEY`` environment variable is used.
            voice (str | None): The voice to use, given as a voice name or voice ID. If
                ``None``, the first available account voice (or the API default) is used.
            output_format (Literal): The output audio format. One of "mp3", "wav",
                "ogg", "flac".
            enhance (bool): Whether to apply 60dB's audio enhancement. Defaults to True.
            speed (float): Speech speed, range 0.5 to 2.0. Defaults to 1.0.
            stability (float): Expressiveness vs. consistency, range 0 to 100. Defaults to 50.
            similarity (float): Source-voice matching, range 0 to 100. Defaults to 75.
            stream (bool): Kept for parity with the ElevenLabs base; streaming behavior
                is provided by the dedicated streaming/websocket templates.
            base_url (str): Override for the REST base URL.
            ws_url (str): Override for the WebSocket URL.
        """

        api_key: str | None = None
        voice: str | None = None
        output_format: Literal["mp3", "wav", "ogg", "flac"] = "mp3"
        enhance: bool = True
        speed: float = 1.0
        stability: float = 50.0
        similarity: float = 75.0
        stream: bool = False
        base_url: str = DEFAULT_BASE_URL
        ws_url: str = DEFAULT_WS_URL

    attributes: AttributesBaseModel

    UIProperties = UIPropertiesMetadata(
        category="60dB",
        output_type=OutputTypes.AUDIO,
        tags=[Tags.AUDIO, Tags.SIXTYDB, Tags.SPEECH],
    )

    def __init__(self, attributes: TemplateAttributeType) -> None:
        """Initializes the 60dB API client with the given attributes."""
        super().__init__(attributes)
        self.client = self.init_client()

    def init_client(self) -> SixtyDBClient:
        """Creates the 60dB client object."""
        key = self.attributes.api_key if self.attributes.api_key else SIXTYDB_API_KEY
        return SixtyDBClient(api_key=key, base_url=self.attributes.base_url, ws_url=self.attributes.ws_url)

    def reset_state(self, template_name: str | None = None) -> None:
        """Resets state of the client."""
        _ = template_name
        self.client = self.init_client()

    @abc.abstractmethod
    def synthesize_speech(self, input_data: list) -> RESPONSE_TYPE:
        """Abstract method for 60dB speech synthesis."""

    def _generate_audio_stream(self, response: Iterable | bytes) -> bytes:
        """Generates and returns the audio stream as a single bytes object."""
        try:
            if isinstance(response, bytes):
                audio_stream = response
            elif isinstance(response, Iterator):
                audio_stream = b"".join(list(response))
            else:
                raise TypeError(f"Unsupported response type: {type(response)}")

            self.logger.info("Returning audio stream")
            return audio_stream
        except IOError as e:
            self.logger.error(f"I/O error while processing the audio stream: {e}")
            raise
        except ValueError as e:
            self.logger.error(f"Value error while processing audio chunks: {e}")
            raise

    def _process_audio_output(self, response: Iterable | bytes) -> tuple[np.ndarray, int]:
        """Processes a single audio output (either stream or file)."""
        result = self._generate_audio_stream(response)
        audio_np, sample_rate = audio_bytes_to_numpy(result)
        return audio_np, sample_rate

    def generate_speech(self, input_data: list[Packet]) -> list[tuple] | None:
        """Generates speech and returns a list of (audio_array, sample_rate) tuples."""
        responses: RESPONSE_TYPE = self.synthesize_speech(input_data)
        if not responses:
            return None

        if isinstance(responses, (bytes, Iterator)):
            responses = cast(list, [responses])
        elif isinstance(responses, Generator):
            responses = list(responses)
        audio_outputs = [self._process_audio_output(response) for response in responses]
        return audio_outputs

    def _handle_streaming_output(self, audio_outputs: list[tuple]) -> list[AudioPacket]:
        """Wraps each audio output into an AudioPacket."""
        generated_audios: list[AudioPacket] = []
        for audio_output in audio_outputs:
            audio = audio_output[0]
            sample_rate = audio_output[1]
            audio_packet = AudioPacket(
                content=audio,
                sample_rate=sample_rate,
            )
            generated_audios.append(audio_packet)
        return generated_audios

    def _handle_audio_outputs(self, audio_outputs: list[tuple], container: DataContainer) -> None:
        """Appends the generated audio outputs to the container."""
        container.audios = container.audios or []
        container.audios = self._handle_streaming_output(audio_outputs)

    def execute(self, container: DataContainer) -> DataContainer:
        """
        Processes the input data and generates a speech output.

        Depending on the configuration, either a single audio blob or a stream of
        audio is generated and added to the provided `container`.
        """
        if SIXTYDB_API_KEY is None and self.attributes.api_key is None:
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
