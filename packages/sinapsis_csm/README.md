<h1 align="center">
<br>
<a href="https://sinapsis.tech/">
  <img
    src="https://github.com/Sinapsis-AI/brand-resources/blob/main/sinapsis_logo/4x/logo.png?raw=true"
    alt="" width="300">
</a><br>
Sinapsis CSM
<br>
</h1>

<p align="center">
<a href="#installation">🐍 Installation</a> •
<a href="#features">🚀 Features</a> •
<a href="#example">📚 Usage example</a> •
<a href="#documentation">📙 Documentation</a> •
<a href="#license">🔍 License</a>
</p>

This **Sinapsis CSM** package integrates a lightweight, efficient text-to-speech engine using the CSM model. It provides a simple template to convert input text into speech using Sinapsis.

---

<h2 id="installation">🐍 Installation</h2>

> [!IMPORTANT]
> Sinapsis project requires Python 3.10 or higher.

Install using your preferred package manager. We strongly recommend using <code>uv</code>. To install <code>uv</code>, refer to the [official documentation](https://docs.astral.sh/uv/getting-started/installation/#installation-methods).

Install with <code>uv</code>:
```bash
uv pip install sinapsis-csm --extra-index-url https://pypi.sinapsis.tech
```

Or with raw <code>pip</code>:
```bash
pip install sinapsis-csm --extra-index-url https://pypi.sinapsis.tech
```

> [!IMPORTANT]
> Templates in each package may require additional dependencies. For development, we recommend installing the package with all the optional dependencies:

With <code>uv</code>:
```bash
uv pip install sinapsis-csm[all] --extra-index-url https://pypi.sinapsis.tech
```

Or with raw <code>pip</code>:
```bash
pip install sinapsis-csm[all] --extra-index-url https://pypi.sinapsis.tech
```

To run this package you need a HuggingFace token. See the [official instructions](https://huggingface.co/docs/hub/security-tokens)
and set it using
```bash
export HF_TOKEN=<token-provided-by-hf>
```

and test it through the cli or the webapp.

Access to the following models is needed:

* [Llama-3.2-1B](https://huggingface.co/meta-llama/Llama-3.2-1B)
* [CSM-1B](https://huggingface.co/sesame/csm-1b)

---

<h2 id="features">🚀 Features</h2>

<h3>Templates Supported</h3>

- **CSMTTS**: Converts text into speech using the CSM model.

  <details>
  <summary>Attributes</summary>

  - `speaker_id` (int, default: 0): Speaker identity index.
  - `max_audio_length_ms` (int, default: 10000): Max audio length in milliseconds.
  - `device` ("cpu" or "cuda", default: "cpu"): Device used for inference.
  - `context` (context: list[str] | None = None): Optional list of past utterances for context.
  - `sample_rate_hz` (int, default: 24000): Output audio sample rate.
  </details>

---

<h2 id="example">📚 Usage example</h2>

This example shows how to use the **CSMTTS** template to convert text into speech and save it to disk.

<details>
<summary><strong><span style="font-size: 1.2em;">Agent config</span></strong></summary>

```yaml
agent:
  name: csm_tts_agent
  description: Agent that synthesizes speech from text using the CSM model.

templates:
  - template_name: InputTemplate
    class_name: InputTemplate
    attributes: {}

  - template_name: TextInput
    class_name: TextInput
    template_input: InputTemplate
    attributes:
      text: "Hi, my name is Taylor and this is Sinapsis"

  - template_name: CSMTTS
    class_name: CSMTTS
    template_input: TextInput
    attributes:
      speaker_id: 0
      max_audio_length_ms: 10000
      device: cpu
      context: null
      sample_rate_hz: 24000

  - template_name: AudioWriterSoundFile
    class_name: AudioWriterSoundFile
    template_input: CSMTTS
    attributes:
      save_dir: csm_tts
      extension: wav
```

</details>

To run the config, use:

```bash
sinapsis run packages/sinapsis_csm/src/sinapsis_csm/configs/csm_agent.yml
```

> [!NOTE]
> The `TextInput` and `AudioWriterSoundFile` templates come from the [sinapsis-data-readers](https://github.com/Sinapsis-AI/sinapsis-data-tools) and [sinapsis-data-writers](https://github.com/Sinapsis-AI/sinapsis-data-tools) packages. Make sure they are installed to use this example.

---


<h2 id="webapp">🌐 Webapp</h2>
The webapp included in this project showcases the modularity of the CSM template for speech generation tasks.

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
docker compose -f docker/compose_apps.yaml up -d sinapsis-csm
```
3. **Check the logs**
```bash
docker logs -f sinapsis-csm
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
uv run webapps/packet_tts_apps/csm_tts_app.py
```
4. **The terminal will display the URL to access the webapp (e.g.)**:
```bash
Running on local URL:  http://127.0.0.1:7860
```
**NOTE**: The URL may vary; check the terminal output for the correct address.

</details>



<h2 id="documentation">📙 Documentation</h2>

Documentation is available on the [Sinapsis website](https://docs.sinapsis.tech/docs).

Tutorials and guides for different templates and agents are available at [docs.sinapsis.tech/tutorials](https://docs.sinapsis.tech/tutorials).

---

<h2 id="license">🔍 License</h2>

This project is licensed under the AGPLv3 license, which encourages open collaboration and sharing. For more details, please refer to the [LICENSE](LICENSE) file.

For commercial use, please refer to our [official Sinapsis website](https://sinapsis.tech) for information on obtaining a commercial license.