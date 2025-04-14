# -*- coding: utf-8 -*-
from typing import Set

import torch
import torchaudio
from sinapsis_core.template_base.template import TemplateAttributeType
from sinapsis_core.utils.logging_utils import sinapsis_logger
from zonos.conditioning import make_cond_dict, supported_language_codes
from zonos.model import Zonos

from sinapsis_zonos.helpers.zonos_keys import SamplingParams, TTSKeys


def get_audio_prefix_codes(prefix_path: str | None, model: Zonos) -> torch.Tensor | None:
    """Generates audio prefix codes from an audio file.

    Args:
        prefix_path (str): Path to the audio file to generate the prefix codes from.
        model (Zonos): The Zonos model used to generate the audio prefix codes.

    Returns:
        torch.Tensor | None: The generated audio prefix codes if available, otherwise None.
    """
    if prefix_path:
        waveform, sample_rate = torchaudio.load(prefix_path)
        waveform = waveform.mean(0, keepdim=True)
        waveform = model.autoencoder.preprocess(waveform, sample_rate)
        return model.autoencoder.encode(waveform.unsqueeze(0))
    return None


def get_conditioning(
    attributes: TemplateAttributeType, model: Zonos, input_text: str, device: torch.device
) -> torch.Tensor:
    """
    Generates conditioning tensor for the input text, combining it with speaker embeddings and emotions.

    Args:
        attributes (TemplateAttributeType): attributes with configuration for the conditioning dictionary
        of the model.
        model (Zonos): Model to be used during inference, where the setup is modified.
        input_text (str): The text to be converted to speech.
        device (torch.device): Device where model should be loaded.

    Returns:
        torch.Tensor: The generated conditioning tensor for speech synthesis.
    """
    speaker_embedding = get_speaker_embedding(attributes.speaker_audio, attributes.unconditional_keys, model, device)
    emotion_data = get_emotion_tensor(attributes, device)
    validate_language(attributes)

    vq_data = torch.tensor([attributes.vq_score] * 8, device=device).unsqueeze(0)

    conditioning_dict = make_cond_dict(
        text=input_text,
        language=attributes.language,
        speaker=speaker_embedding,
        emotion=emotion_data,
        vqscore_8=vq_data,
        fmax=attributes.fmax,
        pitch_std=attributes.pitch_std,
        speaking_rate=attributes.speaking_rate,
        dnsmos_ovrl=attributes.dnsmos,
        speaker_noised=attributes.denoised_speaker,
        device=device,
        unconditional_keys=attributes.unconditional_keys,
    )
    return model.prepare_conditioning(conditioning_dict)


def get_emotion_tensor(attributes: TemplateAttributeType, device: torch.device) -> torch.Tensor:
    """
    Extracts or constructs an emotion tensor from the given attributes.

    If `attributes.emotions` is present, its values are serialized and converted into a tensor.
    If not, a default zero tensor of shape (8,) is returned, and the `emotion` key is
    added to `attributes.unconditional_keys` (if not already included) to indicate unconditional conditioning.

    Args:
        attributes (TemplateAttributeType): Attributes for Zonos TTS model configuration.
        device (torch.device): The device on which the tensor should be created.

    Returns:
        torch.Tensor: A tensor representing emotion values, either user-provided or default.
    """
    if attributes.emotions:
        emotion_values = list(map(float, attributes.emotions.model_dump().values()))
        return torch.tensor(emotion_values, device=device)
    else:
        if TTSKeys.emotion not in attributes.unconditional_keys:
            attributes.unconditional_keys.add(TTSKeys.emotion)
        return torch.tensor([0.0] * 8, device=device)


def get_sampling_params(sampling_params: SamplingParams | dict) -> dict:
    """
    Returns a dictionary of sampling parameters for audio generation.

    If `sampling_params` is a Pydantic model, its non-null fields are serialized using `model_dump()`.
    If `sampling_params` is empty, a default dictionary with a minimum probability value is returned.

    Args:
        sampling_params (SamplingParams | dict): A SamplingParams Pydantic model or dictionary.

    Returns:
        dict: A dictionary of sampling parameters, either user-defined or with a default fallback.
    """
    if isinstance(sampling_params, SamplingParams):
        return sampling_params.model_dump(exclude_none=True)
    return {TTSKeys.min_p: 0.1}


def get_speaker_embedding(
    speaker_path: str | None, unconditional_keys: Set[str], model: Zonos, device: torch.device
) -> torch.Tensor | None:
    """Extracts speaker embedding from an audio file.

    Args:
        speaker_path (str): Path to the audio file from which the speaker embedding will be extracted.
        unconditional_keys (dict): Dictionary of keys to condition speech synthesis.
            This will be used to determine whether a speaker embedding is needed.
        model (Zonos): The Zonos model used for generating the speaker embedding.

    Returns:
        torch.Tensor | None: The speaker embedding if available, otherwise None.
    """
    if speaker_path and TTSKeys.speaker not in unconditional_keys:
        waveform, sample_rate = torchaudio.load(speaker_path)
        speaker_embedding = model.make_speaker_embedding(waveform, sample_rate)
        return speaker_embedding.to(device, dtype=torch.bfloat16)
    return None


def init_seed(attributes: TemplateAttributeType) -> None:
    """Initializes the seed for reproducible results."""
    if attributes.randomized_seed:
        attributes.seed = torch.randint(0, 2**32 - 1, (1,)).item()
    torch.manual_seed(attributes.seed)


def validate_language(attributes: TemplateAttributeType) -> None:
    """
    Validates and updates the language attribute in the provided TTS configuration.

    Checks if `attributes.language` is included in the list of supported language codes.
    If the language is unsupported, logs an error and defaults it to `TTSKeys.en_language`.

    Args:
        attributes (TemplateAttributeType): The model attributes containing the language setting.
    """
    if attributes.language not in supported_language_codes:
        sinapsis_logger.error(f"Language {attributes.language} not supported. Defaulting to {TTSKeys.en_language}")
        attributes.language = TTSKeys.en_language
