# -*- coding: utf-8 -*-
import gradio as gr
from helpers import add_logos_and_title
from sinapsis.webapp.agent_gradio_helper import css_header
from sinapsis.webapp.tts_base import TTSAppAudioFromGeneric
from sinapsis_core.data_containers.data_packet import AudioPacket, DataContainer
from sinapsis_core.utils.env_var_keys import AGENT_CONFIG_PATH, GRADIO_SHARE_APP, SINAPSIS_CACHE_DIR

CONFIG_PATH = (
    AGENT_CONFIG_PATH or "packages/sinapsis_elevenlabs/src/sinapsis_elevenlabs/configs/elevenlabs_sts_demo.yaml"
)
GENERIC_KEY = "ElevenLabsSTS"


class ElevenLabsSTSApp(TTSAppAudioFromGeneric):
    def audio_to_agent(self, initialized: bool, audio_file: str) -> tuple[gr.Audio | None, str | None]:
        """
        Processes the input audio for speech-to-speech conversion.

        Args:
            initialized (bool): Whether the agent is initialized and ready.
            agent (Agent): The Sinapsis agent instance.
            audio_file (str): File path to the uploaded or recorded audio sample.

        Returns:
            tuple[gr.Audio | None, str | None]: Tuple containing the generated audio and a status message.
        """
        if initialized:
            if not audio_file:
                gr.Warning("The audio sample is required.")
                return None, "Please provide a valid audio sample."
            with open(audio_file, "rb") as f:
                audio_bytes = f.read()
            container = DataContainer(audios=[AudioPacket(content=audio_bytes)])
            output_container = self.agent(container)
            audio_path = self._postprocess_output(output_container, self.generic_key_or_base_path)
            if audio_path:
                return gr.Audio(audio_path, visible=True), None
            raise gr.Error("Unable to process audio")
        return None, "#### Model not ready! Please wait..."

    def inner_tts_functionality(self) -> None:
        """
        Defines the Gradio interface components and their interactions for the speech-to-speech app.

        Args:
            interface (gr.Interface): The Gradio interface context.
        """
        initialized_state = gr.State(True)
        audio_input = gr.Audio(sources=["upload", "microphone"], type="filepath", label="Upload or record your audio:")
        status_msg = gr.Markdown("#### Initializing model...")
        initialized_state.change(self.update_status_msg, outputs=[status_msg])
        audio_generated = gr.Audio(label="Output audio:", visible=False)
        audio_input.change(
            self.audio_to_agent,
            inputs=[initialized_state, audio_input],
            outputs=[audio_generated, status_msg],
        )

    def __call__(self) -> gr.Blocks:
        with gr.Blocks(css=css_header()) as sts_interface:
            add_logos_and_title("Sinapsis ElevenLabs Speech-to-Speech demo")
            self.inner_tts_functionality()
        return sts_interface


if __name__ == "__main__":
    app = ElevenLabsSTSApp(CONFIG_PATH, GENERIC_KEY, "ElevenLabs", "Speech-to-Speech")
    app.launch(share=GRADIO_SHARE_APP, allowed_paths=[SINAPSIS_CACHE_DIR])
