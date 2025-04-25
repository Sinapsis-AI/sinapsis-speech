<h1 align="center">
<br>
<a href="https://sinapsis.tech/">
  <img
    src="https://github.com/Sinapsis-AI/brand-resources/blob/main/sinapsis_logo/4x/logo.png?raw=true"
    alt="" width="300">
</a><br>
Sinapsis Zonos
<br>
</h1>

<h4 align="center">Templates for advanced speech synthesis using Zonos</h4>

<p align="center">
<a href="#installation">🐍 Installation</a> •
<a href="#features"> 🚀 Features</a> •
<a href="#example"> 📚 Usage example</a> •
<a href="#webapp">🌐 Webapp</a> •
<a href="#documentation">📙 Documentation</a> •
<a href="#packages">🔍 License</a>
</p>

This **Sinapsis Zonos** package provides a single template for integrating, configuring, and running **text-to-speech (TTS)** and **voice cloning** functionalities powered by [Zonos](https://github.com/Zyphra/Zonos/tree/main). It supports multilingual speech, emotional modulation, and real-time audio generation.

<h2 id="installation">🐍 Installation</h2>


> [!IMPORTANT]
> Sinapsis project requires Python 3.10 or higher.
>

Install using your preferred package manager. We strongly recommend using <code>uv</code>. To install <code>uv</code>, refer to the [official documentation](https://docs.astral.sh/uv/getting-started/installation/#installation-methods).


Install with <code>uv</code>:
```bash
  uv pip install sinapsis-zonos --extra-index-url https://pypi.sinapsis.tech
```
Or with raw <code>pip</code>:
```bash
  pip install sinapsis-zonos --extra-index-url https://pypi.sinapsis.tech
```

> [!IMPORTANT]
> Templates in each package may require additional dependencies. For development, we recommend installing the package with all the optional dependencies:
>
With <code>uv</code>:

```bash
  uv pip install sinapsis-zonos[all] --extra-index-url https://pypi.sinapsis.tech
```
Or with raw <code>pip</code>:
```bash
  pip install sinapsis-zonos[all] --extra-index-url https://pypi.sinapsis.tech
```

> [!NOTE]
Zonos depends on the eSpeak library phonemization. The installation depends on your OS. For Linux:
```bash
apt install -y espeak-ng
```


<h2 id="features">🚀 Features</h2>

<h3>Templates Supported</h3>

- **ZonosTTS**: Template for converting text to speech or performing voice cloning based on the presence of an audio sample.​

    <details>
    <summary>Attributes</summary>

    - `cfg_scale`(Optional): Controls randomness and creativity in speech generation (default: `2.0`, range: 1.0–5.0). Higher values introduce more variation in speech output.
    - `denoised_speaker`(Optional): If True, applies denoising to the speaker embedding to reduce background noise (default: `False`).
    - `dnsmos`(Optional): Denoising strength for hybrid models (default: `4.0`, range: 1.0–5.0).
    - `emotions`(Optional): Emotion configuration to fine-tune the emotional tone of the generated speech (default: `{}`). Accepts an Emotions object with weights for various emotions.
    - `fmax`(Optional): Maximum frequency cutoff in Hz for audio generation (default: `22050`, range: 0–24000).
    - `language`(Optional): Language code used for synthesis (default: `en-us`)
    - `model`(Optional): The Zonos model identifier to use (default: `Zyphra/Zonos-v0.1-transformer`). Options: `Zyphra/Zonos-v0.1-transformer` and `Zyphra/Zonos-v0.1-hybrid`.
    - `output_folder`(Optional): The folder where generated audio files will be saved (default: `SINAPSIS_CACHE_DIR/elevenlabs/ audios`).
    - `pitch_std`(Optional): Standard deviation for pitch variation, which influences pitch naturalness (default: `20.0`, range: 0–300).
    - `prefix_audio`(Optional): Path to an audio file used for prefix conditioning (e.g., whispering or prosody control) (default: `None`).
    - `randomized_seed`(Optional): If True, a random seed is used for each generation (default: `True`).
    - `sampling_params`(Optional): Controls sampling behavior for speech synthesis. Accepts a SamplingParams object with fields like `top_p`, `top_k`, `min_p`, `linear`, `conf`, and `quad`.
    - `seed`(Optional): Random seed used for deterministic generation. If randomized_seed is False, this value ensures repeatable output (default: `420`).
    - `speaker_audio`(Optional): Path to a reference audio file used to extract speaker characteristics for voice cloning (default: `None`).
    - `speaking_rate`(Optional): Speaking rate in syllables per second (default: `15.0`, range: 5–30).
    - `unconditional_keys`(Optional): A set of keys (e.g., {`vqscore_8`, `dnsmos_ovrl`}) that disable speaker conditioning when generating speech.
    - `vq_score`(Optional): VQ score threshold used by hybrid models to determine decoding style (default: `0.7`, range: 0.5–0.8).

    </details>

> [!TIP]
> Use CLI command ```sinapsis info --example-template-config TEMPLATE_NAME``` to produce an example Agent config for the Template specified in ***TEMPLATE_NAME***.

For example, for ***ZonosTTS*** use ```sinapsis info --example-template-config ZonosTTS``` to produce an example config like:

<details>
<summary ><strong><span style="font-size: 1.0em;">Config</span></strong></summary>

```yaml
agent:
  name: my_test_agent
templates:
- template_name: InputTemplate
  class_name: InputTemplate
  attributes: {}
- template_name: ZonosTTS
  class_name: ZonosTTS
  template_input: InputTemplate
  attributes:
    cfg_scale: 2.0
    denoised_speaker: false
    dnsmos: 4.0
    emotions:
      happiness: 0
      sadness: 0
      disgust: 0
      fear: 0
      surprise: 0
      anger: 0
      other: 0
      neutral: 0
    fmax: 22050.0
    language: en-us
    model: Zyphra/Zonos-v0.1-transformer
    output_folder: ~/.cache/sinapsis/zonos/audios
    pitch_std: 20.0
    prefix_audio: null
    randomized_seed: true
    sampling_params:
      min_p: 0.0
      top_k: 0
      top_p: 0.0
      linear: 0.0
      conf: 0.0
      quad: 0.0
    seed: 420
    speaker_audio: null
    speaking_rate: 15.0
    unconditional_keys: !!set
      dnsmos_ovrl: null
      vqscore_8: null
    vq_score: 0.7
```
</details>

<h2 id='example'>📚 Usage example</h2>

This example shows how to use the **ZonosTTS** template to convert text into speech. The generated audio is based on the input text and is saved locally as a file.

<details>
<summary ><strong><span style="font-size: 1.4em;">Config</span></strong></summary>

```yaml
agent:
  name: text_to_speech
  description: text to speech agent using Zonos

templates:

- template_name: InputTemplate
  class_name: InputTemplate
  attributes: {}

- template_name: TextInput
  class_name: TextInput
  template_input: InputTemplate
  attributes:
    text:  This is a test of Sinapsis Zonos text-to-speech template.

- template_name: ZonosTTS
  class_name: ZonosTTS
  template_input: TextInput
  attributes:
    model: Zyphra/Zonos-v0.1-transformer
    language: en-us
    emotions:
      happiness: 0.3077
      sadness: 0.0256
      disgust: 0.0256
      fear: 0.0256
      surprise: 0.0256
      anger: 0.0256
      other: 0.2564
      neutral: 0.3077
    fmax: 24000
    pitch_std: 45.0
    speaking_rate: 15.0
    cfg_scale: 2.0
    sampling_params:
      linear: 0.5
      conf: 0.4
      quad: 0
    randomized_seed: True
    denoised_speaker: False
    unconditional_keys:
      - dnsmos_ovrl
      - vqscore_8

```
</details>

This configuration defines an **agent** and a sequence of **templates** for speech synthesis, using Zonos.

> [!IMPORTANT]
> The TextInput template correspond to [sinapsis-data-readers](https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_readers). If you want to use the example, please make sure you install the package.
>

To run the config, use the CLI:
```bash
sinapsis run name_of_config.yml
```

<h2 id="webapp">🌐 Webapp</h2>
The webapps included in this project showcase the modularity of the templates, in this case for speech generation tasks.

> [!IMPORTANT]
> To run the app you first need to clone this repository:

```bash
git clone git@github.com:Sinapsis-ai/sinapsis-speech.git
cd sinapsis-speech
```

> [!NOTE]
> If you'd like to enable external app sharing in Gradio, `export GRADIO_SHARE_APP=True`


<details>
<summary id="docker"><strong><span style="font-size: 1.4em;">🐳 Build with Docker</span></strong></summary>

**IMPORTANT**: This Docker image depends on the `sinapsis-nvidia:base` image. For detailed instructions, please refer to the [Sinapsis README](https://github.com/Sinapsis-ai/sinapsis?tab=readme-ov-file#docker).


1. **Build the Docker image**:
```bash
docker compose -f docker/compose.yaml build
```

2. **Start the app container**:
```bash
docker compose -f docker/compose_apps.yaml up -d sinapsis-zonos
```
3. **Check the logs**
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



