# -*- coding: utf-8 -*-

import numpy as np
from llama_cpp import Llama
from orpheus_cpp import OrpheusCpp
from orpheus_cpp.model import TTSOptions
from pydantic import TypeAdapter
from sinapsis_core.data_containers.data_packet import (
    AudioPacket,
    DataContainer,
)
from sinapsis_core.template_base import Template
from sinapsis_core.template_base.base_models import (
    OutputTypes,
    TemplateAttributes,
    TemplateAttributeType,
    UIPropertiesMetadata,
)
from sinapsis_core.utils.env_var_keys import SINAPSIS_CACHE_DIR

from sinapsis_orpheus_cpp.thirdparty.helpers import download_model, setup_snac_session


class OrpheusTTSAttributes(TemplateAttributes):
    """Attributes configuration for Orpheus TTS Template.

    This class defines all configurable parameters for the Orpheus TTS model,
    including model configuration, GPU settings, and audio generation parameters.

    Attributes:
        n_gpu_layers (int): Number of model layers to offload to GPU.
            -1 means use all available layers on GPU for maximum performance.
            0 means use CPU only. Default: -1.
        n_threads (int): Number of CPU threads to use for model inference.
            0 means auto-detect optimal thread count. Default: 0.
        n_ctx (int): Context window size (maximum number of tokens).
            0 means use the model's maximum trained context size.
            Larger values require more GPU/RAM memory. Default: 8192.
        model_id (str): Hugging Face model repository ID.
            Must be a valid repository containing GGUF model files.
            Required parameter with no default.
        model_variant (str | None): Specific GGUF file to download from the repository.
            If None, will auto-detect based on model_id naming convention.
            Use this to specify exact quantization (e.g., "model-q4_k_m.gguf").
            Default: None.
        cache_dir (str): Directory to store downloaded models and cache files.
            Default: SINAPSIS_CACHE_DIR environment variable.
        verbose (bool): Enable verbose logging for model operations.
            Shows detailed model loading and inference information. Default: False.
        voice_id (str): Voice identifier for speech synthesis.
            Must be a valid voice supported by the Orpheus model.
            Available voices depend on the specific model variant.
            Required parameter with no default.
        batch_size (int): Batch size for model inference.
            Higher values may improve throughput but require more memory.
            Default: 1.
        max_tokens (int): Maximum number of tokens to generate for speech.
            Controls the length of generated audio sequences. Default: 2048.
        temperature (float): Sampling temperature for token generation.
            Higher values (>1.0) make output more random, lower values (<1.0)
            make it more deterministic. Default: 0.8.
        top_p (float): Nucleus sampling probability threshold.
            Only tokens with cumulative probability <= top_p are considered.
            Range: 0.0-1.0. Default: 0.95.
        top_k (int): Top-k sampling parameter.
            Only the top k most likely tokens are considered for sampling.
            Default: 40.
        min_p (float): Minimum probability threshold for token selection.
            Tokens with probability below this threshold are filtered out.
            Range: 0.0-1.0. Default: 0.05.
        pre_buffer_size (float): Duration in seconds of audio to generate
            before yielding the first chunk during streaming.
            Larger values provide smoother audio but higher latency.
            Default: 1.5.
    """

    n_gpu_layers: int = -1
    n_threads: int = 0
    n_ctx: int = 8192
    model_id: str
    model_variant: str | None = None
    cache_dir: str = SINAPSIS_CACHE_DIR
    verbose: bool = False
    voice_id: str
    batch_size: int = 1
    max_tokens: int = 2048
    temperature: float = 0.8
    top_p: float = 0.95
    top_k: int = 40
    min_p: float = 0.05
    pre_buffer_size: float = 1.5


class OrpheusTTS(Template):
    """Text-to-Speech template using Orpheus model for speech synthesis.

    This template converts text input into high-quality speech audio using
    the Orpheus neural TTS model. It handles model downloading, initialization,
    and audio generation with configurable voice parameters.

    Usage example:

    agent:
        name: my_test_agent
    templates:
    - template_name: InputTemplate
      class_name: InputTemplate
      attributes: {}
    - template_name: OrpheusTTS
      class_name: OrpheusTTS
      template_input: InputTemplate
      attributes:
        n_gpu_layers: -1
        n_threads: 0
        n_ctx: 8192
        model_id: '`replace_me:<class ''str''>`'
        model_variant: null
        cache_dir: ~/sinapsis
        verbose: false
        voice_id: '`replace_me:<class ''str''>`'
        batch_size: 1
        max_tokens: 2048
        temperature: 0.8
        top_p: 0.95
        top_k: 40
        min_p: 0.05
        pre_buffer_size: 1.5

    """

    AttributesBaseModel = OrpheusTTSAttributes
    UIProperties = UIPropertiesMetadata(category="TTS", output_type=OutputTypes.AUDIO)

    def __init__(self, attributes: TemplateAttributeType) -> None:
        super().__init__(attributes)
        self._engine: OrpheusCpp
        self._llm_available: bool = False
        self._initialize_engine()

    def _initialize_engine(self) -> None:
        """Initialize the OrpheusCpp engine with downloaded model.

        Creates a new OrpheusCpp instance without calling its constructor
        to avoid default parameter conflicts, then manually configures
        both the LLM and SNAC session components.

        Raises:
            ValueError: If model download fails.
            RuntimeError: If engine initialization fails.
        """
        self._engine = OrpheusCpp.__new__(OrpheusCpp)
        model_file = download_model(
            model_id=self.attributes.model_id,
            model_variant=self.attributes.model_variant,
            cache_dir=self.attributes.cache_dir,
        )
        self._setup_llm(model_file)
        self._setup_snac_session()

    def _setup_llm(self, model_file: str) -> None:
        """Setup the Large Language Model component with specified parameters.

        Initializes the Llama model with custom configuration parameters.
        Implements graceful error handling for Out-of-Memory conditions
        by setting the LLM as unavailable instead of crashing.

        Args:
            model_file (str): Path to the downloaded GGUF model file.

        Raises:
            ValueError: For non-OOM related model initialization errors.

        Note:
            If a "Failed to create llama_context" error occurs (typically OOM),
            the method logs the error and disables TTS functionality instead
            of terminating the program.
        """
        try:
            self._engine._llm = Llama(
                model_path=model_file,
                n_ctx=self.attributes.n_ctx,
                verbose=self.attributes.verbose,
                n_gpu_layers=self.attributes.n_gpu_layers,
                n_threads=self.attributes.n_threads,
                batch_size=self.attributes.batch_size,
            )
            self._llm_available = True
        except ValueError as e:
            if "Failed to create llama_context" in str(e):
                error_msg = (
                    f"Failed to create llama_context - Out of Memory (OOM) issue. "
                    f"Current n_ctx: {self.attributes.n_ctx}, n_gpu_layers: {self.attributes.n_gpu_layers}. "
                    f"Try reducing n_ctx or "
                    f"reduce n_gpu_layers if using GPU. "
                )
                self.logger.error(error_msg)
                self._engine._llm = None
                self._llm_available = False
            else:
                raise

    def _setup_snac_session(self) -> None:
        """
        Initializes the SNAC (Streaming Neural Audio Codec) session required
        for converting model tokens to audio waveforms. Only sets up the session
        if the LLM was successfully initialized.

        Note:
            SNAC session is only created when LLM is available to avoid
            unnecessary resource allocation when TTS is disabled.
        """
        if self._llm_available:
            self._engine._snac_session = setup_snac_session(self.attributes.cache_dir)
        else:
            self._engine._snac_session = None

    def _create_tts_options(self) -> TTSOptions:
        """
        Dynamically builds a TTSOptions dictionary by filtering template attributes
        to include only those that are valid TTSOptions parameters.

        Returns:
            TTSOptions: Dictionary containing TTS generation parameters.
        """
        tts_option_fields = TypeAdapter(TTSOptions)
        attributes_dict = self.attributes.model_dump()
        return tts_option_fields.validate_python(attributes_dict)

    def generate_speech(self, text: str) -> tuple[int, np.ndarray] | None:
        """
        Converts text to speech using the Orpheus TTS model with configured
        voice and generation parameters.

        Args:
            text (str): Input text to convert to speech.

        Returns:
            tuple[int, np.ndarray] | None: Tuple of (sample_rate, audio_array)
                if generation succeeds, None if LLM is unavailable.

        Note:
            Returns None when LLM is not available (e.g., due to OOM errors)
            instead of raising an exception, allowing graceful degradation.
        """
        if not self._llm_available:
            return None
        return self._engine.tts(text, options=self._create_tts_options())

    def create_audio_packet(self, text: str, source: str | None = None) -> AudioPacket | None:
        """
        Generates speech from text and wraps the result in a
        `AudioPacket` for data pipeline compatibility.

        Args:
            text (str): Input text to convert to speech.
            source (str | None): Optional source identifier for traceability.

        Returns:
            AudioPacket | None: Audio packet containing generated speech,
                or None if speech generation fails or is unavailable.
        """
        speech_result = self.generate_speech(text)
        if speech_result is None:
            return None

        sample_rate, audio_data = speech_result
        return AudioPacket(
            content=audio_data,
            source=source,
            sample_rate=sample_rate,
        )

    def execute(self, container: DataContainer) -> DataContainer:
        """
        Processes all text packets in the input container and generates
        corresponding audio packets using the Orpheus TTS model.

        Args:
            container (DataContainer): Input container with text packets to process.

        Returns:
            DataContainer: Updated container with generated audio packets added.

        Note:
            When LLM is unavailable (due to initialization failures), the method
            logs a warning and returns the container without modifications rather
            than raising an exception.
        """
        if not container.texts:
            return container

        if not self._llm_available:
            return container

        for text_packet in container.texts:
            audio_packet = self.create_audio_packet(text=text_packet.content, source=text_packet.source)
            if audio_packet is not None:
                container.audios.append(audio_packet)

        return container
