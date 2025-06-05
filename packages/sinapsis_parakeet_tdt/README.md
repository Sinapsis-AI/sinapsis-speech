<h1 align="center">
<br>
<a href="https://sinapsis.tech/">
  <img
    src="https://github.com/Sinapsis-AI/brand-resources/blob/main/sinapsis_logo/4x/logo.png?raw=true"
    alt="" width="300">
</a><br>
Sinapsis Parakeet TDT
<br>
</h1>

<h4 align="center">Templates for advanced speech-to-text transcription with NVIDIA Parakeet TDT</h4>

<p align="center">
<a href="#installation">🐍 Installation</a> •
<a href="#features"> 🚀 Features</a> •
<a href="#example"> 📚 Usage example</a> •
<a href="#webapp">🌐 Webapp</a> •
<a href="#documentation">📙 Documentation</a> •
<a href="#license">🔍 License</a>
</p>

This **Sinapsis Parakeet TDT** package provides a template for seamlessly integrating, configuring, and running **speech-to-text (STT)** functionalities powered by [NVIDIA's Parakeet TDT model](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v2).

<h2 id="installation">🐍 Installation</h2>

Install using your favourite package manager. We strongly encourage the use of <code>uv</code>, although any other package manager should work too.
If you need to install <code>uv</code> please see the [official documentation](https://docs.astral.sh/uv/getting-started/installation/#installation-methods).

Example with <code>uv</code>:
```bash
  uv pip install sinapsis-parkeet-tdt --extra-index-url https://pypi.sinapsis.tech
```
 or with raw <code>pip</code>:
```bash
  pip install sinapsis-parkeet-tdt --extra-index-url https://pypi.sinapsis.tech
```

> [!IMPORTANT]
> Templates in each package may require extra dependencies. For development, we recommend installing the package with all the optional dependencies:
>
with <code>uv</code>:

```bash
  uv pip install sinapsis-parkeet-tdt[all] --extra-index-url https://pypi.sinapsis.tech
```
 or with raw <code>pip</code>:
```bash
  pip install sinapsis-parkeet-tdt[all] --extra-index-url https://pypi.sinapsis.tech
```

<h2 id="features">🚀 Features</h2>

<h3>Templates Supported</h3>

This module includes a template for speech-to-text transcription using the Parakeet TDT model:

**ParakeetTDTInference**: Converts speech to text using NVIDIA's Parakeet TDT 0.6B model. This template processes audio packets from the input container or specified file paths, performs transcription with optional timestamp prediction, and adds the resulting text packets to the container.

<details>
<summary>Attributes</summary>

- `model_name (str)`: Name or path of the Parakeet TDT model. Defaults to "nvidia/parakeet-tdt-0.6b-v2".
- `audio_paths (list[str] | None)`: Optional list of audio file paths to transcribe. If None, audio will be taken from the AudioPackets in the DataContainer. Defaults to None.
- `enable_timestamps (bool)`: Whether to generate timestamps for the transcription. Defaults to False.
- `timestamp_level (Literal["char", "word", "segment"])`: Level of timestamp detail. Defaults to "word".
- `device (Literal["cpu", "cuda"])`: Device to run the model on. Defaults to "cuda".
- `refresh_cache (bool)`: Whether to refresh the cache when downloading the model. Defaults to False.
</details>

> [!TIP]
> Use CLI command ```sinapsis info --example-template-config TEMPLATE_NAME``` to produce an example Agent config for the Template specified in ***TEMPLATE_NAME***.

For example, for ***ParakeetTDTInference*** use ```sinapsis info --example-template-config ParakeetTDTInference``` to produce an example config like:

```yaml
agent:
  name: my_test_agent
templates:
- template_name: InputTemplate
  class_name: InputTemplate
  attributes: {}
- template_name: ParakeetTDTInference
  class_name: ParakeetTDTInference
  template_input: InputTemplate
  attributes:
    model_name: "nvidia/parakeet-tdt-0.6b-v2"
    audio_paths: []
    enable_timestamps: false
    timestamp_level: "word"
    device: "cuda"
    refresh_cache: false
```

<h2 id='example'>📚 Usage example</h2>

This example illustrates how to use the **ParakeetTDTInference** template for speech-to-text transcription. It converts audio input into text using NVIDIA's Parakeet TDT model.

<details>
<summary><strong><span style="font-size: 1.4em;">Config</span></strong></summary>

```yaml
agent:
  name: parakeet_tdt_agent
  description: "Agent that transcribes speech to text using the NVIDIA Parakeet TDT model."

templates:
- template_name: InputTemplate
  class_name: InputTemplate
  attributes: {}

- template_name: AudioReaderSoundfile
  class_name: AudioReaderSoundfile
  template_input: InputTemplate
  attributes:
    audio_file_path: "artifacts/sample.wav"
    source: "artifacts/sample.wav"

- template_name: ParakeetTDTInference
  class_name: ParakeetTDTInference
  template_input: AudioReaderSoundfile
  attributes:
    model_name: "nvidia/parakeet-tdt-0.6b-v2"
    enable_timestamps: true
    timestamp_level: "word"
    device: "cuda"
```
</details>

This configuration defines a complete pipeline for speech-to-text transcription:

1. First, an audio file is read using the AudioReaderSoundfile template
2. The audio is then processed by the ParakeetTDTInference template, which transcribes it to text
3. The transcription is saved to a text file using the TextWriter template

> [!IMPORTANT]
> The AudioReaderSoundfile and TextWriter templates correspond to [sinapsis-data-readers](https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_readers). If you want to use the example, please make sure you install these packages.
>

To run the config, use the CLI:
```bash
sinapsis run name_of_config.yml
```

<h2 id="webapp">🌐 Webapp</h2>
The webapp included in this project showcases the capabilities of the Parakeet TDT model for speech recognition tasks.

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
docker compose -f docker/compose_apps.yaml up -d sinapsis-parakeet-tdt
```

3. **Check the logs**
```bash
docker logs -f sinapsis-parakeet-tdt
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

1. **Sync the virtual environment**:

```bash
uv sync --frozen
```
2. **Install the wheel**:

```bash
uv pip install sinapsis-speech[all] --extra-index-url https://pypi.sinapsis.tech
```
3. **Run the webapp**:

```bash
uv run webapps/speech_to_text_apps/parakeet_tdt_app.py
```
4. **The terminal will display the URL to access the webapp (e.g.)**:
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