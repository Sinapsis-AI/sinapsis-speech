# -*- coding: utf-8 -*-
from typing import Any, Literal

import torch
from csm.generator import Generator
from csm.models import Model


class CSMGenerator:
    """
    Wrapper around the CSM model providing a simple interface
    for text-to-speech generation
    """

    def __init__(self, device: Literal["cpu", "cuda"] = "cpu", sample_rate: int = 24000) -> None:
        self.device: str = device
        self.sample_rate: int = sample_rate
        self.model: Model = Model.from_pretrained("sesame/csm-1b")
        self.model.to(device=device)
        setattr(self.model, "sample_rate", sample_rate)
        self.generator = Generator(self.model)

    def generate(
        self, text: str, speaker: int = 0, context: list[Any] | None = None, max_audio_length_ms: int = 10000
    ) -> torch.Tensor:
        if context is None:
            context = []
        return self.generator.generate(
            text=text,
            speaker=speaker,
            context=context,
            max_audio_length_ms=max_audio_length_ms,
        )


def load_csm_1b(device: Literal["cpu", "cuda"] = "cpu", sample_rate: int = 24000) -> CSMGenerator:
    """
    Loads and configures the CSM TTS model.

    Returns:
        CSMGenerator: Model wrapper with ready-to-use generate method.
    """
    return CSMGenerator(device=device, sample_rate=sample_rate)
