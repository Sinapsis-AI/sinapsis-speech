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

<h4 align="center"> Sinapsis package with a suite of templates and utilities for seamlessly integrating, configuring, and running functionalities powered by ElevenLabs </h4>

<p align="center">
<a href="#installation">🐍 Installation</a> •
<a href="#packages">📦 Features</a> •
<a href="#webapp">🌐 Webapp</a> •
<a href="#documentation">📙 Documentation</a> •
<a href="#packages">🔍 License</a>
</p>


<h2 id="installation">🐍 Installation</h2>


> [!IMPORTANT]
> Sinapsis project requires Python 3.10 or higher.
>

We strongly encourage the use of <code>uv</code>, although any other package manager should work too.
If you need to install <code>uv</code> please see the [official documentation](https://docs.astral.sh/uv/getting-started/installation/#installation-methods).


1. Install using your favourite package manager.

Example with <code>uv</code>:
```bash
  uv pip install sinapsis-elevenlabs --extra-index-url https://pypi.sinapsis.tech
```
 or with raw <code>pip</code>:
```bash
  pip install sinapsis-elevenlabs --extra-index-url https://pypi.sinapsis.tech
```
**Change the name of the package for the one you want to install**.

> [!TIP]
> You can also install all the packages within this project:
>
```bash
  uv pip install sinapsis-speech[all] --extra-index-url https://pypi.sinapsis.tech
```

<h2 id="packages">📦 Features</h2>

This package provides a suite of templates and utilities for seamlessly integrating, configuring, and running **text-to-speech (TTS)** and **voice generation** functionalities powered by [ElevenLabs](https://elevenlabs.io/):

- **Text-to-speech**: Template for converting text into speech using ElevenLabs' voice models.

- **Voice generation**: Template for generating custom synthetic voices based on user-provided descriptions.

<h2 id="webapps">🌐 Webapps</h2>
The webapps included in this project showcase the modularity of the templates, in this case
for speech generation tasks.

> [!IMPORTANT]
> To run the app you first need to clone this repository:

```bash
git clone git@github.com:Sinapsis-ai/sinapsis-speech.git
cd sinapsis-speech
```

> [!NOTE]
> If you'd like to enable external app sharing in Gradio, `export GRADIO_SHARE_APP=True`

> [!IMPORTANT]
> Elevenlabs requires an api key to run any inference. Please go to the [official website](https://elevenlabs.io), create an account.
If you already have an account, go to the [token page](https://elevenlabs.io/app/settings/api-keys) and generate a token.

> [!IMPORTANT]
> set your env var using <code> export ELEVENLABS_API_KEY='your-api-key'</code>

<details>
<summary id="docker"><strong><span style="font-size: 1.4em;">🐳 Build with Docker</span></strong></summary>

1. **Build the Docker image**:
```bash
docker compose -f docker/compose.yaml build
```

2. **Launch the service**:
```bash
docker compose -f docker/compose_apps.yaml up -d sinapsis-elevenlabs
```
2. **Check the logs**
```bash
docker logs -f sinapsis-elevenlabs
```
3. **The logs will display the URL to access the webapp, e.g.,:**:
```bash
Running on local URL:  http://127.0.0.1:7860
```
4. To stop the app:
```bash
docker compose -f docker/compose_apps.yaml down sinapsis-elevenlabs
```
</details>

<details>
<summary id="virtual-environment"><strong><span style="font-size: 1.4em;">💻 UV</span></strong></summary>

1. **Sync the virtual environment**:

```bash
uv sync --frozen
```
2. Install the wheel:

```bash
uv pip install sinapsis-speech[all] --extra-index-url https://pypi.sinapsis.tech
```
3. **Activate the virtual environment**:

```bash
source .venv/bin/activate
```
4. **Launch the demo**:

```bash
python webapps/elevenlabs/elevenlabs_tts_app.py
```
4. Open the displayed URL, e.g.:
```bash
Running on local URL:  http://127.0.0.1:7860
```
**NOTE**: The URL can be different, please make sure you check the logs.

</details>



<h2 id="documentation">📙 Documentation</h2>

Documentation is available on the [sinapsis website](https://docs.sinapsis.tech/docs)

Tutorials for different projects within sinapsis are available at [sinapsis tutorials page](https://docs.sinapsis.tech/tutorials)

<h2 id="license">🔍 License</h2>

This project is licensed under the AGPLv3 license, which encourages open collaboration and sharing. For more details, please refer to the [LICENSE](LICENSE) file.

For commercial use, please refer to our [official Sinapsis website](https://sinapsis.tech) for information on obtaining a commercial license.



