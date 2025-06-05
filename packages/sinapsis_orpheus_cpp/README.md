<h1 align="center">
<br>
<a href="https://sinapsis.tech/">
  <img
    src="https://github.com/Sinapsis-AI/brand-resources/blob/main/sinapsis_logo/4x/logo.png?raw=true"
    alt="" width="300">
</a><br>
Sinapsis Orpheus-CPP
<br>
</h1>

<h4 align="center">Templates for advanced text-to-speech synthesis with Orpheus-TTS</h4>

<p align="center">
<a href="#installation">🐍 Installation</a> •
<a href="#features"> 🚀 Features</a> •
<a href="#example"> 📚 Usage example</a> •
<a href="#webapp">🌐 Webapp</a> •
<a href="#documentation">📙 Documentation</a> •
<a href="#packages">🔍 License</a>
</p>

This **Sinapsis Orpheus-TTS** package provides a template for seamlessly integrating, configuring, and running **text-to-speech (TTS)** functionalities powered by [Orpheus-TTS](https://github.com/shivammehta25/Orpheus).

<h2 id="installation">🐍 Installation</h2>

Install using your favourite package manager. We strongly encourage the use of <code>uv</code>, although any other package manager should work too.
If you need to install <code>uv</code> please see the [official documentation](https://docs.astral.sh/uv/getting-started/installation/#installation-methods).

Example with <code>uv</code>:
```bash
  uv pip install sinapsis-orpheus-tts --extra-index-url https://pypi.sinapsis.tech
```
 or with raw <code>pip</code>:
```bash
  pip install sinapsis-orpheus-tts --extra-index-url https://pypi.sinapsis.tech
```

> [!IMPORTANT]
> Templates in each package may require extra dependencies. For development, we recommend installing the package with all the optional dependencies:
>
with <code>uv</code>:

```bash
  uv pip install sinapsis-orpheus-tts[all] --extra-index-url https://pypi.sinapsis.tech
```
 or with raw <code>pip</code>:
```bash
  pip install sinapsis-orpheus-tts[all] --extra-index-url https://pypi.sinapsis.tech
```

<h2 id="features">🚀 Features
</h2>


<h3>Templates Supported</h3>

This module includes a template for text-to-speech synthesis using the Orpheus TTS model:

**OrpheusTTS**: Converts text to speech using the Orpheus TTS model with advanced neural voice synthesis. The template processes text packets from the input container, generates corresponding audio using Orpheus TTS, and adds the resulting audio packets to the container. Features graceful error handling for out-of-memory conditions.

<details>
<summary>Attributes</summary>

- `n_gpu_layers`: Number of model layers to offload to GPU (-1 = use all layers, 0 = CPU only) (default: -1)
- `n_threads`: Number of CPU threads to use for model inference (0 = auto-detect) (default: 0)
- `n_ctx`: Context window size (maximum number of tokens, 0 = use model's maximum) (default: 8192)
- `model_id`: Hugging Face model repository ID (required)
- `model_variant`: Specific GGUF file to download from the repository (default: None)
- `cache_dir`: Directory to store downloaded models and cache files (default: SINAPSIS_CACHE_DIR)
- `verbose`: Enable verbose logging for model operations (default: False)
- `voice_id`: Voice identifier for speech synthesis (required)
- `batch_size`: Batch size for model inference (default: 1)
- `max_tokens`: Maximum number of tokens to generate for speech (default: 2048)
- `temperature`: Sampling temperature for token generation (default: 0.8)
- `top_p`: Nucleus sampling probability threshold (default: 0.95)
- `top_k`: Top-k sampling parameter (default: 40)
- `min_p`: Minimum probability threshold for token selection (default: 0.05)
- `pre_buffer_size`: Duration in seconds of audio to generate before yielding the first chunk (default: 1.5)

</details>

> [!TIP]
> Use CLI command ```sinapsis info --example-template-config TEMPLATE_NAME``` to produce an example Agent config for the Template specified in ***TEMPLATE_NAME***.

For example, for ***OrpheusTTS*** use ```sinapsis info --example-template-config OrpheusTTS``` to produce an example config like:

```yaml
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
    cache_dir: ~/sinapsis_cache
    verbose: false
    voice_id: '`replace_me:<class ''str''>`'
    batch_size: 1
    max_tokens: 2048
    temperature: 0.8
    top_p: 0.95
    top_k: 40
    min_p: 0.05
    pre_buffer_size: 1.5
```


<h2 id='example'>📚 Usage example</h2>

This example illustrates how to use the **OrpheusTTS** template for text-to-speech synthesis. It converts text input into speech using Orpheus-TTS and saves the resulting audio file locally.

<details>
<summary ><strong><span style="font-size: 1.4em;">Config</span></strong></summary>

```yaml
agent:
  name: orpheus_tts_agent
  description: "Agent that generates speech from text using the Orpheus TTS model."

templates:
- template_name: InputTemplate
  class_name: InputTemplate
  attributes: {}

- template_name: TextInput
  class_name: TextInput
  template_input: InputTemplate
  attributes:
    source: "user_input"
    text: "Hi, I'm Tara. Welcome to Orpheus text-to-speech system! I can speak in a very natural way."

- template_name: OrpheusTTS
  class_name: OrpheusTTS
  template_input: TextInput
  attributes:
    n_gpu_layers: -1
    n_ctx: 4096
    model_id: "isaiahbjork/orpheus-3b-0.1-ft-Q4_K_M-GGUF"
    voice_id: "tara"
    temperature: 0.8
    top_p: 0.95
    top_k: 40
    min_p: 0.05
    pre_buffer_size: 1.5
    max_tokens: 2048

- template_name: SaveGeneratedAudio
  class_name: AudioWriterSoundfile
  template_input: OrpheusTTS
  attributes:
    save_dir: "orpheus_tts"
    root_dir: "artifacts"
    extension: "wav"
```
</details>

This configuration defines an **agent** and a sequence of **templates** for converting text to speech using **Orpheus-TTS**.

> [!IMPORTANT]
> The TextInput and AudioWriterSoundfile correspond to [sinapsis-data-writers](https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_writers). If you want to use the example, please make sure you install the packages.
>

To run the config, use the CLI:
```bash
sinapsis run name_of_config.yml
```

<h2 id="webapp">🌐 Webapp</h2>
The webapp included in this project showcases the modularity of the Orpheus TTS template for speech generation tasks.

> [!IMPORTANT]
> To run the app you first need to clone this repository:

```bash
git clone git@github.com:Sinapsis-ai/sinapsis-speech.git
cd sinapsis-speech
```

> [!NOTE]
> If you'd like to enable external app sharing in Gradio, `export GRADIO_SHARE_APP=True`

<details>
<summary id="docker"><strong><span style="font-size: 1.4em;">🐳 Docker</span></strong></summary>

**IMPORTANT** This docker image depends on the sinapsis-nvidia:base image. Please refer to the official [sinapsis](https://github.com/Sinapsis-ai/sinapsis?tab=readme-ov-file#docker) instructions to Build with Docker.

1. **Build the sinapsis-speech image**:
```bash
docker compose -f docker/compose.yaml build
```

2. **Start the app container**:
```bash
docker compose -f docker/compose_apps.yaml up -d sinapsis-orpheus-tts
```

3. **Check the logs**
```bash
docker logs -f sinapsis-orpheus-tts
```

4. **The logs will display the URL to access the webapp, e.g.,:**:
```bash
Running on local URL:  http://127.0.0.1:7860
```

**NOTE**: The url may be different, check the output of logs.

5. **To stop the app**:
```bash
docker compose -f docker/compose_apps.yaml down
```
</details>

<details>
<summary id="virtual-environment"><strong><span style="font-size: 1.4em;">💻 UV</span></strong></summary>

To run the webapp using the <code>uv</code> package manager, follow these steps:

1. **Export the environment variable to install the python bindings for llama-cpp**:

```bash
export CMAKE_ARGS="-DGGML_CUDA=on"
export FORCE_CMAKE="1"
```

2. **Export CUDACXX**:
```bash
export CUDACXX=$(command -v nvcc)
```

3. **Sync the virtual environment**:

```bash
uv sync --frozen
```
4. **Install the wheel**:

```bash
uv pip install sinapsis-speech[all] --extra-index-url https://pypi.sinapsis.tech
```
5. **Run the webapp**:

```bash
uv run webapps/packet_tts_apps/orpheus_tts_app.py
```
6. **The terminal will display the URL to access the webapp (e.g.)**:
```bash
Running on local URL:  http://127.0.0.1:7860
```
**NOTE**: The URL may vary; check the terminal output for the correct address.

</details>



<h2 id="documentation">📙 Documentation</h2>

Documentation is available on the [sinapsis website](https://docs.sinapsis.tech/docs)

Tutorials for different projects within sinapsis are available at [sinapsis tutorials page](https://docs.sinapsis.tech/tutorials)

<h2 id="license">🔍 License</h2>

This project is licensed under the AGPLv3 license, which encourages open collaboration and sharing. For more details, please refer to the [LICENSE](LICENSE) file.

For commercial use, please refer to our [official Sinapsis website](https://sinapsis.tech) for information on obtaining a commercial license.