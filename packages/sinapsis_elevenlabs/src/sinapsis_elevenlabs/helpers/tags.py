# -*- coding: utf-8 -*-
from enum import Enum


class Tags(Enum):
    AUDIO = "audio"
    AUDIO_GENERATION = "audio_generation"
    ELEVENLABS = "elevenlabs"
    PROMPT = "prompt"
    SPEECH = "speech"
    SPEECH_TO_SPEECH = "speech_to_speech"
    TEXT_TO_SPEECH = "text_to_speech"
    VOICE_CONVERSION = "voice_conversion"
    VOICE_CLONING = "voice_cloning"
    VOICE_GENERATION = "voice_generation"
