# -*- coding: utf-8 -*-

import gradio as gr
from sinapsis.webapp.tts_base import TTSAppAudioFromGeneric
from sinapsis_core.data_containers.data_packet import (
    AudioPacket,
    DataContainer,
    TextPacket,
)
from sinapsis_core.utils.env_var_keys import (
    AGENT_CONFIG_PATH,
    GRADIO_SHARE_APP,
    SINAPSIS_CACHE_DIR,
)

CONFIG_PATH = (
    AGENT_CONFIG_PATH or "packages/sinapsis_elevenlabs/src/sinapsis_elevenlabs/configs/elevenlabs_voice_clone_demo.yaml"
)
GENERIC_KEY = "ElevenLabsVoiceClone"


class ElevenLabsVoiceCloneApp(TTSAppAudioFromGeneric):
    def audio_and_text_to_agent(self, audio_file: str, text_to_convert: str) -> tuple[gr.Audio | None, str | None]:
        """
        Processes the reference audio and text input to perform voice cloning and speech synthesis.

        Args:
            audio_file (str): File path to the uploaded or recorded audio sample.
            text_to_convert (str): The text to synthesize using the cloned voice.

        Returns:
            tuple[gr.Audio | None, str | None]: Tuple containing the generated audio and a status message.
        """
        if self.initialized_state:
            if not audio_file or len(text_to_convert) < 100:
                gr.Warning("The audio sample is required and the text to convert must be at least 100 characters long.")
                return None, "Please provide a valid audio sample and text to convert."

            with open(audio_file, "rb") as f:
                audio_bytes = f.read()

            container = DataContainer(
                audios=[AudioPacket(content=audio_bytes)],
                texts=[TextPacket(content=text_to_convert)],
            )
            output_container = self.agent(container)
            audio_path = self._postprocess_output(output_container, self.generic_key_or_base_path)

            if audio_path:
                return gr.Audio(audio_path, visible=True), None
            raise gr.Error("Unable to generate speech with cloned voice")

        return None, "#### Model not ready! Please wait..."

    def inner_tts_functionality(self) -> None:
        """
        Defines the Gradio interface components and their interactions for the voice cloning app.
        Extends the base class functionality to include audio input for voice cloning.
        """
        audio_input = gr.Audio(
            sources=["upload", "microphone"],
            type="filepath",
            label="Upload or record your reference audio (for cloning):",
        )

        text_input = gr.Textbox(
            submit_btn=True,
            label="Text to convert:",
            value="The Sinapsis platform aims to democratize artificial intelligence by offering "
            "a flexible template system that ensures modularity and compatibility between models and tools widely "
            "used by the community.",
        )

        status_msg = self.update_status_msg()
        audio_generated = gr.Audio(label="Cloned voice output:", visible=False)
        status_msg = gr.Markdown()
        text_input.submit(
            self.audio_and_text_to_agent,
            inputs=[audio_input, text_input],
            outputs=[audio_generated, status_msg],
        )


if __name__ == "__main__":
    app = ElevenLabsVoiceCloneApp(CONFIG_PATH, GENERIC_KEY, "ElevenLabs", "Voice Clone")
    app.launch(share=GRADIO_SHARE_APP, allowed_paths=[SINAPSIS_CACHE_DIR])
