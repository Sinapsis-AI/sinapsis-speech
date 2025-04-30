# -*- coding: utf-8 -*-
import os
import subprocess
import tempfile
from typing import Any, Literal

import numpy as np
import soundfile as sf
from pydantic import Field
from pydantic.dataclasses import dataclass
from sinapsis_core.data_containers.data_packet import (
    AudioPacket,
    DataContainer,
)
from sinapsis_core.template_base import Template
from sinapsis_core.template_base.base_models import OutputTypes, TemplateAttributes, UIPropertiesMetadata


@dataclass
class F5CliKeys:
    cli_flag: str = "cli_flag"
    cli_param: str = "cli_param"


class F5TTSInferenceAttributes(TemplateAttributes):
    """Configuration attributes for the F5TTS text-to-speech inference template.

    Attributes:
        model (str): The model name to use for synthesis. Options include 'F5TTS_v1_Base',
            'F5TTS_Base', 'E2TTS_Base', etc. Default is 'F5TTS_v1_Base'.
        model_cfg (str | None): Path to the F5-TTS model config file (.yaml). If None,
            the default configuration will be used.
        ckpt_file (str | None): Path to model checkpoint file (.pt). If None, the default
            checkpoint will be used.
        vocab_file (str | None): Path to vocabulary file (.txt). If None, the default
            vocabulary will be used.
        ref_audio (str): Path to the reference audio file. This is required to clone the voice
            characteristics.
        ref_text (str): The transcript/subtitle for the reference audio. Default is a space character.
            When left empty, the system will attempt to extract text from the audio automatically.
            It's recommended to leave this empty for automatic extraction.
        vocoder_name (Literal["vocos", "bigvgan"]): The vocoder to use for audio generation.
            Options are 'vocos' or 'bigvgan'. Default is 'vocos'.
        load_vocoder_from_local (bool): Whether to load the vocoder from a local directory
            (default: ../checkpoints/vocos-mel-24khz) instead of downloading it. Default is False.
        nfe_step (int): The number of function evaluation steps (denoising steps) to perform
            during inference. Higher values may produce better quality at the cost of speed. Default is 32.
        cfg_strength (float): Classifier-free guidance strength. Controls how closely the output
            follows the reference voice. Default is 2.0.
        cross_fade_duration (float): Duration of cross-fade between audio segments in seconds.
            Used when generating longer audio that requires multiple segments. Default is 0.15.
        speed (float): The speed of the generated audio. Values > 1.0 speed up the audio,
            values < 1.0 slow it down. Default is 1.0.
        sway_sampling_coef (float): Sway Sampling coefficient for controlling variability
            in the generated speech. Default is -1.0.
        target_rms (float | None): Target output speech loudness normalization value.
            Controls the volume of the output. Default is None.
        fix_duration (float | None): Fix the total duration (reference and generated audios)
            in seconds. Default is None.
        remove_silence (bool): Whether to remove long silence found in the output. Default is False.
        save_chunk (bool): Whether to save each audio chunk during inference. Useful for
            debugging or analyzing the generation process. Default is False.
        device (str | None): Specify the device to run inference on (e.g., 'cuda:0', 'cpu').
            Default is None, which uses the system's default device.
    """

    model: str = Field(default="F5TTS_v1_Base", json_schema_extra={F5CliKeys.cli_param: "-m"})

    model_cfg: str | None = Field(default=None, json_schema_extra={F5CliKeys.cli_param: "-mc"})

    ckpt_file: str | None = Field(default=None, json_schema_extra={F5CliKeys.cli_param: "-p"})

    vocab_file: str | None = Field(default=None, json_schema_extra={F5CliKeys.cli_param: "-v"})

    ref_audio: str = Field(json_schema_extra={F5CliKeys.cli_param: "-r"})

    ref_text: str = Field(default=" ", json_schema_extra={F5CliKeys.cli_param: "-s"})

    vocoder_name: Literal["vocos", "bigvgan"] = Field(
        default="vocos", json_schema_extra={F5CliKeys.cli_param: "--vocoder_name"}
    )

    load_vocoder_from_local: bool = Field(
        default=False, json_schema_extra={F5CliKeys.cli_flag: "--load_vocoder_from_local"}
    )

    nfe_step: int = Field(default=32, json_schema_extra={F5CliKeys.cli_param: "--nfe_step"})

    cfg_strength: float = Field(default=2.0, json_schema_extra={F5CliKeys.cli_param: "--cfg_strength"})

    cross_fade_duration: float = Field(default=0.15, json_schema_extra={F5CliKeys.cli_param: "--cross_fade_duration"})

    speed: float = Field(default=1.0, json_schema_extra={F5CliKeys.cli_param: "--speed"})

    sway_sampling_coef: float = Field(default=-1.0, json_schema_extra={F5CliKeys.cli_param: "--sway_sampling_coef"})

    target_rms: float | None = Field(default=None, json_schema_extra={F5CliKeys.cli_param: "--target_rms"})

    fix_duration: float | None = Field(default=None, json_schema_extra={F5CliKeys.cli_param: "--fix_duration"})

    remove_silence: bool = Field(default=False, json_schema_extra={F5CliKeys.cli_flag: "--remove_silence"})

    save_chunk: bool = Field(default=False, json_schema_extra={F5CliKeys.cli_flag: "--save_chunk"})

    device: str | None = Field(default=None, json_schema_extra={F5CliKeys.cli_param: "--device"})


class F5TTSInference(Template):
    """Template for performing text-to-speech synthesis using the F5TTS model.

    This template uses the F5TTS CLI tool to generate speech from text input.
    It processes text packets from the input container, generates corresponding
    audio using F5TTS, and adds the resulting audio packets to the container.

    Usage example:

    agent:
      name: my_test_agent
    templates:
    - template_name: InputTemplate
      class_name: InputTemplate
      attributes: {}
    - template_name: F5TTSInference
      class_name: F5TTSInference
      template_input: InputTemplate
      attributes:
        model: F5TTS_v1_Base
        model_cfg: null
        ckpt_file: null
        vocab_file: null
        ref_audio: '`replace_me:<class ''str''>`'
        ref_text: ' '
        vocoder_name: vocos
        load_vocoder_from_local: false
        nfe_step: 32
        cfg_strength: 2.0
        cross_fade_duration: 0.15
        speed: 1.0
        sway_sampling_coef: -1.0
        target_rms: null
        fix_duration: null
        remove_silence: false
        save_chunk: false
        device: null

    """

    AttributesBaseModel = F5TTSInferenceAttributes
    UIProperties = UIPropertiesMetadata(category="F5TTS", output_type=OutputTypes.AUDIO)

    def _add_attribute_to_command(self, cli_command: list[str], field_name: str, field: Any) -> None:
        """
        This method examines each attribute field's metadata to determine if and how
        it should be added to the CLI command. It handles both parameter-style options
        (--param value) and flag-style options (--flag).

        Args:
            cli_command (list[str]): The command list being built, modified in-place.
                This list will be extended with the appropriate CLI arguments.
            field_name (str): Name of the attribute field to process from the template's
                attributes.
            field (Any): Field definition containing metadata about the attribute,
                including CLI parameter information.
        """
        attribute_value = getattr(self.attributes, field_name)
        json_schema_extra = field.json_schema_extra

        if json_schema_extra is None:
            return

        if F5CliKeys.cli_param in json_schema_extra and attribute_value is not None:
            cli_param = json_schema_extra[F5CliKeys.cli_param]
            cli_command.extend([cli_param, str(attribute_value)])

        if F5CliKeys.cli_flag in json_schema_extra and attribute_value:
            cli_flag = json_schema_extra[F5CliKeys.cli_flag]
            cli_command.append(cli_flag)

    @staticmethod
    def _add_io_parameters(cli_command: list[str], input_text: str, output_file_path: str) -> None:
        """
        Configures the input text to synthesize and the output location for the
        generated audio file. Sets up the output directory based on the temporary
        file path and adds the necessary CLI parameters.

        Args:
            cli_command (list[str]): The command list being built, modified in-place.
                This list will be extended with the input/output CLI arguments.
            input_text (str): The text to synthesize into speech. This will be passed
                to the F5TTS CLI with the -t/--gen_text parameter.
            output_file_path (str): Path where the generated audio file will be saved.
                This will be passed to the F5TTS CLI with the -w/--output_file parameter.
        """
        temp_dir = os.path.dirname(output_file_path)
        cli_command.extend(["-o", temp_dir])
        cli_command.extend(["-t", input_text, "-w", output_file_path])

    def _build_cli_command(self, input_text: str, output_file_path: str) -> list[str]:
        """Builds the complete F5TTS CLI command for speech synthesis.

        Constructs a command list that includes:
        1. The base CLI command
        2. All applicable template attributes converted to CLI parameters
        3. Input/output parameters for text and audio file paths

        Args:
            input_text (str): The text to synthesize into speech.
            output_file_path (str): Path where the generated audio file will be saved.

        Returns:
            list[str]: A list of strings representing the complete command to be executed
                by the subprocess module. The command includes all necessary parameters
                and flags for the F5TTS CLI tool.
        """
        cli_command = ["f5-tts_infer-cli"]

        for field_name, field in self.AttributesBaseModel.model_fields.items():
            self._add_attribute_to_command(cli_command, field_name, field)

        self._add_io_parameters(cli_command, input_text, output_file_path)
        return cli_command

    def _run_cli_command(self, cli_command: list[str]) -> bool:
        """
        Runs the constructed CLI command as a subprocess, captures its output,
        and logs the results. Handles both successful execution and errors.

        Args:
            cli_command (list[str]): The complete command list to execute.
                This should be a list of strings as produced by _build_cli_command().

        Returns:
            bool: True if the command executed successfully (return code 0),
                False if an error occurred during execution.
        """
        try:
            process_result = subprocess.run(cli_command, capture_output=True, text=True, check=True)
            self.logger.info(f"Command output: {process_result.stdout}")
            if process_result.stderr:
                self.logger.info(f"Command stderr: {process_result.stderr}")
            return True
        except subprocess.CalledProcessError as error:
            self.logger.error(f"CLI error: {error.stderr}")
            return False

    def _load_audio_file(self, file_path: str) -> tuple[np.ndarray, int] | None:
        """Loads audio data from a file using soundfile.

        Attempts to read an audio file from the specified path and returns the
        audio data as a numpy array along with its sample rate. Handles file
        existence checks and error conditions.

        Args:
            file_path (str): Path to the audio file to load. This should be a
                valid audio file format supported by the soundfile library.

        Returns:
            tuple[np.ndarray, int] | None: A tuple containing audio data as a numpy array of shape (samples, channels)
                and sample rate as an integer in Hz. Or None if the file could not be read or does not exist.
        """
        if not os.path.exists(file_path):
            self.logger.error(f"Output file not found: {file_path}")
            return None

        try:
            return sf.read(file_path)
        except (ValueError, RuntimeError, IOError) as error:
            self.logger.error(f"Error reading audio file: {error!s}")
            return None

    def _generate_speech(self, input_text: str) -> tuple[np.ndarray, int] | None:
        """Generates speech audio from the input text using F5TTS.

        This method orchestrates the entire speech generation process:
        1. Creates a temporary file for the output audio
        2. Builds and executes the F5TTS CLI command
        3. Loads the resulting audio file
        4. Cleans up the temporary file

        The method ensures proper resource cleanup even if errors occur during
        the generation process.

        Args:
            input_text (str): The text to synthesize into speech. This text will
                be passed to the F5TTS CLI tool for synthesis.

        Returns:
            tuple[np.ndarray, int] | None: A tuple containing:
                - The generated audio data as a numpy array
                - The sample rate as an integer in Hz
                Or None if speech generation failed at any stage.
        """
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_file_path = temp_file.name

        try:
            cli_command = self._build_cli_command(input_text, temp_file_path)
            if not self._run_cli_command(cli_command):
                return None

            audio_data = self._load_audio_file(temp_file_path)
            return audio_data
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    def _create_audio_packet(
        self,
        audio_data: np.ndarray,
        sample_rate: int,
        container: DataContainer,
    ) -> None:
        """Creates an audio packet and adds it to the data container.

        Constructs an AudioPacket object from the generated speech data and
        adds it to the container's audio collection. The packet includes
        metadata about the source (this template instance) and audio properties.

        Args:
            audio_data (np.ndarray): The audio samples as a numpy array of shape
                (samples, channels).
            sample_rate (int): The sample rate of the audio in Hz.
            container (DataContainer): The data container to add the audio packet to.
                The packet will be appended to the container's audios list.
        """
        audio_packet = AudioPacket(
            content=audio_data,
            source=self.instance_name,
            sample_rate=sample_rate,
        )
        container.audios.append(audio_packet)

    def execute(self, container: DataContainer) -> DataContainer:
        """Processes text packets and generates corresponding speech audio.

        Args:
            container (DataContainer): The data container with text packets to process.
                Each text packet's content will be synthesized into speech.

        Returns:
            DataContainer: The same data container with added audio packets containing
                the generated speech. If no text packets were present or speech generation
                failed for all texts, the container is returned unchanged.
        """
        if not container.texts:
            return container

        for text_packet in container.texts:
            speech_result = self._generate_speech(text_packet.content)

            if speech_result:
                audio_data, sample_rate = speech_result
                self._create_audio_packet(
                    audio_data=audio_data,
                    sample_rate=sample_rate,
                    container=container,
                )

        return container
