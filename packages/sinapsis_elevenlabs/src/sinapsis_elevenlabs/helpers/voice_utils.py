# -*- coding: utf-8 -*-
import json

from elevenlabs import Voice, VoiceSettings
from elevenlabs.client import ElevenLabs
from sinapsis_core.data_containers.data_packet import TextPacket
from sinapsis_core.utils.logging_utils import sinapsis_logger


def create_voice_settings(settings: VoiceSettings, as_json: bool = False) -> VoiceSettings | None | str:
    """
    Creates or updates a `VoiceSettings` object based on the provided settings.

    Args:
        settings (VoiceSettings | None): An instance of `VoiceSettings` containing the settings to be applied.
            If `None`, the function returns the default settings.
        as_json (bool): Whether to return the settings as JSON string.

    Returns:
        VoiceSettings | None | str: The provided `VoiceSettings` object if `settings` is not `None`. Otherwise,
            `None` is returned for default settings.
    """
    if not settings:
        return None

    if as_json:
        return json.dumps(settings.model_dump(exclude_none=True))

    return settings


def get_voice_id(client: ElevenLabs, voice: str | Voice | None) -> str:
    """
    Resolves the voice ID for a given voice name or ID.

    This function searches through available voices from the ElevenLabs API
    to match the provided voice name or ID. If the specified voice is not found,
    it logs the error and returns the first available voice ID as a fallback.

    Args:
        client (ElevenLabs): The ElevenLabs API client instance.
        voice (str | Voice | None): The name or ID of the desired voice.

    Returns:
        str: The resolved voice ID.

    Raises:
        ValueError: If no voices are available to resolve.
    """
    if not voice:
        return get_default_voice(client).voice_id

    if isinstance(voice, Voice):
        sinapsis_logger.debug(f"Voice object provided, using voice_id: {voice.voice_id}")
        return voice.voice_id

    try:
        voices_response = client.voices.get_all()
        voices = voices_response.voices

        for v in voices:
            if voice == v.name or voice == v.voice_id:
                sinapsis_logger.debug(f"Voice {voice} resolved to ID: {v.voice_id}")
                return v.voice_id

        sinapsis_logger.error(f"Voice {voice} is not available.")
        if voices:
            sinapsis_logger.info(f"Returning default voice ID: {voices[0].voice_id}")
            return voices[0].voice_id

        raise ValueError("No available voices to resolve. Ensure the client is configured correctly.")
    except Exception as e:
        sinapsis_logger.error(f"Error resolving voice ID: {e}")
        raise


def get_default_voice(client: ElevenLabs) -> Voice:
    """
    Gets the first available voice as default.

    Args:
        client (ElevenLabs): The ElevenLabs API client instance.

    Returns:
        Voice: The default voice object.
    """
    try:
        voices_response = client.voices.get_all()
        voices = voices_response.voices
        if voices:
            return voices[0]
        raise ValueError("No voices available")
    except Exception as e:
        sinapsis_logger.error(f"Error getting default voice: {e}")
        raise


def load_input_text(input_data: list[TextPacket]) -> str:
    """Loads and concatenates the text content from a list of TextPacket objects."""
    return "".join([item.content for item in input_data])
