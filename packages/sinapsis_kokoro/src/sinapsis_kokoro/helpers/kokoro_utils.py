# -*- coding: utf-8 -*-
from typing import Literal

from pydantic.dataclasses import dataclass

kokoro_voices = Literal[
    "af_heart",
    "af_alloy",
    "af_aoede",
    "af_bella",
    "af_jessicaaf_kore",
    "af_nicole",
    "af_nova",
    "af_river",
    "af_sarah",
    "af_sky",
    "am_adam",
    "am_echo",
    "am_eric",
    "am_fenrir",
    "am_liam",
    "am_michael",
    "am_onyx",
    "am_puck",
    "am_santa",
    "bf_alice",
    "bf_emma",
    "bf_isabella",
    "bf_lily",
    "bm_daniel",
    "bm_fable",
    "bm_george",
    "bm_lewis",
    "jf_alpha",
    "jf_gongitsune",
    "jf_nezumi",
    "jf_tebukuro",
    "jm_kumo",
    "zf_xiaobei",
    "zf_xiaoni",
    "zf_xiaoxiao",
    "zf_xiaoyi",
    "zm_yunjian",
    "zm_yunxi",
    "zm_yunxia",
    "zm_yunyang",
    "ef_dora",
    "em_alex",
    "em_santa",
    "ff_siwis",
    "hf_alpha",
    "hf_beta",
    "hm_omega",
    "hm_psi",
    "if_sara",
    "im_nicola",
    "pf_dora",
    "pm_alex",
    "pm_santa",
]


@dataclass(frozen=True)
class KokoroKeys:
    """
    A class to hold constants for the keys used in the Text-to-Speech (TTS) model configuration.

    These keys represent standard fields that are used to configure various parameters of the TTS model,
    such as speaker attributes, emotions, and other audio-related settings. They are typically used in
    templates and potentially a TTS web application to adjust and access specific TTS settings."
    """

    repo_id: Literal["hexgrad/Kokoro-82M"] = "hexgrad/Kokoro-82M"
    default_voice: Literal["af_heart"] = "af_heart"
