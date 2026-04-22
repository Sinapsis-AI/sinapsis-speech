<h1 align="center"><br/><a href="https://sinapsis.tech/"><img alt="" src="https://github.com/Sinapsis-AI/brand-resources/blob/main/sinapsis_logo/4x/logo.png?raw=true" width="300"/></a><br/>Sinapsis Orpheus-CPP
<br/></h1>
<h4 align="center">Plantillas para la generación avanzada de texto a palabra con Orpheus-TTS</h4>
<p align="center"><a href="#installation">🐍 Instalación</a> •
<a href="#features"> 🚀 Características</a> •
<a href="#example"> 📚 Ejemplo de uso</a> •
<a href="#webapp">🌐 Aplicación web</a> •
<a href="#documentation">📙 Documentación</a> •
<a href="#packages">🔍 Licencia</a>

<strong>Sinapsis Orpheus-CPP</strong> proporciona una plantilla para integrar, configurar y ejecutar sin problemas <strong>texto a palabra (TTS)</strong> funcionalidades alimentadas por <a href="https://github.com/canopyai/Orpheus-TTS">Orpheus-TTS</a>.

<h2 id="installation">🐍 Instalación</h2>

Instala usando tu administrador de paquetes favorito. Alentamos firmemente el uso de <code>uv</code>, aunque cualquier otro administrador de paquetes debe trabajar también.
Si necesita instalar <code>uv</code> Por favor, veamos <a href="https://docs.astral.sh/uv/getting-started/installation/#installation-methods">documentación oficial</a>.


Ejemplo con <code>uv</code>:



```bash
  uv pip install sinapsis-orpheus-cpp --extra-index-url https://pypi.sinapsis.tech
```

o con solo <code>pip</code>:

```bash
  pip install sinapsis-orpheus-cpp --extra-index-url https://pypi.sinapsis.tech
```

<blockquote>

[!IMPORTANT]
Las plantillas en cada paquete pueden requerir dependencias adicionales. Para el desarrollo, recomendamos instalar el paquete con todas las dependencias opcionales:

con <code>uv</code>:

</blockquote>

```bash
  uv pip install sinapsis-orpheus-cpp[all] --extra-index-url https://pypi.sinapsis.tech
```

o con solo <code>pip</code>:

```bash
  pip install sinapsis-orpheus-cpp[all] --extra-index-url https://pypi.sinapsis.tech
```
<h2 id="features">🚀 Características
</h2><h3>Plantillas soportadas</h3>
Este módulo incluye una plantilla para síntesis de texto a palabra utilizando el modelo Orpheus TTS:

<strong>OrpheusTTS</strong>: Plantilla de síntesis avanzada de texto a palabra impulsada por Orpheus TTS, entregando un discurso humano con intonación natural, emoción y ritmo que supera los modelos de código cerrado de última generación. La plantilla soporta la síntesis de habla expresiva a través de etiquetas emotivas incluyendo <code><laugh></code>, <code><chuckle></code>, <code><sigh></code>, <code><cough></code>, <code><sniffle></code>, <code><groan></code>, <code><yawn></code>, y <code><gasp></code> para mejores expresiones vocales. Además, proporciona soporte multilingüe cuando se configura con la ruta adecuada del modelo Hugging Face, lo que hace que sea versátil para aplicaciones globales.


<details><summary>Atributos</summary>
</details>

<ul>
<li><code>n_gpu_layers</code>: Número de capas modelo para descargar a GPU (-1 = utilizar todas las capas, 0 = CPU solamente) (por defecto: -1)</li>

<li><code>n_threads</code>: Número de hilos CPU para utilizar para inferencia modelo (0 = auto-detecto) (por defecto: 0)</li>

<li><code>n_ctx</code>: Tamaño de la ventana contexto (número máximo de fichas, 0 = máximo del modelo de uso) (por defecto: 8192)</li>

<li><code>model_id</code>: Hugging Face model repository ID (requerido)</li>

<li><code>model_variant</code>: Archivo GGUF específico para descargar del repositorio (por defecto: ninguno)</li>

<li><code>cache_dir</code>: Directorio para almacenar los modelos descargados y los archivos de caché (por defecto: SINAPSIS<em>CACHE</em>DIR)</li>

<li><code>verbose</code>: Activar el registro de verbose para las operaciones modelo (por defecto: Falso)</li>

<li><code>voice_id</code>: Identificador de voz para la síntesis del habla (requirido)</li>

<li><code>batch_size</code>: Tamaño del lote para inferencia modelo (por defecto: 1)</li>

<li><code>max_tokens</code>: Número máximo de fichas para generar discurso (por defecto: 2048)</li>

<li><code>temperature</code>: Temperatura de muestreo para la generación de token (predeterminado: 0.8)</li>

<li>¨C29C: umbral de probabilidad de muestreo nucleus (por defecto: 0.95)</li>

<li>¨C30C: Parámetro de muestreo de alta velocidad (por defecto: 40)</li>

<li>¨C31C: umbral de probabilidad mínima para la selección de token (por defecto: 0.05)</li>

<li>¨C32C: Duración en segundos de audio para generar antes de producir el primer trozo (por defecto: 1.5)</li>
</ul>


<blockquote>

[! TIP]
Usa el comando de CLI <code>sinapsis info --example-template-config TEMPLATE_NAME</code> para producir un ejemplo Agente config para la Plantilla especificado en <strong><em>TEMPLATE_NAME</em></strong>.

</blockquote>

Por ejemplo, para <strong><em>OrpheusTTS</em></strong> usa <code>sinapsis info --example-template-config OrpheusTTS</code> para producir un config de ejemplo como:

```yaml
agent:
  name: my_test_agent
templates:
- template_name: InputTemplate
  class_name: InputTemplate
  attributes: {}
- template_name: OrpheusTTS
  class_name: OrpheusTTS
  template_input: InputTemplate
  attributes:
    n_gpu_layers: -1
    n_threads: 0
    n_ctx: 8192
    model_id: '`replace_me:<class ''str''>`'
    model_variant: null
    cache_dir: ~/sinapsis_cache
    verbose: false
    voice_id: '`replace_me:<class ''str''>`'
    batch_size: 1
    max_tokens: 2048
    temperature: 0.8
    top_p: 0.95
    top_k: 40
    min_p: 0.05
    pre_buffer_size: 1.5
```
<h2 id="example">📚 Ejemplo de uso</h2>
Este ejemplo ilustra cómo utilizar el <strong>OrpheusTTS</strong> plantilla para síntesis de texto a palabra. Convierte la entrada de texto en el discurso usando Orpheus-TTS y guarda el archivo de audio resultante localmente.


<details><summary><strong><span style="font-size: 1.4em;">Config</span></strong></summary>
</details>


```yaml
agent:
  name: orpheus_tts_agent
  description: "Agent that generates speech from text using the Orpheus TTS model."

templates:
- template_name: InputTemplate
  class_name: InputTemplate
  attributes: {}

- template_name: TextInput
  class_name: TextInput
  template_input: InputTemplate
  attributes:
    source: "user_input"
    text: "Hi, I'm Tara. Welcome to Orpheus text-to-speech system! I can speak in a very natural way."

- template_name: OrpheusTTS
  class_name: OrpheusTTS
  template_input: TextInput
  attributes:
    n_gpu_layers: -1
    n_ctx: 4096
    model_id: "isaiahbjork/orpheus-3b-0.1-ft-Q4_K_M-GGUF"
    voice_id: "tara"
    temperature: 0.8
    top_p: 0.95
    top_k: 40
    min_p: 0.05
    pre_buffer_size: 1.5
    max_tokens: 2048

- template_name: SaveGeneratedAudio
  class_name: AudioWriterSoundfile
  template_input: OrpheusTTS
  attributes:
    save_dir: "orpheus_tts"
    root_dir: "artifacts"
    extension: "wav"
```



Esta configuración define un <strong>Agente</strong> y una secuencia de <strong>plantillas</strong> para la conversión de texto al habla <strong>Orpheus-TTS</strong>.

<blockquote>

[!IMPORTANT]
El TextInput y AudioWriterSoundfile corresponden a <a href="https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_writers">sinapsis-data-writers</a>. Si desea utilizar el ejemplo, asegúrese de instalar los paquetes.

</blockquote>

Para ejecutar la configuración, utilice el CLI:

```bash
sinapsis run name_of_config.yml
```
<h2 id="webapp">🌐 Aplicación web</h2>
La aplicación web incluida en este proyecto muestra la modularidad de la plantilla Orpheus TTS para tareas de generación de discursos.

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
docker compose -f docker/compose_apps.yaml up -d sinapsis-orpheus-tts
```
<ol start="3">
<li><strong>Compruebe los registros</strong></li>
</ol>

```bash
docker logs -f sinapsis-orpheus-tts
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
<li><strong>Exportar la variable ambiente para instalar las fijaciones de pitón para llama-cpp</strong>:</li>
</ol>

```bash
export CMAKE_ARGS="-DGGML_CUDA=on"
export FORCE_CMAKE="1"
```
<ol start="2">
<li><strong>Exportar CUDACXX</strong>:</li>
</ol>

```bash
export CUDACXX=$(command -v nvcc)
```
<ol start="3">
<li><strong>Sincronizar el entorno virtual</strong>:</li>
</ol>

```bash
uv sync --frozen
```
<ol start="4">
<li><strong>Instalar la rueda</strong>:</li>
</ol>

```bash
uv pip install sinapsis-speech[all] --extra-index-url https://pypi.sinapsis.tech
```
<ol start="5">
<li><strong>Ejecute la aplicación web</strong>:</li>
</ol>

```bash
uv run webapps/packet_tts_apps/orpheus_tts_app.py
```
<ol start="6">
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

