<h1 align="center">
<br>
<a href="https://sinapsis.tech/">
  <img
    src="https://github.com/Sinapsis-AI/brand-resources/blob/main/sinapsis_logo/4x/logo.png?raw=true"
    alt="" width="300">
</a><br>
Sinapsis Elevenlabs
<br>
</h1>

<h4 align="center">Templates for advanced speech generation with Elevenlabs</h4>

<p align="center">
<a href="#installation">🐍 Installation</a> •
<a href="#features"> 🚀 Features</a> •
<a href="#example"> 📚 Usage example</a> •
<a href="#webapp">🌐 Webapp</a> •
<a href="#documentation">📙 Documentation</a> •
<a href="#packages">🔍 License</a>
</p>

This **Sinapsis Elevenlabs** package offers a suite of templates and utilities designed for effortless integrating, configuration, and execution of **text-to-speech (TTS)** and **voice generation** functionalities powered by [ElevenLabs](https://elevenlabs.io/).


<h2 id="installation">🐍 Installation</h2>


> [!IMPORTANT]
> Sinapsis project requires Python 3.10 or higher.
>

Install using your preferred package manager. We strongly recommend using <code>uv</code>. To install <code>uv</code>, refer to the [official documentation](https://docs.astral.sh/uv/getting-started/installation/#installation-methods).


Install with <code>uv</code>:
```bash
  uv pip install sinapsis-elevenlabs --extra-index-url https://pypi.sinapsis.tech
```

Or with raw <code>pip</code>:
```bash
  pip install sinapsis-elevenlabs --extra-index-url https://pypi.sinapsis.tech
```

> [!IMPORTANT]
> Templates in each package may require additional dependencies. For development, we recommend installing the package with all the optional dependencies:
>

With <code>uv</code>:
```bash
  uv pip install sinapsis-elevenlabs[all] --extra-index-url https://pypi.sinapsis.tech
```
Or with raw <code>pip</code>:
```bash
  pip install sinapsis-elevenlabs[all] --extra-index-url https://pypi.sinapsis.tech
```

<h2 id="features">🚀 Features</h2>

<h3>Templates Supported</h3>

- **ElevenLabsTTS**: Template for converting text into speech using ElevenLabs' voice models.

    <details>
    <summary>Attributes</summary>

    - `api_key`(Optional): The API key used to authenticate with ElevenLabs' API. Although this parameter is    optional in the function signature, **the API key must be provided** either through this argument or the `ELEVENLABS_API_KEY` environmental variable. If neither is provided, an error will be logged, and no speech    will be generated.
    - `model`(Optional): The model identifier to use for speech synthesis (default: `eleven_turbo_v2_5eleven_turbo_v2_5`). Options: `eleven_turbo_v2_5`, `eleven_multilingual_v2`, `eleven_turbo_v2`, `eleven_monolingual_v1`, `eleven_multilingual_v1`.
    - `output_format`(Optional): The output audio format and quality (default: `mp3_44100_128`). Options: `mp3_22050_32`, `mp3_44100_32`, `mp3_44100_64`, `mp3_44100_96`, `mp3_44100_128`, `mp3_44100_192`, `pcm_16000`, `pcm_22050`, `pcm_24000`, `pcm_44100`, `ulaw_8000`.
    - `output_folder`(Optional): The folder where generated audio files will be saved (default: `SINAPSIS_CACHE_DIR/elevenlabs/ audios`).
    - `stream`(Optional): If True, the audio is returned as a stream; otherwise, saved to a file (default: `False`).
    - `voice`(Optional): Voice for speech synthesis. Can be a voice ID (str), name (str), or ElevenLabs voice object (Voice) (default: None).
    - `voice_settings`(Optional):Dictionary of voice control settings:
        - `stability`: Controls voice randomness and emotional range (range: 0.0 to 1.0).
        - `similarity_boost`: Adjusts how closely the voice matches the original (range: 0.0 to 1.0).
        - `style`: Amplifies the speaker’s style, consuming more resources (range: 0.0 to 1.0).
        - `use_speaker_boost`: Increases similarity to the speaker with higher computational cost (boolean: `True` or `False`).
        - `speed`: Adjusts speech speed (range: 0.7 to 1.2, default: 1.0).
    </details>

- **ElevenLabsVoiceGeneration**: Template for generating custom synthetic voices based on user-provided descriptions.

    <details>
    <summary>Attributes</summary>

    - `api_key`(Optional): The API key used to authenticate with ElevenLabs' API. Although this parameter is    optional in the function signature, **the API key must be provided** either through this argument or the    `ELEVENLABS_API_KEY` environmental variable. If neither is provided, an error will be logged, and no speech    will be generated.
    - `model`(Optional): The model identifier to use for speech synthesis (default:     `eleven_turbo_v2_5eleven_turbo_v2_5`). Options: `eleven_turbo_v2_5`, `eleven_multilingual_v2`,    `eleven_turbo_v2`, `eleven_monolingual_v1`, `eleven_multilingual_v1`.
    - `output_format`(Optional): The output audio format and quality (default: `mp3_44100_128`). Options:     `mp3_22050_32`, `mp3_44100_32`, `mp3_44100_64`, `mp3_44100_96`, `mp3_44100_128`, `mp3_44100_192`,     `pcm_16000`, `pcm_22050`, `pcm_24000`, `pcm_44100`, `ulaw_8000`.
    - `output_folder`(Optional): The folder where generated audio files will be saved (default:     `SINAPSIS_CACHE_DIR/elevenlabs/ audios`).
    - `stream`(Optional): If True, the audio is returned as a stream; otherwise, saved to a file (default:    `False`).
    - `voice`(Optional): Voice for speech synthesis. Can be a voice ID (str), name (str), or ElevenLabs voice object (Voice) (default: None).
    - `voice_description`(Required): A description of the voice to be used for synthesis. This field is mandatory and helps to define the voice's characteristics or style.
    - `voice_settings`(Optional):Dictionary of voice control settings:
        - `stability`: Controls voice randomness and emotional range (range: 0.0 to 1.0).
        - `similarity_boost`: Adjusts how closely the voice matches the original (range: 0.0 to 1.0).
        - `style`: Amplifies the speaker’s style, consuming more resources (range: 0.0 to 1.0).
        - `use_speaker_boost`: Increases similarity to the speaker with higher computational cost (boolean:     `True` or `False`).
        - `speed`: Adjusts speech speed (range: 0.7 to 1.2, default: 1.0).
    </details>

> [!TIP]
> Use CLI command ```sinapsis info --example-template-config TEMPLATE_NAME``` to produce an example Agent config for the Template specified in ***TEMPLATE_NAME***.

For example, for ***ElevenLabsTTS*** use ```sinapsis info --example-template-config ElevenLabsTTS``` to produce an example config like:

```yaml
agent:
  name: my_test_agent
templates:
- template_name: InputTemplate
  class_name: InputTemplate
  attributes: {}
- template_name: ElevenLabsTTS
  class_name: ElevenLabsTTS
  template_input: InputTemplate
  attributes:
    api_key: null
    voice: null
    voice_settings:
      stability: null
      similarity_boost: null
      style: null
      use_speaker_boost: null
      speed: null
    model: eleven_turbo_v2_5
    output_format: mp3_44100_128
    output_folder: ~/.cache/sinapsis/elevenlabs/audios
    stream: false
```

<h2 id='example'>📚 Usage example</h2>

This example shows how to use the **ElevenLabsVoiceGeneration** template to convert text into speech. It generates speech based on a voice created from the user's description and saves the resulting audio file locally.

<details>
<summary ><strong><span style="font-size: 1.4em;">Config</span></strong></summary>

```yaml
agent:
  name: voice_creation
  description: voice generation agent using Elevenlabs

templates:
- template_name: InputTemplate
  class_name: InputTemplate
  attributes: {}

- template_name: TextInput
  class_name: TextInput
  template_input: InputTemplate
  attributes:
    text: En la oscuridad de la noche, se escuchaban los llantos lejanos de una mujer. Nadie sabía exactamente de dónde venían, pero todos los habitantes del pueblo aseguraban que era el llanto de La Llorona. Se decía que era el espíritu de una mujer que, en vida, había perdido a sus hijos y que, condenada por su dolor y su culpa, deambulaba por las orillas de los ríos buscando a sus pequeños. Nadie se atrevía a acercarse al agua cuando oían su llanto, pues sabían que, si la escuchabas cerca, su destino también estaba sellado...

- template_name: ElevenLabsVoiceGeneration
  class_name: ElevenLabsVoiceGeneration
  template_input: TextInput
  attributes:
    voice_description: A warm and engaging Mexican Spanish female voice, perfect for storytelling, audiobooks, and podcasts. Clear and expressive, with a natural, captivating tone, ideal for social media, YouTube, TikTok, and more.

```
</details>

This configuration defines an **agent** and a sequence of **templates** for speech synthesis, using a custom voice created through **ElevenLabs**.

> [!IMPORTANT]
> The TextInput template correspond to [sinapsis-data-readers](https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_readers). If you want to use the example, please make sure you install the package.
>

To run the config, use the CLI:
```bash
sinapsis run name_of_config.yml
```

<h2 id="webapp">🌐 Webapp</h2>
The webapps included in this project showcase the modularity of the ElevenLabs templates, in this case for speech generation tasks.

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

<details>
<summary id="docker"><strong><span style="font-size: 1.4em;">🐳 Docker</span></strong></summary>

**IMPORTANT** This docker image depends on the sinapsis-nvidia:base image. Please refer to the official [sinapsis](https://github.com/Sinapsis-ai/sinapsis?tab=readme-ov-file#docker) instructions to Build with Docker.


1. **Build the sinapsis-speech image**:
```bash
docker compose -f docker/compose.yaml build
```

2. **Start the app container**:
```bash
docker compose -f docker/compose_apps.yaml up -d sinapsis-elevenlabs
```
3. **Check the logs**
```bash
docker logs -f sinapsis-elevenlabs
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
uv run webapps/generic_tts_apps/elevenlabs_tts_app.py
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



