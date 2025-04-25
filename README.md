<h1 align="center">
<br>
<a href="https://sinapsis.tech/">
  <img
    src="https://github.com/Sinapsis-AI/brand-resources/blob/main/sinapsis_logo/4x/logo.png?raw=true"
    alt="" width="300">
</a><br>
Sinapsis Speech
<br>
</h1>

<h4 align="center"> Templates for a wide range of voice generation tasks.</h4>

<p align="center">
<a href="#installation">🐍 Installation</a> •
<a href="#packages">📦 Packages</a> •
<a href="#webapp">🌐 Webapps</a> •
<a href="#documentation">📙 Documentation</a> •
<a href="#packages">🔍 License</a>
</p>


<h2 id="installation">🐍 Installation</h2>


> [!IMPORTANT]
> Sinapsis projects requires Python 3.10 or higher.
>

This repo includes packages for performing speech synthesis using different tools:

* <code>sinapsis-elevenlabs</code>
* <code>sinapsis-f5-tts</code>
* * <code>sinapsis-kokoro</code>
* <code>sinapsis-zonos</code>

Install using your preferred package manager. We strongly recommend using <code>uv</code>. To install <code>uv</code>, refer to the [official documentation](https://docs.astral.sh/uv/getting-started/installation/#installation-methods).


Install with <code>uv</code>:
```bash
uv pip install sinapsis-elevenlabs --extra-index-url https://pypi.sinapsis.tech
```
Or with raw <code>pip</code>:
```bash
pip install sinapsis-elevenlabs --extra-index-url https://pypi.sinapsis.tech
```

**Replace `sinapsis-elevenlabs` with the name of the package you intend to install**.

> [!IMPORTANT]
> Templates in each package may require additional dependencies. For development, we recommend installing the package all optional dependencies:
>
With <code>uv</code>:

```bash
uv pip install sinapsis-elevenlabs[all] --extra-index-url https://pypi.sinapsis.tech
```
Or with raw <code>pip</code>:
```bash
pip install sinapsis-elevenlabs[all] --extra-index-url https://pypi.sinapsis.tech
```

**Be sure to substitute `sinapsis-elevenlabs` with the appropriate package name**.



> [!TIP]
> You can also install all the packages within this project:
>
```bash
uv pip install sinapsis-speech[all] --extra-index-url https://pypi.sinapsis.tech
```


<h2 id="packages">📦 Packages</h2>

This repository is organized into modular packages, each designed for integration with different text-to-speech tools. These packages provide ready-to-use templates for speech synthesis. Below is an overview of the available packages:

<details>
<summary id="elevenlabs"><strong><span style="font-size: 1.4em;"> Sinapsis ElevenLabs </span></strong></summary>

This package offers a suite of templates and utilities designed for effortless integrating, configuration, and execution of **text-to-speech (TTS)** and **voice generation** functionalities powered by [ElevenLabs](https://elevenlabs.io/).

- **ElevenLabsTTS**: Template for converting text into speech using ElevenLabs' voice models.

- **ElevenLabsVoiceGeneration**: Template for generating custom synthetic voices based on user-provided descriptions.

For specific instructions and further details, see the [README.md](https://github.com/Sinapsis-AI/sinapsis-speech/blob/main/packages/sinapsis_elevenlabs/README.md).

</details>


<details>
<summary id="f5tts"><strong><span style="font-size: 1.4em;"> Sinapsis F5-TTS</span></strong></summary>

This package provides a template for seamlessly integrating, configuring, and running **text-to-speech (TTS)** functionalities powered by [F5TTS](https://github.com/SWivid/F5-TTS).

- **F5TTSInference**: Converts text to speech using the F5TTS model with voice cloning capabilities.

For specific instructions and further details, see the [README.md](https://github.com/Sinapsis-AI/sinapsis-speech/blob/main/packages/sinapsis_f5_tts/README.md).

</details>
<details>
<summary id="f5tts"><strong><span style="font-size: 1.4em;"> Sinapsis Kokoro</span></strong></summary>

This package provides a single template for integrating, configuring, and running text-to-speech (TTS) synthesis using the [Kokoro 82M v1.0](https://huggingface.co/hexgrad/Kokoro-82M) model.

KokoroTTS: Converts text to speech using the Kokoro TTS model. The template processes text packets from the input container, generates corresponding audio using Kokoro, and adds the resulting audio packets to the container.
For specific instructions and further details, see the [README.md](https://github.com/Sinapsis-AI/sinapsis-speech/blob/main/packages/sinapsis_kokoro/README.md).
</details>
<details>
<summary id="zonos"><strong><span style="font-size: 1.4em;"> Sinapsis Zonos</span></strong></summary>

This package provides a single template for integrating, configuring, and running **text-to-speech (TTS)** and **voice cloning** functionalities powered by [Zonos](https://github.com/Zyphra/Zonos/tree/main).

- **ZonosTTS**: Template for converting text to speech or performing voice cloning based on the presence of an audio sample.​

For specific instructions and further details, see the [README.md](https://github.com/Sinapsis-AI/sinapsis-speech/blob/main/packages/sinapsis_zonos/README.md).

</details>

<h2 id="webapp">🌐 Webapps</h2>
The webapps included in this project showcase the modularity of the templates, in this case for speech generation tasks.

> [!IMPORTANT]
> To run the app you first need to clone this repository:

```bash
git clone git@github.com:Sinapsis-ai/sinapsis-speech.git
cd sinapsis-speech
```

> [!NOTE]
> If you'd like to enable external app sharing in Gradio, `export GRADIO_SHARE_APP=True`


> [!IMPORTANT]
> Elevenlabs requires an API key to run any inference. To get started, visit the [official website](https://elevenlabs.io) and create an account. If you already have an account, go to the [API keys page](https://elevenlabs.io/app/settings/api-keys) to generate a token.

> [!IMPORTANT]
> Set your env var using <code> export ELEVENLABS_API_KEY='your-api-key'</code>

> [!IMPORTANT]
> F5-TTS requires a reference audio file for voice cloning. Make sure you have a reference audio file in the artifacts directory.

> [!NOTE]
> Agent configuration can be changed through the `AGENT_CONFIG_PATH` env var. You can check the available configurations in each package configs folder.

<details>
<summary id="docker"><strong><span style="font-size: 1.4em;">🐳 Docker</span></strong></summary>

**IMPORTANT**: This Docker image depends on the `sinapsis-nvidia:base` image. For detailed instructions, please refer to the [Sinapsis README](https://github.com/Sinapsis-ai/sinapsis?tab=readme-ov-file#docker).

1. **Build the sinapsis-speech image**:

```bash
docker compose -f docker/compose.yaml build
```


2. **Start the app container**:

- For ElevenLabs:
```bash
docker compose -f docker/compose_apps.yaml up -d sinapsis-elevenlabs
```
- For F5-TTS:
```bash
docker compose -f docker/compose_apps.yaml up -d sinapsis-f5_tts
```

- For Kokoro:

```bash
docker compose -f docker/compose_apps.yaml up -d sinapsis-kokoro
```

- For Zonos:
```bash
docker compose -f docker/compose_apps.yaml up -d sinapsis-zonos
```

3. **Check the logs**

- For ElevenLabs:
```bash
docker logs -f sinapsis-elevenlabs
```
- For F5-TTS:
```bash
docker logs -f sinapsis-f5tts
```
- For Kokoro:
```bash
docker logs -f sinapsis-kokoro
```

- For Zonos:
```bash
docker logs -f sinapsis-zonos
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

- For ElevenLabs:
```bash
uv run webapps/generic_tts_apps/elevenlabs_tts_app.py
```
- For F5-TTS:
```bash
uv run webapps/packet_tts_apps/f5_tts_app.py
```

- For Kokoro:
```bash
uv run webapps/packet_tts_apps/kokoro_tts_app.py
```
- For Zonos:
```bash
uv run webapps/generic_tts_apps/zonos_tts_app.py
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



