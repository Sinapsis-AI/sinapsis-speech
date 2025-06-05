# -*- coding: utf-8 -*-
"""
Themethods declared in this file are inspired in the following source:

https://github.com/freddyaboulton/orpheus-cpp

which is Licensed under the MIT License.

"""

import onnxruntime
from huggingface_hub import hf_hub_download
from sinapsis_core.utils.logging_utils import sinapsis_logger


def download_model(cache_dir: str, model_id: str, model_variant: str | None = None) -> str | None:
    """
    Download a model from Hugging Face Hub.

    Args:
        model_id: The model ID on Hugging Face Hub.
        model_variant: The specific model variant file to download.
        cache_dir: Directory to store downloaded models.

    Returns:
        Path to the downloaded model file or None if download fails.
    """
    if model_variant:
        filename = model_variant
    elif model_id.endswith(("-GGUF", "-gguf")):
        filename = model_id.split("/")[-1].lower().replace("-gguf", ".gguf")
    else:
        filename = f"{model_id.split('/')[-1]}.gguf"

    sinapsis_logger.info(f"Downloading model {model_id} with filename {filename}")

    model_file = hf_hub_download(
        repo_id=model_id,
        filename=filename,
        cache_dir=cache_dir,
    )

    sinapsis_logger.info(f"Successfully downloaded model to {model_file}")
    return model_file


def setup_snac_session(cache_dir: str) -> onnxruntime.InferenceSession:
    """
    Download and setup the SNAC ONNX session for audio processing.

    Args:
        cache_dir: Directory to store downloaded models.

    Returns:
        Configured ONNX inference session.
    """
    repo_id = "onnx-community/snac_24khz-ONNX"
    snac_model_file = "decoder_model.onnx"
    snac_model_path = hf_hub_download(
        repo_id,
        subfolder="onnx",
        filename=snac_model_file,
        cache_dir=cache_dir,
    )

    return onnxruntime.InferenceSession(
        snac_model_path,
        providers=["CUDAExecutionProvider", "CPUExecutionProvider"],
    )
