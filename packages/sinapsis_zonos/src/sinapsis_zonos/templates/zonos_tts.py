# -*- coding: utf-8 -*-
"""Base template for Zonos speech synthesis"""

import os
import uuid
from typing import Literal, Set

import torch
import torchaudio
from pydantic import Field
from sinapsis_core.data_containers.data_packet import DataContainer, TextPacket
from sinapsis_core.template_base.base_models import (
    OutputTypes,
    TemplateAttributes,
    TemplateAttributeType,
    UIPropertiesMetadata,
)
from sinapsis_core.template_base.template import Template
from sinapsis_core.utils.env_var_keys import SINAPSIS_CACHE_DIR
from zonos.model import Zonos
from zonos.utils import DEFAULT_DEVICE as device

from sinapsis_zonos.helpers.zonos_keys import EmotionsConfig, SamplingParams, TTSKeys
from sinapsis_zonos.helpers.zonos_tts_utils import (
    get_audio_prefix_codes,
    get_conditioning,
    get_sampling_params,
    init_seed,
)


class ZonosTTS(Template):
    """
    Base template for speech synthesis using the Zonos model.

    This template is designed to generate high-quality, expressive text-to-speech (TTS) outputs
    using the Zonos TTS model, which supports multilingual speech generation, speaker cloning,
    and fine control over various speech attributes like pitch, speaking rate, and emotions.
    """

    UIProperties = UIPropertiesMetadata(category="Zonos", output_type=OutputTypes.AUDIO)

    class AttributesBaseModel(TemplateAttributes):
        """
        Attributes for Zonos TTS model configuration.
        Args:
            model (str): Model identifier for Zonos. Options:
                "Zyphra/Zonos-v0.1-transformer", "Zyphra/Zonos-v0.1-hybrid" (default: "Zyphra/Zonos-v0.1-transformer").
            language (str): Language for speech synthesis (default: 'en-us').
            emotions (Emotions | None): Emotions to apply to generated speech, fine-tuning emotional tone.
            fmax (float): Max frequency for speech in Hz (default: 22050, range: 0-24000).
            pitch_std (float): Standard deviation for pitch variation (default: 20.0, range: 0-300).
            speaking_rate (float): Rate of speech (default: 15.0, range: 5-30).
            dnsmos (float): Denoising strength for hybrid models (default: 4.0, range: 1-5).
            vq_score (float): VQ score for hybrid models (default: 0.78, range: 0.5-0.8).
            cfg_scale (float): Controls randomness in speech (default: 2.0, range: 1-5).
            sampling_params (SamplingParams | None): Controls sampling behavior, including `top_p`, `top_k`, `min_p`,
                `linear`, `conf`, and `quad` parameters for sampling.
            randomized_seed (bool): If True, the seed is randomized (default: True).
            denoised_speaker (bool): If True, applies denoising to speaker embedding.
            unconditional_keys (Iterable[str]): Keys for conditioning speech without speaker embedding.
            prefix_audio (str | None): Path to an audio file for prefix conditioning (e.g., whispering).
            speaker_audio (str | None): Path to an audio file for creating a speaker embedding for voice cloning.
            output_folder (str): Folder for saving generated audio files (default: SINAPSIS_CACHE_DIR/zonos/audios).
        """

        cfg_scale: float = 2.0
        denoised_speaker: bool = False
        dnsmos: float = 4.0
        emotions: EmotionsConfig = Field(default_factory=dict)  # type: ignore[arg-type]
        fmax: float = 22050.0
        language: str = TTSKeys.en_language
        model: Literal["Zyphra/Zonos-v0.1-transformer", "Zyphra/Zonos-v0.1-hybrid"] = "Zyphra/Zonos-v0.1-transformer"
        output_folder: str = os.path.join(SINAPSIS_CACHE_DIR, "zonos", "audios")
        pitch_std: float = 20.0
        prefix_audio: str | None = None
        randomized_seed: bool = True
        sampling_params: SamplingParams = Field(default_factory=dict)  # type: ignore[arg-type]
        seed: int = 420
        speaker_audio: str | None = None
        speaking_rate: float = 15.0
        unconditional_keys: Set[str] = Field(default={TTSKeys.vqscore_8, TTSKeys.dnsmos_ovrl})
        vq_score: float = 0.7

    def __init__(self, attributes: TemplateAttributeType) -> None:
        """Initializes the Zonos model with the provided attributes."""
        super().__init__(attributes)
        os.makedirs(self.attributes.output_folder, exist_ok=True)
        self.device = device
        self.model = self._init_model()
        init_seed(self.attributes)
        self.logger.debug(f"Model {self.attributes.model} initalized\nSeed: {self.attributes.seed}")

    def _init_model(self) -> Zonos:
        """
        Initialize and load the specified Zonos model.

        Returns:
            Zonos: The loaded and prepared Zonos model, set to evaluation mode with gradients disabled.
        """
        model = Zonos.from_pretrained(self.attributes.model, device=self.device)
        model.requires_grad_(False).eval()
        return model

    def _del_model(self) -> None:
        """
        Delete the current model instance and clear CUDA cache.

        Frees GPU memory by deleting the model and explicitly emptying the CUDA cache.
        """
        if self.model:
            del self.model
            torch.cuda.empty_cache()

    def reset_state(self) -> None:
        """Reinitialize the model and random seed."""
        self._del_model()
        self.model = self._init_model()
        init_seed(self.attributes)
        self.logger.debug(f"Model {self.attributes.model} reset\nSeed: {self.attributes.seed}")

    def generate_speech(self, input_data: list[TextPacket]) -> torch.Tensor:
        """
        Generates speech for the input text data.

        Args:
            input_data (list[TextPacket]): A list of `TextPacket` objects containing the text data.

        Returns:
            torch.Tensor: The generated speech audio tensor.
        """
        input_text = "".join(t.content for t in input_data)
        conditioning = get_conditioning(self.attributes, self.model, input_text, self.device)
        prefix_codes = get_audio_prefix_codes(
            self.attributes.prefix_audio,
            self.model,
        )

        codes = self.model.generate(
            prefix_conditioning=conditioning,
            audio_prefix_codes=prefix_codes,
            cfg_scale=self.attributes.cfg_scale,
            batch_size=1,
            sampling_params=get_sampling_params(self.attributes.sampling_params),
        )
        output_wav = self.model.autoencoder.decode(codes).cpu().detach()
        return output_wav

    def save_audio_output(self, output_audio: torch.Tensor, container: DataContainer) -> None:
        """
        Saves a single generated audio output to the specified folder.

        Args:
            output_audio (torch.Tensor): The generated audio output tensor.
            container (DataContainer): The container to store metadata.
        """
        output_path = os.path.join(self.attributes.output_folder, f"{uuid.uuid4()}.{TTSKeys.wav}")
        torchaudio.save(output_path, output_audio[0], self.model.autoencoder.sampling_rate)
        self._set_generic_data(container, [output_path])
        self.logger.debug(f"Audio saved to: {output_path}")

    def execute(self, container: DataContainer) -> DataContainer:
        """Processes the input data and generates a speech output."""

        if not container.texts:
            self.logger.debug("No query to enter")
            return container

        audio_output = self.generate_speech(container.texts)
        if audio_output is None:
            self.logger.error("Unable to generate speech")
            return container

        self.save_audio_output(audio_output, container)

        return container
