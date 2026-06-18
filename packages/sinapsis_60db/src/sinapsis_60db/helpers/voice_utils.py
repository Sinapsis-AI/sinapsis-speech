# -*- coding: utf-8 -*-
from sinapsis_core.data_containers.data_packet import TextPacket
from sinapsis_core.utils.logging_utils import sinapsis_logger

from sinapsis_60db.helpers.client import SixtyDBClient


def get_voice_id(client: SixtyDBClient, voice: str | None) -> str | None:
    """Resolves a voice name or ID to a 60dB ``voice_id``.

    Searches the account's voices (``GET /myvoices``) for a name or ID match. If
    ``voice`` is not provided, the first available voice is used as the default. If
    ``voice`` is provided but not found, it is assumed to already be a valid
    ``voice_id`` and returned as-is (with a warning).

    Args:
        client (SixtyDBClient): The 60dB API client instance.
        voice (str | None): The desired voice name or ID.

    Returns:
        str | None: The resolved voice ID, or ``None`` if no voice is available
            and none was provided (lets the API fall back to its system default).
    """
    if not voice:
        default_voice = get_default_voice(client)
        return default_voice.get("voice_id") if default_voice else None

    try:
        voices = client.get_voices()
        for v in voices:
            if voice in (v.get("name"), v.get("voice_id")):
                sinapsis_logger.debug(f"Voice {voice} resolved to ID: {v.get('voice_id')}")
                return v.get("voice_id")

        sinapsis_logger.warning(f"Voice '{voice}' not found in account voices; using it as a raw voice_id.")
        return voice
    except Exception as e:
        sinapsis_logger.error(f"Error resolving voice ID: {e}")
        raise


def get_default_voice(client: SixtyDBClient) -> dict | None:
    """Returns the first available voice as the default, or ``None`` if none exist."""
    try:
        voices = client.get_voices()
        if voices:
            return voices[0]
        sinapsis_logger.warning("No voices available on the 60dB account; relying on API default voice.")
        return None
    except Exception as e:
        sinapsis_logger.error(f"Error getting default voice: {e}")
        raise


def load_input_text(input_data: list[TextPacket]) -> str:
    """Loads and concatenates the text content from a list of TextPacket objects."""
    return "".join([item.content for item in input_data])
