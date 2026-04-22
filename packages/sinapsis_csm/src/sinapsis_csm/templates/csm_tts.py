# -*- coding: utf-8 -*-
from typing import Literal

import torch
from sinapsis_core.data_containers.data_packet import AudioPacket, DataContainer
from sinapsis_core.template_base import Template
from sinapsis_core.template_base.base_models import TemplateAttributes, TemplateAttributeType

from sinapsis_csm.helpers.generator import load_csm_1b


class CSMTTS(Template):
    """
    Sinapsis template for converting text into speech using the CSM TTS model.
    """

    class AttributesBaseModel(TemplateAttributes):
        """
        Defines configurable attributes for the CSMTTS template.
        """

        speaker_id: int = 0
        max_audio_length_ms: int = 10000
        device: Literal["cuda", "cpu"] = "cpu"
        context: list[str] | None = None
        sample_rate_hz: int = 24000

    attributes: AttributesBaseModel

    def __init__(self, attributes: TemplateAttributeType) -> None:
        """
        Initializes the template and loads the CSM model.

        Args:
            attributes (TemplateAttributeType): User-defined attributes from YAML configuration.
        """
        super().__init__(attributes)
        self.model = load_csm_1b(device=self.attributes.device, sample_rate=self.attributes.sample_rate_hz)

    def generate_audio(self, text: str) -> torch.Tensor:
        """
        Converts input text to audio using the CSM model.

        Args:
            text (str): Input text string.

        Returns:
            torch.Tensor: Audio waveform tensor.
        """
        context = self.attributes.context if self.attributes.context else []
        return self.model.generate(
            text=text,
            speaker=self.attributes.speaker_id,
            context=context,
            max_audio_length_ms=self.attributes.max_audio_length_ms,
        )

    def generate_audio_packet(self, audio: torch.Tensor, source_text: str) -> AudioPacket:
        """
        Wraps a raw audio tensor into a sinapsis compatible audioPacket

        Args:
            audio (torch.Tensor): Audio waveform.
            source_text (str): Original input text used for generation.

        Returns:
            AudioPacket: Encapsulated audio data with metadata.
        """
        audio_np = audio.cpu().numpy()
        return AudioPacket(
            content=audio_np,
            sample_rate=self.attributes.sample_rate_hz,
            generic_data={"source_text": source_text, "model": "CSM"},
        )

    def execute(self, container: DataContainer) -> DataContainer:
        """
        Main method executed by Sinapsis. Converts all text packets in the input container to audio.

        Args:
            container (DataContainer): Input container with text packets.

        Returns:
            DataContainer: Output container with generated audio packets.
        """
        for packet in container.texts:
            audio = self.generate_audio(packet.content)
            audio_packet = self.generate_audio_packet(audio, packet.content)
            audio_packet.source = self.instance_name
            container.audios.append(audio_packet)
        return container
