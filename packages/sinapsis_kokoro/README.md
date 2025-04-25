<h1 align="center">
<br>
<a href="https://sinapsis.tech/">
  <img
    src="https://github.com/Sinapsis-AI/brand-resources/blob/main/sinapsis_logo/4x/logo.png?raw=true"
    alt="" width="300">
</a><br>
Sinapsis Kokoro
<br>
</h1>

<h4 align="center">Templates for advanced text-to-speech synthesis using the Kokoro 82M v1.0 model</h4>

<p align="center">
<a href="#installation">🐍 Installation</a> •
<a href="#features"> 🚀 Features</a> •
<a href="#example"> 📚 Usage example</a> •
<a href="#webapp">🌐 Webapp</a> •
<a href="#documentation">📙 Documentation</a> •
<a href="#packages">🔍 License</a>
</p>

This **Sinapsis Kokoro** package package provides a single template for integrating, configuring, and running **text-to-speech (TTS)** functionalities powered by [Kokoro](https://huggingface.co/hexgrad/Kokoro-82M).

<h2 id="installation">🐍 Installation</h2>

Install using your preferred package manager. We strongly recommend using <code>uv</code>. To install <code>uv</code>, refer to the [official documentation](https://docs.astral.sh/uv/getting-started/installation/#installation-methods).


Install with <code>uv</code>:
```bash
  uv pip install sinapsis-kokoro --extra-index-url https://pypi.sinapsis.tech
```
Or with raw <code>pip</code>:
```bash
  pip install sinapsis-kokoro --extra-index-url https://pypi.sinapsis.tech
```

> [!IMPORTANT]
> Templates in each package may require additional dependencies. For development, we recommend installing the package with all the optional dependencies:
>
With <code>uv</code>:

```bash
  uv pip install sinapsis-kokoro[all] --extra-index-url https://pypi.sinapsis.tech
```
 or with raw <code>pip</code>:
```bash
  pip install sinapsis-kokoro[all] --extra-index-url https://pypi.sinapsis.tech
```

> [!NOTE]
Zonos depends on the eSpeak library phonemization. The installation depends on your OS. For Linux:
```bash
apt install -y espeak-ng
```

<h2 id="features">🚀 Features
</h2>


<h3>Templates Supported</h3>

This module includes a template for text-to-speech synthesis using the Kokoro TTS model:

- **KokoroTTS**: Converts text to speech using the Kokoro TTS model. The template processes text packets from the input container, generates corresponding audio using Kokoro, and adds the resulting audio packets to the container.

  <details>
  <summary>Attributes</summary>

  - `speed` (Optional): The speed at which the speech will be generated     (default: `1`).
  - `split_pattern` (Optional): The regular expression pattern used to split the input text into smaller chunks (default: `r"\+"`).
  - `voice` (Optional): The voice model to use for speech synthesis (default:`af_heart`).

  The list of languages and voices supported by Kokoro can be found [here](https:/huggingface.co/hexgrad/Kokoro-82M/blobmain/VOICES.md)
  </details>

> [!TIP]
> Use CLI command ```sinapsis info --example-template-config TEMPLATE_NAME``` to produce an example Agent config for the Template specified in ***TEMPLATE_NAME***.

For example, for ***KokoroTTS*** use ```sinapsis info --example-template-config KokoroTTS``` to produce an example config like:

```yaml
agent:
  name: my_test_agent
templates:
- template_name: InputTemplate
  class_name: InputTemplate
  attributes: {}
- template_name: KokoroTTS
  class_name: KokoroTTS
  template_input: InputTemplate
  attributes:
    speed: 1
    split_pattern: \n+
    voice: af_heart

```

<h2 id='example'>📚 Usage example</h2>

This example illustrates how to use the **KokoroTTS** template for text-to-speech synthesis. It converts text input into speech using the Kokoro 82M v1.0 model and saves the resulting audio files locally.

<details>
<summary ><strong><span style="font-size: 1.4em;">Config</span></strong></summary>

```yaml
agent:
  name: kokoro_tts_agent
  description: "Agent that generates speech from text using the Kokoro-TTS model."

templates:
- template_name: InputTemplate
  class_name: InputTemplate
  attributes: {}

- template_name: TextInput
  class_name: TextInput
  template_input: InputTemplate
  attributes:
    text: "[Kokoro](/kˈOkəɹO/) is an open-weight TTS model with 82 million parameters. Despite its lightweight architecture, it delivers comparable quality to larger models while being significantly faster and more cost-efficient. With Apache-licensed weights, [Kokoro](/kˈOkəɹO/) can be deployed anywhere from production environments to personal projects."

- template_name: KokoroTTS
  class_name: KokoroTTS
  template_input: TextInput
  attributes:
    speed: 1
    voice: af_heart

- template_name: AudioWriterSoundfile
  class_name: AudioWriterSoundfile
  template_input: KokoroTTS
  attributes:
    save_dir: "kokoro_tts"
    extension: "wav"

```
</details>

This configuration defines an **agent** and a sequence of **templates** for converting text to speech using **Kokoro**.

> [!IMPORTANT]
> The TextInput and AudioWriterSoundfile correspond to [sinapsis-data-readers](https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_readers) and [sinapsis-data-writers](https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_writers). If you want to use the example, please make sure you install the packages.
>

To run the config, use the CLI:
```bash
sinapsis run name_of_config.yml
```

<h2 id="webapp">🌐 Webapp</h2>
The webapp included in this project showcases the modularity of the `KokoroTTS` template for speech generation tasks.

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
docker compose -f docker/compose_apps.yaml up -d sinapsis-kokoro
```
3. **Check the logs**
```bash
docker logs -f sinapsis-kokoro
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
uv run webapps/packet_tts_apps/kokoro_tts_app.py
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
