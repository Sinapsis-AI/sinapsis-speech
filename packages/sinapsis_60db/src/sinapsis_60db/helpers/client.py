# -*- coding: utf-8 -*-
"""Lightweight client for the 60dB REST and WebSocket speech APIs.

60dB does not ship an official Python SDK, so this module provides a thin wrapper
around its HTTP endpoints. The interface intentionally mirrors the shape used by
the ElevenLabs SDK (``client.text_to_speech(...)``, ``client.get_voices()``, ...)
so the Sinapsis templates can stay consistent across both vendors.
"""

import base64
import json
from typing import Iterator

import requests
from sinapsis_core.utils.logging_utils import sinapsis_logger

DEFAULT_BASE_URL = "https://api.60db.ai"
DEFAULT_WS_URL = "wss://api.60db.ai/ws/tts"
DEFAULT_TIMEOUT = 120


class SixtyDBClient:
    """Thin synchronous client for the 60dB speech API.

    Args:
        api_key (str): The API key used to authenticate against the 60dB API.
        base_url (str): The REST base URL. Defaults to ``https://api.60db.ai``.
        ws_url (str): The WebSocket TTS URL. Defaults to ``wss://api.60db.ai/ws/tts``.
        timeout (int): Per-request timeout (seconds) for the REST calls.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        ws_url: str = DEFAULT_WS_URL,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.ws_url = ws_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
        )

    def get_voices(self) -> list[dict]:
        """Returns the list of voices available to the account (``GET /myvoices``)."""
        response = self.session.get(f"{self.base_url}/myvoices", timeout=self.timeout)
        response.raise_for_status()
        payload = response.json()
        return payload.get("data", []) or []

    @staticmethod
    def _build_payload(
        text: str,
        voice_id: str | None,
        output_format: str,
        enhance: bool,
        speed: float,
        stability: float,
        similarity: float,
    ) -> dict:
        """Builds the JSON body shared by the synthesize and stream endpoints."""
        payload: dict = {
            "text": text,
            "enhance": enhance,
            "speed": speed,
            "stability": stability,
            "similarity": similarity,
            "output_format": output_format,
        }
        if voice_id:
            payload["voice_id"] = voice_id
        return payload

    def text_to_speech(
        self,
        text: str,
        voice_id: str | None = None,
        output_format: str = "mp3",
        enhance: bool = True,
        speed: float = 1.0,
        stability: float = 50.0,
        similarity: float = 75.0,
    ) -> bytes:
        """Synthesizes speech in a single request (``POST /tts-synthesize``).

        Returns:
            bytes: The decoded audio bytes (the API returns base64-encoded audio).
        """
        payload = self._build_payload(text, voice_id, output_format, enhance, speed, stability, similarity)
        response = self.session.post(f"{self.base_url}/tts-synthesize", json=payload, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()
        if not data.get("success", True):
            raise RuntimeError(f"60dB TTS request failed: {data.get('message')}")
        audio_base64 = data.get("audio_base64")
        if not audio_base64:
            raise ValueError("60dB response did not contain 'audio_base64'.")
        return base64.b64decode(audio_base64)

    def text_to_speech_stream(
        self,
        text: str,
        voice_id: str | None = None,
        output_format: str = "mp3",
        enhance: bool = True,
        speed: float = 1.0,
        stability: float = 50.0,
        similarity: float = 75.0,
    ) -> Iterator[bytes]:
        """Streams synthesized speech (``POST /tts-stream``).

        The endpoint responds with newline-delimited JSON (NDJSON). Each line is an
        object whose ``type`` is one of ``chunk`` (base64 audio in
        ``result.audioContent``), ``complete`` (end of stream), or ``error``.

        Yields:
            bytes: Decoded audio chunks, in order.
        """
        payload = self._build_payload(text, voice_id, output_format, enhance, speed, stability, similarity)
        with self.session.post(
            f"{self.base_url}/tts-stream",
            json=payload,
            stream=True,
            timeout=self.timeout,
        ) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if not line:
                    continue
                obj = json.loads(line)
                msg_type = obj.get("type")
                if msg_type == "error":
                    raise RuntimeError(f"60dB stream error: {obj.get('message') or obj.get('result')}")
                if msg_type == "complete":
                    break
                result = obj.get("result") or obj
                audio_base64 = result.get("audioContent")
                if audio_base64:
                    yield base64.b64decode(audio_base64)

    def text_to_speech_websocket(
        self,
        text: str,
        voice_id: str,
        audio_encoding: str = "OGG_OPUS",
        sample_rate_hertz: int = 48000,
        speed: float = 1.0,
        stability: float = 50.0,
        similarity: float = 75.0,
        context_id: str = "sinapsis",
    ) -> bytes:
        """Synthesizes speech over the WebSocket API (``wss://.../ws/tts``).

        Opens a context, sends the full text, flushes, and collects every
        ``audio_chunk`` until ``flush_completed`` is received, then closes the
        context. Returns the concatenated audio bytes.

        Args:
            text (str): Text to synthesize (cumulative max 50,000 characters).
            voice_id (str): The voice identifier (required by the WS protocol).
            audio_encoding (str): One of LINEAR16, PCM, MULAW, ULAW, OGG_OPUS.
            sample_rate_hertz (int): One of 8000, 16000, 24000, 48000.
        """
        # Imported lazily so the REST templates do not require the websockets dependency.
        from websockets.exceptions import ConnectionClosed
        from websockets.sync.client import connect

        url = f"{self.ws_url}?apiKey={self.api_key}"
        chunks: list[bytes] = []
        with connect(url) as websocket:
            websocket.send(
                json.dumps(
                    {
                        "type": "create_context",
                        "context_id": context_id,
                        "voice_id": voice_id,
                        "audio_config": {
                            "audio_encoding": audio_encoding,
                            "sample_rate_hertz": sample_rate_hertz,
                        },
                        "speed": speed,
                        "stability": stability,
                        "similarity": similarity,
                    }
                )
            )
            websocket.send(json.dumps({"type": "send_text", "context_id": context_id, "text": text}))
            websocket.send(json.dumps({"type": "flush_context", "context_id": context_id}))

            while True:
                try:
                    message = websocket.recv()
                except ConnectionClosed:
                    break
                obj = json.loads(message)
                msg_type = obj.get("type")
                if msg_type == "audio_chunk":
                    audio_base64 = obj.get("audioContent")
                    if audio_base64:
                        chunks.append(base64.b64decode(audio_base64))
                elif msg_type == "flush_completed":
                    break
                elif msg_type == "error":
                    raise RuntimeError(f"60dB websocket error: {obj.get('message')}")

            try:
                websocket.send(json.dumps({"type": "close_context", "context_id": context_id}))
            except Exception as e:  # noqa: BLE001 - best-effort close, connection may already be gone
                sinapsis_logger.debug(f"Could not send close_context cleanly: {e}")

        return b"".join(chunks)
