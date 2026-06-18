# -*- coding: utf-8 -*-
from enum import Enum


class Tags(str, Enum):
    AUDIO = "audio"
    AUDIO_GENERATION = "audio_generation"
    SIXTYDB = "60db"
    SPEECH = "speech"
    STREAMING = "streaming"
    TEXT_TO_SPEECH = "text_to_speech"
    WEBSOCKET = "websocket"
