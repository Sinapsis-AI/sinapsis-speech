# -*- coding: utf-8 -*-
import os
from typing import Any, Literal

import nemo.collections.asr as nemo_asr
import torch
from sinapsis_core.data_containers.data_packet import (
    AudioPacket,
    DataContainer,
    TextPacket,
)
from sinapsis_core.template_base.base_models import (
    OutputTypes,
    TemplateAttributes,
    UIPropertiesMetadata,
)
from sinapsis_core.template_base.template import Template

from sinapsis_parakeet_tdt.helpers.tags import Tags


class ParakeetTDTInferenceAttributes(TemplateAttributes):
    """
    Attributes for the ParakeetTDT model.

    Attributes:
        model_name (str): Name or path of the Parakeet TDT model. Defaults to "nvidia/parakeet-tdt-0.6b-v2".
        audio_paths (list[str]): Optional list of audio file paths to transcribe. If empty, audio will be
            taken from the `AudioPackets` in the `DataContainer`. Defaults to an empty list.
        enable_timestamps (bool): Whether to generate timestamps for the transcription. Defaults to False.
        timestamp_level (Literal["char", "word", "segment"]): Level of timestamp detail. Defaults to "word".
        device (Literal["cpu", "cuda"]): Device to run the model on. Defaults to "cuda".
        refresh_cache (bool): Whether to refresh the cache when downloading the model. Defaults to False.
            This is useful if the model has been updated and you want to ensure you have the latest version.
    """

    model_name: str = "nvidia/parakeet-tdt-0.6b-v2"
    audio_paths: list[str] | None = None
    enable_timestamps: bool = False
    timestamp_level: Literal["char", "word", "segment"] = "word"
    device: Literal["cpu", "cuda"] = "cuda"
    refresh_cache: bool = False


class ParakeetTDTInference(Template):
    """Template for NVIDIA Parakeet TDT 0.6B speech recognition.

    This template uses NVIDIA's Parakeet TDT 0.6B automatic speech recognition (ASR) model
    to transcribe audio. It can read audio directly from AudioPackets in the DataContainer
    or from specified file paths. The model supports punctuation, capitalization, and
    timestamp prediction.

    Usage example:

    agent:
      name: my_transcription_agent
    templates:
    - template_name: InputTemplate
      class_name: InputTemplate
      attributes: {}

    - template_name: ParakeetTDT
      class_name: ParakeetTDTInference
      template_input: InputTemplate
      attributes:
        model_name: "nvidia/parakeet-tdt-0.6b-v2"
        audio_paths: ['/path/to/file.wav']
        enable_timestamps: True
        timestamp_level: "word"
        device: "cuda"
        refresh_cache: False
    """

    UIProperties = UIPropertiesMetadata(
        category="Parakeet TDT",
        output_type=OutputTypes.TEXT,
        tags=[
            Tags.AUDIO,
            Tags.SPEECH,
            Tags.PARAKEET_TDT,
            Tags.SPEECH_RECOGNITION,
            Tags.SPEECH_TO_TEXT,
            Tags.TRANSCRIPTION,
        ],
    )

    AttributesBaseModel = ParakeetTDTInferenceAttributes

    def __init__(self, attributes: TemplateAttributes) -> None:
        super().__init__(attributes)
        self._load_model()

    def _load_model(self) -> None:
        """
        Load the ASR model from pretrained source.

        This method initializes the NeMo ASR model using the specified model name
        and device configuration from the template attributes.
        """
        self.model = nemo_asr.models.ASRModel.from_pretrained(
            model_name=self.attributes.model_name,
            map_location=self.attributes.device,
        )

    def get_sources_from_packets(self, audio_packets: list[AudioPacket]) -> list[str]:
        """
        Extract valid audio file paths from AudioPackets.

        Args:
            audio_packets: List of audio packets to extract source paths from.

        Returns:
            list[str]: List of valid audio file paths extracted from the packets.
        """
        sources = []
        for audio_packet in audio_packets:
            if not audio_packet or not audio_packet.source:
                self.logger.warning(f"Invalid or nonexistent audio source: {audio_packet.source}")
            sources.append(audio_packet.source)
        return sources

    def get_sources_from_paths(self, paths: list[str]) -> list[str]:
        """
        Extract valid audio file paths from a list of paths.

        Args:
            paths: List of file paths to validate and extract.

        Returns:
            list[str]: List of valid audio file paths.
        """
        sources = []
        for path in paths:
            if not os.path.exists(path):
                self.logger.warning(f"Audio file not found: {path}")
            sources.append(path)
        return sources

    def get_audio_sources(self, container: DataContainer) -> list[str]:
        """
        Get audio sources from container or attributes.

        This method first attempts to extract audio sources from the DataContainer's
        audio packets. If no sources are found, it falls back to using the audio paths
        specified in the template attributes.

        Args:
            container: DataContainer containing possible audio packets.

        Returns:
            list[str]: List of audio file paths to be transcribed.
        """
        sources = []
        if container.audios:
            sources = self.get_sources_from_packets(container.audios)

        if not sources and self.attributes.audio_paths:
            sources = self.get_sources_from_paths(self.attributes.audio_paths)

        return sources

    @staticmethod
    def _process_transcription_result(result: Any) -> str:
        """
        Extract text from transcription result.

        Args:
            result: Transcription result object from the ASR model.

        Returns:
            str: The extracted text content.
        """
        return result.text if hasattr(result, "text") else str(result)

    def _extract_timestamps(self, result: Any) -> dict | None:
        """
        Extract timestamps from result if available.

        Args:
            result: Transcription result object from the ASR model.

        Returns:
            dict | None: Dictionary containing timestamp information at the specified
            level (char, word, or segment) or None if no timestamps are available.
        """
        if not result.timestamp:
            return None

        return result.timestamp.get(self.attributes.timestamp_level, [])

    @staticmethod
    def create_text_packet(text: str, source: str) -> TextPacket:
        """
        Create text packet from transcription data.

        Args:
            text: Transcribed text content.
            source: Source identifier for the text packet.

        Returns:
            TextPacket: A text packet containing the transcription.
        """
        text_packet = TextPacket(
            content=text,
            source=source,
        )

        return text_packet

    def transcribe_sources(self, sources: list[str]) -> list[Any]:
        """
        Transcribe audio sources and return results.

        This method passes the audio sources to the ASR model for transcription,
        with timestamp generation enabled based on the template attributes.

        Args:
            sources: List of audio file paths to transcribe.

        Returns:
            list[Any]: List of transcription results from the ASR model.
        """
        return self.model.transcribe(
            sources,
            timestamps=self.attributes.enable_timestamps,
        )

    def process_results(
        self,
        transcription_results: list[Any],
        sources: list[str],
        container: DataContainer,
    ) -> list[TextPacket]:
        """
        Process transcription results into text packets.

        This method extracts text and timestamps from the transcription results
        and creates corresponding text packets. Timestamps are stored in the
        container's generic data dictionary.

        Args:
            transcription_results: List of transcription results from the ASR model.
            sources: List of audio file paths that were transcribed.
            container: DataContainer to store additional data.

        Returns:
            list[TextPacket]: List of text packets containing the transcriptions.
        """
        text_packets = []

        for i, result in enumerate(transcription_results):
            source = sources[i] if i < len(sources) else f"transcription_{i}"
            text = self._process_transcription_result(result)
            timestamps = self._extract_timestamps(result)
            text_packet = self.create_text_packet(text, source)
            text_packets.append(text_packet)
            if timestamps:
                self._set_generic_data(container, {f"timestamps_{source}": timestamps})

        return text_packets

    def execute(self, container: DataContainer) -> DataContainer:
        """
        Transcribe audio to text using the Parakeet TDT model.

        Args:
            container: DataContainer with audio packets to transcribe.

        Returns:
            DataContainer: The same container with added text packets containing transcriptions.
        """
        sources = self.get_audio_sources(container)

        if not sources:
            self.logger.info("No audio sources found for transcription")
            return container

        self.logger.info(f"Transcribing {len(sources)} audio files")
        transcription_results = self.transcribe_sources(sources)
        text_packets = self.process_results(transcription_results, sources, container)
        container.texts = container.texts or []
        container.texts.extend(text_packets)

        return container

    def reset_state(self, template_name: str | None = None) -> None:
        if "cuda" in self.attributes.device:
            torch.cuda.empty_cache()
        super().reset_state(template_name)
