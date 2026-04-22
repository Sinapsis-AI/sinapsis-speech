<h1 align="center"><br/><a href="https://sinapsis.tech/"><img alt="" src="https://github.com/Sinapsis-AI/brand-resources/blob/main/sinapsis_logo/4x/logo.png?raw=true" width="300"/></a><br/>Sinapsis Kokoro
<br/></h1>
<h4 align="center">Plantillas para la generación avanzada de texto a palabra utilizando el modelo Kokoro 82M v1.0</h4>
<p align="center"><a href="#installation">🐍 Instalación</a> •
<a href="#features"> 🚀 Características</a> •
<a href="#example"> 📚 Ejemplo de uso</a> •
<a href="#webapp">🌐 Aplicación web</a> •
<a href="#documentation">📙 Documentación</a> •
<a href="#packages">🔍 Licencia</a>


Esto <strong>Sinapsis Kokoro</strong> paquete proporciona una sola plantilla para integrar, configurar y ejecutar funcionalidades <strong>texto a palabra (TTS)</strong>  alimentadas por <a href="https://huggingface.co/hexgrad/Kokoro-82M">Kokoro</a>.

<h2 id="installation">🐍 Instalación</h2>

Instalar usando el administrador de paquetes preferido. Recomendamos fuertemente el uso <code>uv</code>. Para instalar <code>uv</code>, consulta el <a href="https://docs.astral.sh/uv/getting-started/installation/#installation-methods">documentación oficial</a>.


Instalar con <code>uv</code>:



```bash
  uv pip install sinapsis-kokoro --extra-index-url https://pypi.sinapsis.tech
```

O con solo <code>pip</code>:

```bash
  pip install sinapsis-kokoro --extra-index-url https://pypi.sinapsis.tech
```

<blockquote>

[!IMPORTANT]
Las plantillas en cada paquete pueden requerir dependencias adicionales. Para el desarrollo, recomendamos instalar el paquete con todas las dependencias opcionales:

Con <code>uv</code>:

</blockquote>

```bash
  uv pip install sinapsis-kokoro[all] --extra-index-url https://pypi.sinapsis.tech
```

o con solo <code>pip</code>:

```bash
  pip install sinapsis-kokoro[all] --extra-index-url https://pypi.sinapsis.tech
```

<blockquote>

[!NOTE]
Zonos depende de la fonización de la biblioteca eSpeak. La instalación depende de su sistema operativo. Para Linux:

</blockquote>

```bash
apt install -y espeak-ng
```
<h2 id="features">🚀 Características
</h2><h3>Plantillas soportadas</h3>
Este módulo incluye una plantilla para síntesis de texto a palabra utilizando el modelo Kokoro TTS:
<ul>
<li>
<strong>KokoroTTS</strong>: Convierte texto al discurso utilizando el modelo Kokoro TTS. La plantilla procesa paquetes de texto del contenedor de entrada, genera el audio correspondiente utilizando Kokoro, y añade los paquetes de audio resultantes al contenedor.


<details><summary>Atributos</summary>
</details>

</li>

<li>
<code>speed</code> (Opcional): La velocidad a la que se generará el discurso (por defecto: <code>1</code>).
</li>

<li>
<code>split_pattern</code> (Opcional): El patrón de expresión regular utilizado para dividir el texto de entrada en pedazos más pequeños (por defecto: <code>r"\+"</code>).
</li>

<li>
<code>voice</code> (Opcional): El modelo de voz para usar para la síntesis del habla (por defecto:<code>af_heart</code>).

La lista de idiomas y voces soportadas por Kokoro se puede encontrar <a href="https:/huggingface.co/hexgrad/Kokoro-82M/blobmain/VOICES.md">Aquí.</a>
</li>
</ul>
<blockquote>

[! TIP]
Usa el comando de CLI <code>sinapsis info --example-template-config TEMPLATE_NAME</code> para producir un ejemplo Agente config para la Plantilla especificado en <strong><em>TEMPLATE_NAME</em></strong>.

</blockquote>

Por ejemplo, para <strong><em>KokoroTTS</em></strong> usa <code>sinapsis info --example-template-config KokoroTTS</code> para producir un config de ejemplo como:

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
<h2 id="example">📚 Ejemplo de uso</h2>
Este ejemplo ilustra cómo utilizar el <strong>KokoroTTS</strong> plantilla para síntesis de texto a palabra. Convierte la entrada de texto en el discurso usando el modelo Kokoro 82M v1.0 y guarda los archivos de audio resultantes localmente.


<details><summary><strong><span style="font-size: 1.4em;">Config</span></strong></summary>
</details>


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



Esta configuración define un <strong>Agente</strong> y una secuencia de <strong>plantillas</strong> para la conversión de texto al habla <strong>Kokoro</strong>.

<blockquote>

[!IMPORTANT]
El TextInput y AudioWriterSoundfile corresponden a <a href="https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_readers">sinapsis-data-readers</a> y <a href="https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_writers">sinapsis-data-writers</a>. Si desea utilizar el ejemplo, asegúrese de instalar los paquetes.

</blockquote>

Para ejecutar la configuración, utilice el CLI:

```bash
sinapsis run name_of_config.yml
```
<h2 id="webapp">🌐 Aplicación web</h2>
La aplicación web incluida en este proyecto muestra la modularidad de la <code>KokoroTTS</code> plantilla para tareas de generación de discursos.

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
docker compose -f docker/compose_apps.yaml up -d sinapsis-kokoro
```
<ol start="3">
<li><strong>Compruebe los registros</strong></li>
</ol>

```bash
docker logs -f sinapsis-kokoro
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
uv run webapps/packet_tts_apps/kokoro_tts_app.py
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

