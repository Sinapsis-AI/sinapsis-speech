# -*- coding: utf-8 -*-
from elevenlabs import VoiceSettings
from elevenlabs.client import DEFAULT_VOICE, ElevenLabs, VoiceId, VoiceName
from sinapsis_core.data_containers.data_packet import TextPacket
from sinapsis_core.utils.logging_utils import sinapsis_logger


def create_voice_settings(settings: VoiceSettings) -> VoiceSettings | None:
    """
    Creates or updates a `VoiceSettings` object based on the provided settings.

    Args:
        settings (VoiceSettings | None): An instance of `VoiceSettings` containing the settings to be applied.
            If `None`, the function returns the default settings.

    Returns:
        VoiceSettings: The provided `VoiceSettings` object if `settings` is not `None`. Otherwise,
            `DEFAULT_VOICE.settings` is returned.
    """
    if not settings:
        return DEFAULT_VOICE.settings

    return settings


def get_voice_id(client: ElevenLabs, voice: VoiceId | VoiceName) -> VoiceId:
    """
    Resolves the voice ID for a given voice name or ID.

    This function searches through available voices from the ElevenLabs API
    to match the provided voice name or ID. If the specified voice is not found,
    it logs the error and returns the first available voice ID as a fallback.

    Args:
        client (ElevenLabs): The ElevenLabs API client instance.
        voice (VoiceId | VoiceName): The name or ID of the desired voice.

    Returns:
        VoiceId: The resolved voice ID.

    Raises:
        ValueError: If no voices are available to resolve.
    """
    try:
        voices = client.voices.get_all().voices
        for v in voices:
            if voice == v.name or voice == v.voice_id:
                sinapsis_logger.debug("Voice '%s' resolved to ID: %s", voice, v.voice_id)
                return v.voice_id

        sinapsis_logger.error("Voice '%s' is not available.", voice)
        if voices:
            sinapsis_logger.info("Returning default voice ID: %s", voices[0].voice_id)
            return voices[0].voice_id

        raise ValueError("No available voices to resolve. Ensure the client is configured correctly.")
    except Exception as e:
        sinapsis_logger.error("Error resolving voice ID: %s", e)
        raise


def load_input_text(input_data: list[TextPacket]) -> str:
    """Loads and concatenates the text content from a list of TextPacket objects."""
    return "".join([item.content for item in input_data])
