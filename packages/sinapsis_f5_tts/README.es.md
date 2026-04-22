<h1 align="center"><br/><a href="https://sinapsis.tech/"><img alt="" src="https://github.com/Sinapsis-AI/brand-resources/blob/main/sinapsis_logo/4x/logo.png?raw=true" width="300"/></a><br/>Sinapsis F5-TTS
<br/></h1>
<h4 align="center">Plantillas para la generación avanzada de texto a palabra con F5-TTS</h4>
<p align="center"><a href="#installation">🐍 Instalación</a> •
<a href="#features"> 🚀 Características</a> •
<a href="#example"> 📚 Ejemplo de uso</a> •
<a href="#webapp">🌐 Aplicación web</a> •
<a href="#documentation">📙 Documentación</a> •
<a href="#packages">🔍 Licencia</a>


Esto <strong>Sinapsis F5-TTS</strong> paquete proporciona una plantilla para integrar, configurar y ejecutar sin problemas <strong>texto a palabra (TTS)</strong> funcionalidades alimentadas por <a href="https://github.com/SWivid/F5-TTS">F5TTS</a>.

<h2 id="installation">🐍 Instalación</h2>

Instala usando tu administrador de paquetes favorito. Alentamos firmemente el uso de <code>uv</code>, aunque cualquier otro administrador de paquetes debe trabajar también.
Si necesita instalar <code>uv</code> Por favor, veamos <a href="https://docs.astral.sh/uv/getting-started/installation/#installation-methods">documentación oficial</a>.


Ejemplo con <code>uv</code>:



```bash
  uv pip install sinapsis-f5-tts --extra-index-url https://pypi.sinapsis.tech
```

o con solo <code>pip</code>:

```bash
  pip install sinapsis-f5-tts --extra-index-url https://pypi.sinapsis.tech
```

<blockquote>

[!IMPORTANT]
Las plantillas en cada paquete pueden requerir dependencias adicionales. Para el desarrollo, recomendamos instalar el paquete con todas las dependencias opcionales:

con <code>uv</code>:

</blockquote>

```bash
  uv pip install sinapsis-f5-tts[all] --extra-index-url https://pypi.sinapsis.tech
```

o con solo <code>pip</code>:

```bash
  pip install sinapsis-f5-tts[all] --extra-index-url https://pypi.sinapsis.tech
```
<h2 id="features">🚀 Características
</h2><h3>Plantillas soportadas</h3>
Este módulo incluye una plantilla para síntesis de texto a palabra utilizando el modelo F5TTS:

<strong>F5TTSInference</strong>: Convierte texto al discurso usando el modelo F5TTS con capacidades de clonación de voz. La plantilla procesa paquetes de texto del contenedor de entrada, genera el audio correspondiente mediante F5TTS y añade los paquetes de audio resultantes al contenedor.


<details><summary>Atributos</summary>
</details>

<ul>
<li><code>model</code>: Nombre modelo para usar para inferencia (por defecto: "F5TTS<em>v1</em>Base")</li>

<li><code>model_cfg</code>: Vía opcional al archivo de configuración modelo</li>

<li><code>ckpt_file</code>: Vía opcional para modelar el archivo de control</li>

<li><code>vocab_file</code>: Vía opcional al archivo de vocabulario</li>

<li><code>ref_audio</code>: Path to reference audio file for voice cloning (default: "artifacts/town.mp3")</li>

<li><code>ref_text</code>: Texto de referencia correspondiente al audio de referencia (por defecto: cadena vacía)</li>

<li><code>vocoder_name</code>: Vocoder a utilizar para la generación de ondas, ya sea "vocos" o "bigvgan" (por defecto: "vocos")</li>

<li><code>load_vocoder_from_local</code>: Ya sea para cargar el vocoder del camino local (por defecto: Falso)</li>

<li><code>nfe_step</code>: Número de pasos de evaluación de funciones para la difusión, valores más altos dan mejor calidad pero menor inferencia (por defecto: 32)</li>

<li><code>cfg_strength</code>: Fortaleza de guía sin clasificar, los valores más altos dan una salida más estable pero menos expresividad (por defecto: 2.0)</li>

<li><code>cross_fade_duration</code>: Duración del enfrentamiento entre segmentos de audio en segundos (predeterminado: 0.15)</li>

<li>¨C21C: Factor de velocidad para el discurso generado, valores 1 hacer el discurso más rápido, &lt; 1 hacer más lento (por defecto: 1.0)</li>

<li>¨C22C: Coeficiente para muestreo (por defecto: -1.0)</li>

<li>¨C23C: Objetivo RMS valor para la normalización de audio (por defecto: ninguno)</li>

<li>¨C24C: Duración fija para el audio generado en segundos (por defecto: ninguno)</li>

<li>¨C25C: Ya sea para eliminar el silencio del audio generado (por defecto: falso)</li>

<li>¨C26C: Ya sea para guardar trozos de audio individuales (por defecto: falso)</li>

<li>¨C27C: Dispositivo de uso para inferencia, por ejemplo, "cuda", "cpu" (por defecto: ninguno, auto-detecto)
</li>
</ul>
<blockquote>

[! TIP]
Usa el comando de CLI <code>sinapsis info --example-template-config TEMPLATE_NAME</code> para producir un ejemplo Agente config para la Plantilla especificado en <strong><em>TEMPLATE_NAME</em></strong>.

</blockquote>

Por ejemplo, para <strong><em>F5TTSInference</em></strong> usa <code>sinapsis info --example-template-config RFDETRTrain</code> para producir un config de ejemplo como:

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
<h2 id="example">📚 Ejemplo de uso</h2>
Este ejemplo ilustra cómo utilizar el <strong>F5TTSInference</strong> plantilla para síntesis de texto a palabra. Convierte la entrada de texto en el discurso usando F5-TTS y guarda el archivo de audio resultante localmente.


<details><summary><strong><span style="font-size: 1.4em;">Config</span></strong></summary>
</details>


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



Esta configuración define un <strong>Agente</strong> y una secuencia de <strong>plantillas</strong> para la conversión de texto al habla <strong>F5-TTS</strong>.

<blockquote>

[!IMPORTANT]
El TextInput y AudioWriterSoundfile corresponden a <a href="https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_readers">sinapsis-data-readers</a> y <a href="https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_writers">sinapsis-data-writers</a>. Si desea utilizar el ejemplo, asegúrese de instalar los paquetes.

</blockquote>

Para ejecutar la configuración, utilice el CLI:

```bash
sinapsis run name_of_config.yml
```
<h2 id="webapp">🌐 Aplicación web</h2>
La aplicación web incluida en este proyecto muestra la modularidad de la plantilla F5TTS para tareas de generación de discursos.

<blockquote>

[!IMPORTANT]
Para ejecutar la aplicación primero necesitas clonar este repositorio:

</blockquote>

```bash
git clone git@github.com:Sinapsis-ai/sinapsis-speech.git
cd sinapsis-speech
```

<blockquote>

[!NOTE]
Si desea habilitar el intercambio de aplicaciones externas en Gradio, <code>export GRADIO_SHARE_APP=True</code>

[!IMPORTANT]
F5TTS requiere un archivo de audio de referencia para la clonación de voz. Asegúrese de tener un archivo de audio de referencia en el directorio de artefactos.

</blockquote>


<details><summary id="docker"><strong><span style="font-size: 1.4em;">🐳 Docker</span></strong></summary>
</details>


<strong>IMPORTANTE</strong> Esta imagen del docker depende de la sinapsis-nvidia: imagen básica. Por favor consulta el sitio web oficial de  <a href="https://github.com/Sinapsis-ai/sinapsis?tab=readme-ov-file#docker">sinapsis</a> para instrucciones sobre construir con Docker.
<ol>
<li><strong>Construir la imagen de sinapsis-habla</strong>:</li>
</ol>

```bash
docker compose -f docker/compose.yaml build
```
<ol start="2">
<li><strong>Iniciar el contenedor de aplicaciones</strong>:</li>
</ol>

```bash
docker compose -f docker/compose_apps.yaml up -d sinapsis-f5tts
```
<ol start="3">
<li><strong>Compruebe los registros</strong></li>
</ol>

```bash
docker logs -f sinapsis-f5tts
```
<ol start="4">
<li><strong>Los registros mostrarán la URL para acceder a la aplicación web, por ejemplo:</strong>:</li>
</ol>

```bash
Running on local URL:  http://127.0.0.1:7860
```

<strong>NOTA</strong>: La url puede ser diferente, comprobar la salida de los registros.
<ol start="5">
<li><strong>Para detener la aplicación</strong>:</li>
</ol>

```bash
docker compose -f docker/compose_apps.yaml down
```




<details><summary id="virtual-environment"><strong><span style="font-size: 1.4em;">💻 UV</span></strong></summary>
</details>


Para ejecutar la aplicación web utilizando <code>uv</code> gestor de paquetes, siga estos pasos:
<ol>
<li><strong>Sincronizar el entorno virtual</strong>:</li>
</ol>

```bash
uv sync --frozen
```
<ol start="2">
<li><strong>Instalar la rueda</strong>:</li>
</ol>

```bash
uv pip install sinapsis-speech[all] --extra-index-url https://pypi.sinapsis.tech
```
<ol start="3">
<li><strong>Ejecute la aplicación web</strong>:</li>
</ol>

```bash
uv run webapps/packet_tts_apps/f5_tts_app.py
```
<ol start="4">
<li><strong>El terminal mostrará la URL para acceder a la aplicación web (por ejemplo)</strong>:</li>
</ol>

```bash
Running on local URL:  http://127.0.0.1:7860
```

<strong>NOTA</strong>: La URL puede variar; comprueba la salida de la terminal para la dirección correcta.


<h2 id="documentation">📙 Documentación</h2>
La documentación está disponible <a href="https://docs.sinapsis.tech/docs">web de sinapsis</a>

Los tutoriales para diferentes proyectos dentro de sinapsis están disponibles en <a href="https://docs.sinapsis.tech/tutorials">sinapsis tutoriales página</a>
<h2 id="license">🔍 Licencia</h2>
Este proyecto está licenciado bajo la licencia AGPLv3, que fomenta la colaboración abierta y el intercambio. Para más detalles, consulta el archivo <a href="LICENSE">LICENSE</a>.

Para uso comercial, consulta el  <a href="https://sinapsis.tech"> sitio web oficial de Sinapsis</a> para información sobre la obtención de una licencia comercial.

