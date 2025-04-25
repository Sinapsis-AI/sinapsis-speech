<h1 align="center">
<br>
<a href="https://sinapsis.tech/">
  <img
    src="https://github.com/Sinapsis-AI/brand-resources/blob/main/sinapsis_logo/4x/logo.png?raw=true"
    alt="" width="300">
</a><br>
Sinapsis F5-TTS
<br>
</h1>

<h4 align="center">Templates for advanced text-to-speech synthesis with F5-TTS</h4>

<p align="center">
<a href="#installation">🐍 Installation</a> •
<a href="#features"> 🚀 Features</a> •
<a href="#example"> 📚 Usage example</a> •
<a href="#webapp">🌐 Webapp</a> •
<a href="#documentation">📙 Documentation</a> •
<a href="#packages">🔍 License</a>
</p>

This **Sinapsis F5-TTS** package provides a template for seamlessly integrating, configuring, and running **text-to-speech (TTS)** functionalities powered by [F5TTS](https://github.com/SWivid/F5-TTS).

<h2 id="installation">🐍 Installation</h2>

Install using your favourite package manager. We strongly encourage the use of <code>uv</code>, although any other package manager should work too.
If you need to install <code>uv</code> please see the [official documentation](https://docs.astral.sh/uv/getting-started/installation/#installation-methods).

Example with <code>uv</code>:
```bash
  uv pip install sinapsis-f5-tts --extra-index-url https://pypi.sinapsis.tech
```
 or with raw <code>pip</code>:
```bash
  pip install sinapsis-f5-tts --extra-index-url https://pypi.sinapsis.tech
```

> [!IMPORTANT]
> Templates in each package may require extra dependencies. For development, we recommend installing the package with all the optional dependencies:
>
with <code>uv</code>:

```bash
  uv pip install sinapsis-f5-tts[all] --extra-index-url https://pypi.sinapsis.tech
```
 or with raw <code>pip</code>:
```bash
  pip install sinapsis-f5-tts[all] --extra-index-url https://pypi.sinapsis.tech
```

<h2 id="features">🚀 Features
</h2>


<h3>Templates Supported</h3>

This module includes a template for text-to-speech synthesis using the F5TTS model:

**F5TTSInference**: Converts text to speech using the F5TTS model with voice cloning capabilities. The template processes text packets from the input container, generates corresponding audio using F5TTS, and adds the resulting audio packets to the container.

<details>
<summary>Attributes</summary>

- `model`: Model name to use for inference (default: "F5TTS_v1_Base")
- `model_cfg`: Optional path to model configuration file
- `ckpt_file`: Optional path to model checkpoint file
- `vocab_file`: Optional path to vocabulary file
- `ref_audio`: Path to reference audio file for voice cloning (default: "artifacts/town.mp3")
- `ref_text`: Reference text corresponding to the reference audio (default: empty string)
- `vocoder_name`: Vocoder to use for waveform generation, either "vocos" or "bigvgan" (default: "vocos")
- `load_vocoder_from_local`: Whether to load vocoder from local path (default: False)
- `nfe_step`: Number of function evaluation steps for diffusion, higher values give better quality but slower inference (default: 32)
- `cfg_strength`: Classifier-free guidance strength, higher values give more stable output but less expressivity (default: 2.0)
- `cross_fade_duration`: Duration of cross-fade between audio segments in seconds (default: 0.15)
- `speed`: Speed factor for generated speech, values > 1 make speech faster, < 1 make it slower (default: 1.0)
- `sway_sampling_coef`: Coefficient for sway sampling (default: -1.0)
- `target_rms`: Target RMS value for audio normalization (default: None)
- `fix_duration`: Fixed duration for generated audio in seconds (default: None)
- `remove_silence`: Whether to remove silence from generated audio (default: False)
- `save_chunk`: Whether to save individual audio chunks (default: False)
- `device`: Device to use for inference, e.g., "cuda", "cpu" (default: None, auto-detect)
</details>

> [!TIP]
> Use CLI command ```sinapsis info --example-template-config TEMPLATE_NAME``` to produce an example Agent config for the Template specified in ***TEMPLATE_NAME***.

For example, for ***F5TTSInference*** use ```sinapsis info --example-template-config RFDETRTrain``` to produce an example config like:

```yaml
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

```


<h2 id='example'>📚 Usage example</h2>

This example illustrates how to use the **F5TTSInference** template for text-to-speech synthesis. It converts text input into speech using F5-TTS and saves the resulting audio file locally.

<details>
<summary ><strong><span style="font-size: 1.4em;">Config</span></strong></summary>

```yaml
agent:
  name: f5tts_agent
  description: "Agent that generates speech from text using the F5TTS model."

templates:
- template_name: InputTemplate
  class_name: InputTemplate
  attributes: {}

- template_name: TextInput
  class_name: TextInput
  template_input: InputTemplate
  attributes:
    source: "user_input"
    text: "A bottle of water with a soup"

- template_name: F5TTSInference
  class_name: F5TTSInference
  template_input: TextInput
  attributes:
    model: "F5TTS_v1_Base"
    ref_audio: "artifacts/small.mp3"
    ref_text: " "
    vocoder_name: "vocos"
    nfe_step: 32
    cfg_strength: 2.0
    cross_fade_duration: 0.15
    speed: 1.0
    sway_sampling_coef: -1

- template_name: SaveGeneratedAudio
  class_name: AudioWriterSoundfile
  template_input: F5TTSInference
  attributes:
    save_dir: "f5_tts"
    root_dir: "artifacts"
    extension: "wav"
```
</details>

This configuration defines an **agent** and a sequence of **templates** for converting text to speech using **F5-TTS**.

> [!IMPORTANT]
> The TextInput and AudioWriterSoundfile correspond to [sinapsis-data-readers](https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_readers) and [sinapsis-data-writers](https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_writers). If you want to use the example, please make sure you install the packages.
>

To run the config, use the CLI:
```bash
sinapsis run name_of_config.yml
```

<h2 id="webapp">🌐 Webapp</h2>
The webapp included in this project showcases the modularity of the F5TTS template for speech generation tasks.

> [!IMPORTANT]
> To run the app you first need to clone this repository:

```bash
git clone git@github.com:Sinapsis-ai/sinapsis-speech.git
cd sinapsis-speech
```

> [!NOTE]
> If you'd like to enable external app sharing in Gradio, `export GRADIO_SHARE_APP=True`

> [!IMPORTANT]
> F5TTS requires a reference audio file for voice cloning. Make sure you have a reference audio file in the artifacts directory.

<details>
<summary id="docker"><strong><span style="font-size: 1.4em;">🐳 Docker</span></strong></summary>

**IMPORTANT** This docker image depends on the sinapsis-nvidia:base image. Please refer to the official [sinapsis](https://github.com/Sinapsis-ai/sinapsis?tab=readme-ov-file#docker) instructions to Build with Docker.

1. **Build the sinapsis-speech image**:
```bash
docker compose -f docker/compose.yaml build
```

2. **Start the app container**:
```bash
docker compose -f docker/compose_apps.yaml up -d sinapsis-f5tts
```
3. **Check the logs**
```bash
docker logs -f sinapsis-f5tts
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
uv run webapps/packet_tts_apps/f5_tts_app.py
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
