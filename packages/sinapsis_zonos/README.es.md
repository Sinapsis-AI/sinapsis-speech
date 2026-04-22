<h1 align="center"><br/><a href="https://sinapsis.tech/"><img alt="" src="https://github.com/Sinapsis-AI/brand-resources/blob/main/sinapsis_logo/4x/logo.png?raw=true" width="300"/></a><br/>Sinapsis Zonos
<br/></h1>
<h4 align="center">Plantillas para la conversión de habla avanzada utilizando Zonos</h4>
<p align="center"><a href="#installation">🐍 Instalación</a> •
<a href="#features"> 🚀 Características</a> •
<a href="#example"> 📚 Ejemplo de uso</a> •
<a href="#webapp">🌐 Aplicación web</a> •
<a href="#documentation">📙 Documentación</a> •
<a href="#packages">🔍 Licencia</a>


<strong>Sinapsis Zonos</strong> proporciona una sola plantilla para integrar, configurar y ejecutar <strong>texto a palabra (TTS)</strong> y <strong>clonación de voz</strong> funcionalidades alimentadas por <a href="https://github.com/Zyphra/Zonos/tree/main">Zonos</a>. Soporta discurso multilingüe, modulación emocional y generación de audio en tiempo real.

<h2 id="installation">🐍 Instalación</h2>

<blockquote>

[!IMPORTANT]
El proyecto Sinapsis requiere Python 3.10 o superior.

</blockquote>


Instalar usando el administrador de paquetes preferido. Recomendamos fuertemente el uso <code>uv</code>. Para instalar <code>uv</code>, consulta el <a href="https://docs.astral.sh/uv/getting-started/installation/#installation-methods">documentación oficial</a>.


Instalar con <code>uv</code>:



```bash
  uv pip install sinapsis-zonos --extra-index-url https://pypi.sinapsis.tech
```

O con solo <code>pip</code>:

```bash
  pip install sinapsis-zonos --extra-index-url https://pypi.sinapsis.tech
```

<blockquote>

[!IMPORTANT]
Las plantillas en cada paquete pueden requerir dependencias adicionales. Para el desarrollo, recomendamos instalar el paquete con todas las dependencias opcionales:

Con <code>uv</code>:

</blockquote>

```bash
  uv pip install sinapsis-zonos[all] --extra-index-url https://pypi.sinapsis.tech
```

O con solo <code>pip</code>:

```bash
  pip install sinapsis-zonos[all] --extra-index-url https://pypi.sinapsis.tech
```

<blockquote>

[!NOTE]
Zonos depende de la fonización de la biblioteca eSpeak. La instalación depende de su sistema operativo. Para Linux:

</blockquote>

```bash
apt install -y espeak-ng
```
<h2 id="features">🚀 Características</h2><h3>Plantillas soportadas</h3><ul>
<li>
<strong>ZonosTTS</strong>: Plantilla para la conversión de texto al lenguaje o la clonación de voz basada en la presencia de una muestra de audio.


<details><summary>Atributos</summary>
</details>

<ul>
<li><code>cfg_scale</code>(Opcional): Controla la aleatoriedad y la creatividad en la generación del habla (por defecto: <code>2.0</code>, rango: 1.0–5.0). Valores más altos introducen más variación en la salida del habla.</li>

<li><code>denoised_speaker</code>(Opcional): Si es cierto, se aplica la denuncia al altavoz que incrusta para reducir el ruido de fondo (por defecto: <code>False</code>).</li>

<li><code>dnsmos</code>(Opcional): Denoizing strength for Hybrid models (default: <code>4.0</code>, rango: 1.0–5.0).</li>

<li><code>emotions</code>(Opcional): Configuración de emociones para ajustar el tono emocional del discurso generado (por defecto: <code>{}</code>). Acepta un objeto Emociones con pesos para varias emociones.</li>

<li><code>fmax</code>(Opcional): Corte de frecuencia máxima en Hz para la generación de audio (por defecto: <code>22050</code>, rango: 0–24000).</li>

<li><code>language</code>(Opcional): Código de idioma utilizado para la síntesis (predeterminado: ¨C22C)</li>

<li>¨C23C(Opcional): El identificador modelo Zonos para usar (por defecto: ¨C24C). Opciones: ¨C25C y ¨C26C.</li>

<li>¨C27C(Opcional): La carpeta donde se guardarán los archivos de audio generados (por defecto: ¨C28C).</li>

<li>¨C29C(Opcional): Desviación estándar para la variación del campo, que influye en la naturalidad del campo (por defecto: ¨C30C, rango: 0–300).</li>

<li>¨C31C(Opcional): Path to an audio file used for prefix condition (e.g., susurring or prosody control) (default: ¨C32C).</li>

<li>¨C33C(Opcional): Si es verdadero, se utiliza una semilla aleatoria para cada generación (por defecto: ¨C34C).</li>

<li>¨C35C(Opcional): Controla el comportamiento de muestreo para la síntesis del habla. Acepta un objeto SamplingParams con campos como ¨C36C, ¨C37C, ¨C38C, ¨C39C, ¨C40C, y ¨C41C.</li>

<li>¨C42C(Opcional): Semilla aleatoria utilizada para la generación determinista. Si randomized<em>seed es False, este valor asegura la salida repetible (por defecto: ¨C43C).</li>

<li>¨C44C(Opcional): Camino a un archivo de audio de referencia utilizado para extraer características de altavoz para la clonación de voz (por defecto: ¨C45C).</li>

<li>¨C46C(Opcional): Tasa de habla en sílabas por segundo (por defecto: ¨C47C, rango: 5–30).</li>

<li>¨C48C(Opcional): Un conjunto de llaves (por ejemplo, {¨C49C, ¨C50C}) ese altavoz deshabilitado acondicionamiento al generar discurso.</li>

<li>¨C51C(Opcional): umbral de puntuación VQ utilizado por modelos híbridos para determinar el estilo de decodificación (por defecto: ¨C52C, rango: 0,5-0.8).</li>
</ul>

</li>
</ul>
<blockquote>

[! TIP]
Usa el comando de CLI <code>sinapsis info --example-template-config TEMPLATE_NAME</code> para producir un ejemplo Agente config para la Plantilla especificado en <strong><em>TEMPLATE</em>NAME</em></strong>.

</blockquote>

Por ejemplo, para <strong><em>ZonosTTS</em></strong> usa <code>sinapsis info --example-template-config ZonosTTS</code> para producir un config de ejemplo como:


<details><summary><strong><span style="font-size: 1.0em;">Config</span></strong></summary>
</details>


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


<h2 id="example">📚 Ejemplo de uso</h2>
Este ejemplo muestra cómo utilizar el <strong>ZonosTTS</strong> plantilla para convertir texto en discurso. El audio generado se basa en el texto de entrada y se guarda localmente como un archivo.


<details><summary><strong><span style="font-size: 1.4em;">Config</span></strong></summary>
</details>


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



Esta configuración define un <strong>Agente</strong> y una secuencia de <strong>plantillas</strong> para la síntesis del discurso, usando Zonos.

<blockquote>

[!IMPORTANT]
La plantilla TextInput corresponde a <a href="https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_readers">sinapsis-data-readers</a>. Si desea utilizar el ejemplo, asegúrese de instalar el paquete.

</blockquote>

Para ejecutar la configuración, utilice el CLI:

```bash
sinapsis run name_of_config.yml
```
<h2 id="webapp">🌐 Aplicación web</h2>
Las aplicaciones web incluidas en este proyecto muestran la modularidad de las plantillas, en este caso para tareas de generación de discursos.

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

</blockquote>


<details><summary id="docker"><strong><span style="font-size: 1.4em;">Construir con Docker</span></strong></summary>
</details>


<strong>IMPORTANTE</strong>: Esta imagen Docker depende de <code>sinapsis-nvidia:base</code> imagen. Para instrucciones detalladas, consulta el <a href="https://github.com/Sinapsis-ai/sinapsis?tab=readme-ov-file#docker">Sinapsis README</a>.
<ol>
<li><strong>Construir la imagen Docker</strong>:</li>
</ol>

```bash
docker compose -f docker/compose.yaml build
```
<ol start="2">
<li><strong>Iniciar el contenedor de aplicaciones</strong>:</li>
</ol>

```bash
docker compose -f docker/compose_apps.yaml up -d sinapsis-zonos
```
<ol start="3">
<li><strong>Compruebe los registros</strong></li>
</ol>

```bash
docker logs -f sinapsis-zonos
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
uv run webapps/generic_tts_apps/zonos_tts_app.py
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

