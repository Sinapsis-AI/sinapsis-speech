# -*- coding: utf-8 -*-
from typing import Literal

from pydantic import BaseModel
from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class TTSKeys:
    """
    A class to hold constants for the keys used in the Text-to-Speech (TTS) model configuration.

    These keys represent standard fields that are used to configure various parameters of the TTS model,
    such as speaker attributes, emotions, and other audio-related settings. They are typically used in
    templates and potentially a TTS web application to adjust and access specific TTS settings."
    """

    speaker: Literal["speaker"] = "speaker"
    emotion: Literal["emotion"] = "emotion"
    vqscore_8: Literal["vqscore_8"] = "vqscore_8"
    fmax: Literal["fmax"] = "fmax"
    pitch_std: Literal["pitch_std"] = "pitch_std"
    speaking_rate: Literal["speaking_rate"] = "speaking_rate"
    dnsmos_ovrl: Literal["dnsmos_ovrl"] = "dnsmos_ovrl"
    speaker_noised: Literal["speaker_noised"] = "speaker_noised"
    wav: Literal["wav"] = "wav"
    en_language: Literal["en-us"] = "en-us"
    min_p: Literal["min_p"] = "min_p"


class SamplingParams(BaseModel):
    """
    A class to hold the sampling parameters for the TTS model.

    Attributes:
        min_p (float): Minimum token probability, scaled by the highest token probability. Range: 0-1. Default: 0.0.
        top_k (int): Number of top tokens to sample from. Range: 0-1024. Default: 0.
        top_p (float): Cumulative probability threshold for nucleus sampling. Range: 0-1. Default: 0.0.
        linear (float): Controls the token unusualness. Range: -2.0 to 2.0. Default: 0.0.
        conf (float): Confidence level for randomness. Range: -2.0 to 2.0. Default: 0.0.
        quad (float): Controls how much low probabilities are reduced. Range: -2.0 to 2.0. Default: 0.0.
    """

    min_p: float = 0.0
    top_k: int = 0
    top_p: float = 0.0
    linear: float = 0.0
    conf: float = 0.0
    quad: float = 0.0


class EmotionsConfig(BaseModel):
    """
    A class to hold emotional attributes that influence the tone of the generated speech.

    These emotions are represented as float values and are used to adjust the emotional tone of the speech.
    Higher values can represent a stronger presence of a particular emotion.
    """

    happiness: float = 0
    sadness: float = 0
    disgust: float = 0
    fear: float = 0
    surprise: float = 0
    anger: float = 0
    other: float = 0
    neutral: float = 0
