<h1 align="center">
<br>
<a href="https://sinapsis.tech/">
  <img
    src="https://github.com/Sinapsis-AI/brand-resources/blob/main/sinapsis_logo/4x/logo.png?raw=true"
    alt="" width="300">
</a><br>
Sinapsis 60dB
<br>
</h1>

<h4 align="center">Templates for speech generation with the 60dB speech API</h4>

<p align="center">
<a href="#installation">🐍 Installation</a> •
<a href="#features"> 🚀 Features</a> •
<a href="#example"> 📚 Usage example</a> •
<a href="#webapp">🌐 Webapp</a> •
<a href="#documentation">📙 Documentation</a> •
<a href="#license">🔍 License</a>
</p>

This **Sinapsis 60dB** package offers a suite of templates and utilities for **text-to-speech (TTS)** powered by [60dB](https://60db.ai/), available as single-request synthesis, NDJSON streaming, and WebSocket streaming. It mirrors the structure of the **Sinapsis ElevenLabs** package so both vendors can be used interchangeably inside a Sinapsis pipeline.

<h2 id="installation">🐍 Installation</h2>

> [!IMPORTANT]
> Sinapsis project requires Python 3.10 or higher.

Install with <code>uv</code>:
```bash
  uv pip install sinapsis-60db --extra-index-url https://pypi.sinapsis.tech
```
Or with raw <code>pip</code>:
```bash
  pip install sinapsis-60db --extra-index-url https://pypi.sinapsis.tech
```

> [!IMPORTANT]
> Templates in each package may require additional dependencies. For development, we recommend installing the package with all the optional dependencies:

With <code>uv</code>:
```bash
  uv pip install sinapsis-60db[all] --extra-index-url https://pypi.sinapsis.tech
```
Or with raw <code>pip</code>:
```bash
  pip install sinapsis-60db[all] --extra-index-url https://pypi.sinapsis.tech
```

<h2 id="features">🚀 Features</h2>

<h3>Templates Supported</h3>

- **SixtyDBTTS**: Convert text into speech in a single request (`POST /tts-synthesize`).

    <details>
    <summary>Attributes</summary>

    - `api_key`(Optional): API key for 60dB. Must be provided either here or via the `SIXTYDB_API_KEY` environment variable.
    - `voice`(Optional): Voice name or ID. If `None`, the first available account voice (or the API default) is used.
    - `output_format`(Optional): Output audio format (default: `mp3`). Options: `mp3`, `wav`, `ogg`, `flac`.
    - `enhance`(Optional): Apply 60dB audio enhancement (default: `true`).
    - `speed`(Optional): Speech speed, range 0.5–2.0 (default: 1.0).
    - `stability`(Optional): Expressiveness vs. consistency, range 0–100 (default: 50).
    - `similarity`(Optional): Source-voice matching, range 0–100 (default: 75).
    </details>

- **SixtyDBTTSStream**: Convert text into speech and consume the NDJSON streaming response (`POST /tts-stream`).

    <details>
    <summary>Attributes</summary>

    Same as **SixtyDBTTS**, plus `stream` (kept for parity). Audio chunks are joined into a single AudioPacket.
    </details>

- **SixtyDBTTSWebSocket**: Convert text into speech over the WebSocket API (`wss://api.60db.ai/ws/tts`).

    <details>
    <summary>Attributes</summary>

    - `api_key`, `voice`, `speed`, `stability`, `similarity`: as above.
    - `audio_encoding`(Optional): One of `LINEAR16`, `PCM`, `MULAW`, `ULAW`, `OGG_OPUS` (default: `OGG_OPUS`). Raw PCM (`LINEAR16`/`PCM`) is decoded directly using `sample_rate_hertz`.
    - `sample_rate_hertz`(Optional): One of `8000`, `16000`, `24000`, `48000` (default: `48000`).
    - `context_id`(Optional): WebSocket session/context identifier (default: `sinapsis`).
    </details>

> [!TIP]
> Use CLI command ```sinapsis info --example-template-config TEMPLATE_NAME``` to produce an example Agent config for the Template specified in ***TEMPLATE_NAME***.

<h2 id='example'>📚 Usage example</h2>

This example uses the **SixtyDBTTS** template to convert text into speech and save the resulting audio file locally.

<details>
<summary><strong><span style="font-size: 1.4em;">Config</span></strong></summary>

```yaml
agent:
  name: text_to_speech
  description: text to speech agent using 60dB

templates:
- template_name: InputTemplate
  class_name: InputTemplate
  attributes: {}

- template_name: TextInput
  class_name: TextInput
  template_input: InputTemplate
  attributes:
    text: This is a test of the Sinapsis 60dB text-to-speech template.

- template_name: SixtyDBTTS
  class_name: SixtyDBTTS
  template_input: TextInput
  attributes:
    voice: null
    output_format: mp3

- template_name: AudioWriterSoundfile
  class_name: AudioWriterSoundfile
  template_input: SixtyDBTTS
  attributes:
    save_dir: "60db"
    extension: "wav"
```
</details>

> [!IMPORTANT]
> The TextInput template corresponds to [sinapsis-data-readers](https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_readers). If you want to use the example, please make sure you install the package.

To run the config, use the CLI:
```bash
sinapsis run name_of_config.yml
```

<h2 id="webapp">🌐 Webapp</h2>
The webapps included in this project showcase the modularity of the 60dB templates for speech generation tasks.

> [!IMPORTANT]
> To run the app you first need to clone this repository:

```bash
git clone git@github.com:Sinapsis-ai/sinapsis-speech.git
cd sinapsis-speech
```

> [!NOTE]
> If you'd like to enable external app sharing in Gradio, `export GRADIO_SHARE_APP=True`

> [!IMPORTANT]
> 60dB requires an API key to run any inference. Set your env var using <code>export SIXTYDB_API_KEY='your-api-key'</code>

<details>
<summary id="docker"><strong><span style="font-size: 1.4em;">🐳 Docker</span></strong></summary>

1. **Build the sinapsis-speech image**:
```bash
docker compose -f docker/compose.yaml build
```

2. **Start the app container**:
```bash
docker compose -f docker/compose_apps.yaml up -d sinapsis-60db
```
3. **Check the logs**
```bash
docker logs -f sinapsis-60db
```
4. **The logs will display the URL to access the webapp, e.g.,:**
```bash
Running on local URL:  http://127.0.0.1:7860
```
5. **To stop the app**:
```bash
docker compose -f docker/compose_apps.yaml down
```
</details>

<details>
<summary id="virtual-environment"><strong><span style="font-size: 1.4em;">💻 UV</span></strong></summary>

1. **Sync the virtual environment**:
```bash
uv sync --frozen
```
2. **Install the wheel**:
```bash
uv pip install sinapsis-speech[all] --extra-index-url https://pypi.sinapsis.tech
```
3. **Run the webapp** (TTS / streaming / websocket):
```bash
uv run webapps/generic_tts_apps/sixtydb_tts_app.py
uv run webapps/generic_tts_apps/sixtydb_tts_stream_app.py
uv run webapps/generic_tts_apps/sixtydb_tts_websocket_app.py
```
4. **The terminal will display the URL to access the webapp (e.g.)**:
```bash
Running on local URL:  http://127.0.0.1:7860
```
</details>

<h2 id="documentation">📙 Documentation</h2>

Documentation is available on the [sinapsis website](https://docs.sinapsis.tech/docs)

Tutorials for different projects within sinapsis are available at [sinapsis tutorials page](https://docs.sinapsis.tech/tutorials)

<h2 id="license">🔍 License</h2>

This project is licensed under the AGPLv3 license, which encourages open collaboration and sharing. For more details, please refer to the [LICENSE](LICENSE) file.

For commercial use, please refer to our [official Sinapsis website](https://sinapsis.tech) for information on obtaining a commercial license.
