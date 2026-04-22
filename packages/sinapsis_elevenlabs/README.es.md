<h1 align="center"><br/><a href="https://sinapsis.tech/"><img alt="" src="https://github.com/Sinapsis-AI/brand-resources/blob/main/sinapsis_logo/4x/logo.png?raw=true" width="300"/></a><br/>Sinapsis Elevenlabs
<br/></h1>
<h4 align="center">Plantillas para la generación de habla avanzada con Elevenlabs</h4>
<p align="center"><a href="#installation">🐍 Instalación</a> •
<a href="#features"> 🚀 Características</a> •
<a href="#example"> 📚 Ejemplo de uso</a> •
<a href="#webapp">🌐 Aplicación web</a> •
<a href="#documentation">📙 Documentación</a> •
<a href="#packages">🔍 Licencia</a>


Esto <strong>Sinapsis Elevenlabs</strong> paquete ofrece un conjunto de plantillas y utilidades diseñadas para integrar, configurar y ejecutar sin esfuerzo <strong>texto a palabra (TTS)</strong>, <strong>(STS)</strong>, <strong>clonación de voz</strong>, y <strong>Generación de voz</strong> funcionalidades alimentadas por <a href="https://elevenlabs.io/">Once laboratorios</a>.

<h2 id="installation">🐍 Instalación</h2>

<blockquote>

[!IMPORTANT]
El proyecto Sinapsis requiere Python 3.10 o superior.

</blockquote>


Instalar usando el administrador de paquetes preferido. Recomendamos fuertemente el uso <code>uv</code>. Para instalar <code>uv</code>, consulta la <a href="https://docs.astral.sh/uv/getting-started/installation/#installation-methods">documentación oficial</a>.


Instalar con <code>uv</code>:



```bash
  uv pip install sinapsis-elevenlabs --extra-index-url https://pypi.sinapsis.tech
```

O con solo <code>pip</code>:

```bash
  pip install sinapsis-elevenlabs --extra-index-url https://pypi.sinapsis.tech
```

<blockquote>

[!IMPORTANT]
Las plantillas en cada paquete pueden requerir dependencias adicionales. Para el desarrollo, recomendamos instalar el paquete con todas las dependencias opcionales:

</blockquote>

Con <code>uv</code>:

```bash
  uv pip install sinapsis-elevenlabs[all] --extra-index-url https://pypi.sinapsis.tech
```

O con solo <code>pip</code>:

```bash
  pip install sinapsis-elevenlabs[all] --extra-index-url https://pypi.sinapsis.tech
```
<h2 id="features">🚀 Características</h2><h3>Plantillas soportadas</h3><ul>
<li>
<strong>OnceLabsSTS</strong>: Plantilla para transformar una voz en un personaje o estilo diferente usando la API de ElevenLabs Speech-to-Speech.


<details><summary>Atributos</summary>
</details>

<ul>
<li><code>api_key</code>(Opcional): La clave de API utilizada para autenticar con la API de ElevenLabs. Aunque este parámetro es opcional en la firma de funciones, <strong>la clave de API debe ser proporcionada</strong> o bien a través de este argumento o <code>ELEVENLABS_API_KEY</code> variable ambiental. Si no se proporciona ninguno, se registrará un error y no se generará ningún discurso.</li>

<li><code>model</code>(Opcional): El identificador modelo para usar para la síntesis del habla (por defecto: <code>eleven_multilingual_sts_v2</code>). Opciones: <code>eleven_english_sts_v2</code>, <code>eleven_multilingual_sts_v2</code>.</li>

<li><code>output_format</code>(Opcional): El formato de audio de salida y la calidad (por defecto: <code>mp3_44100_128</code>). Opciones: <code>mp3_22050_32</code>, <code>mp3_44100_32</code>, <code>mp3_44100_64</code>, ¨C21C, ¨C22C, ¨C23C, ¨C24C, ¨C25C, ¨C26C, ¨C27C, ¨C28C.</li>

<li>¨C29C(Opcional): La carpeta donde se guardarán los archivos de audio generados (por defecto: ¨C30C).</li>

<li>¨C31C(Opcional): Si es cierto, el audio es devuelto como un flujo; de lo contrario, se guarda en un archivo (por defecto: ¨C32C).</li>

<li>¨C33C(Opcional): Optimización de latencia para el streaming (por defecto: ninguno).</li>

<li>¨C34C(Opcional): Voz para la síntesis del discurso. Puede ser un ID de voz (str), nombre (str), o ElevenLabs objeto de voz (Voice) (por defecto: Ninguno).</li>

<li>¨C35C(Opcional): Diccionario de configuración de control de voz:<ul>
<li>¨C36C: Controla la aleatoriedad de voz y el rango emocional (rango: 0.0 a 1.0).</li>

<li>¨C37C: Ajusta cuán de cerca coincide la voz con el original (rango: 0.0 a 1.0).</li>

<li>¨C38C: Amplifica el estilo del orador, consumiendo más recursos (rango: 0,0 a 1.0).</li>

<li>¨C39C: Aumenta la similitud con el altavoz con mayor costo computacional (boolean: ¨C40C o ¨C41C).</li>

<li>¨C42C: Ajusta la velocidad del habla (rango: 0.7 a 1.2, predeterminado: 1.0).
</li>
</ul></li>
</ul></li>

<li>
<strong>11LabsTTS</strong>: Plantilla para convertir texto en discurso usando modelos de voz de ElevenLabs.


<details><summary>Atributos</summary>
</details>

<ul>
<li><code>api_key</code>(Opcional): La clave de API utilizada para autenticar con la API de ElevenLabs. Aunque este parámetro es opcional en la firma de funciones, <strong>la clave de API debe ser proporcionada</strong> o bien a través de este argumento o <code>ELEVENLABS_API_KEY</code> variable ambiental. Si no se proporciona ninguno, se registrará un error y no se generará ningún discurso.</li>

<li><code>model</code>(Opcional): El identificador modelo para usar para la síntesis del habla (por defecto: <code>eleven_turbo_v2_5</code>). Opciones: <code>eleven_turbo_v2_5</code>, <code>eleven_multilingual_v2</code>, <code>eleven_turbo_v2</code>, <code>eleven_monolingual_v1</code>, <code>eleven_multilingual_v1</code>.</li>

<li><code>output_format</code>(Opcional): El formato de audio de salida y la calidad (por defecto: <code>mp3_44100_128</code>). Opciones: <code>mp3_22050_32</code>, <code>mp3_44100_32</code>, <code>mp3_44100_64</code>, <code>mp3_44100_96</code>, <code>mp3_44100_128</code>, <code>mp3_44100_192</code>, <code>pcm_16000</code>, <code>pcm_22050</code>, <code>pcm_24000</code>, ¨C63C, ¨C64C.</li>

<li><code>output_folder</code>(Opcional): La carpeta donde se guardarán los archivos de audio generados (por defecto: <code>SINAPSIS_CACHE_DIR/elevenlabs/audios</code>).</li>

<li><code>stream</code>(Opcional): Si es cierto, el audio es devuelto como un flujo; de lo contrario, se guarda en un archivo (por defecto: <code>False</code>).</li>

<li><code>voice</code>(Opcional): Voz para la síntesis del discurso. Puede ser un ID de voz (str), nombre (str), o ElevenLabs objeto de voz (Voice) (por defecto: Ninguno).</li>

<li><code>voice_settings</code>(Opcional): Diccionario de configuración de control de voz:<ul>
<li><code>stability</code>: Controla la aleatoriedad de voz y el rango emocional (rango: 0.0 a 1.0).</li>

<li><code>similarity_boost</code>: Ajusta cuán de cerca coincide la voz con el original (rango: 0.0 a 1.0).</li>

<li><code>style</code>: Amplifica el estilo del orador, consumiendo más recursos (rango: 0,0 a 1.0).</li>

<li><code>use_speaker_boost</code>: Aumenta la similitud con el altavoz con mayor costo computacional (boolean: <code>True</code> o <code>False</code>).</li>

<li><code>speed</code>: Ajusta la velocidad del habla (rango: 0.7 a 1.2, predeterminado: 1.0).
</li>
</ul></li>
</ul></li>

<li>
<strong>OnceLabsVoiceClone</strong>: Plantilla para crear una copia sintética de una voz existente usando la API de ElevenLabs.


<details><summary>Atributos</summary>
</details>

<ul>
<li><code>api_key</code>(Opcional): La clave de API utilizada para autenticar con la API de ElevenLabs. Aunque este parámetro es opcional en la firma de funciones, <strong>la clave de API debe ser proporcionada</strong> o bien a través de este argumento o <code>ELEVENLABS_API_KEY</code> variable ambiental. Si no se proporciona ninguno, se registrará un error y no se generará ningún discurso.</li>

<li><code>description</code>(Opcional): Descripción para la voz clonada (por defecto: ninguno).</li>

<li><code>model</code>(Opcional): El identificador modelo para usar para la síntesis del habla (por defecto: <code>eleven_turbo_v2_5</code>). Opciones: <code>eleven_turbo_v2_5</code>, <code>eleven_multilingual_v2</code>, <code>eleven_turbo_v2</code>, <code>eleven_monolingual_v1</code>, <code>eleven_multilingual_v1</code>.</li>

<li><code>name</code>(Opcional): Nombre para la voz clonada (por defecto: ninguno). Si Ninguno, se puede utilizar un nombre predeterminado.</li>

<li><code>output_format</code>(Opcional): El formato de audio de salida y la calidad (por defecto: <code>mp3_44100_128</code>). Opciones: <code>mp3_22050_32</code>, <code>mp3_44100_32</code>, <code>mp3_44100_64</code>, <code>mp3_44100_96</code>, <code>mp3_44100_128</code>, <code>mp3_44100_192</code>, <code>pcm_16000</code>, <code>pcm_22050</code>, <code>pcm_24000</code>, ¨C100C, ¨C101C.</li>

<li><code>output_folder</code>(Opcional): La carpeta donde se guardarán los archivos de audio generados (por defecto: <code>SINAPSIS_CACHE_DIR/elevenlabs/audios</code>).</li>

<li><code>remove_background_noise</code>(Opcional): Ya sea para eliminar el ruido de fondo de las muestras (por defecto: <code>False</code>).</li>

<li><code>stream</code>(Opcional): Si es cierto, el audio es devuelto como un flujo; de lo contrario, se guarda en un archivo (por defecto: <code>False</code>).</li>

<li><code>voice</code>(Opcional): Voz para la síntesis del discurso. Puede ser un ID de voz (str), nombre (str), o ElevenLabs objeto de voz (Voice) (por defecto: Ninguno).</li>

<li><code>voice_description</code>(Requerido): Una descripción de la voz que se utilizará para la síntesis. Este campo es obligatorio y ayuda a definir las características o estilo de la voz.</li>

<li><code>voice_settings</code>(Opcional): Diccionario de configuración de control de voz:<ul>
<li><code>stability</code>: Controla la aleatoriedad de voz y el rango emocional (rango: 0.0 a 1.0).</li>

<li><code>similarity_boost</code>: Ajusta cuán de cerca coincide la voz con el original (rango: 0.0 a 1.0).</li>

<li><code>style</code>: Amplifica el estilo del orador, consumiendo más recursos (rango: 0,0 a 1.0).</li>

<li><code>use_speaker_boost</code>: Aumenta la similitud con el altavoz con mayor costo computacional (boolean: <code>True</code> o <code>False</code>).</li>

<li><code>speed</code>: Ajusta la velocidad del habla (rango: 0.7 a 1.2, predeterminado: 1.0).
</li>
</ul></li>
</ul></li>

<li>
<strong>OnceLabsVoiceGeneration</strong>: Plantilla para generar voces sintéticas personalizadas basadas en descripciones proporcionadas por el usuario.


<details><summary>Atributos</summary>
</details>

<ul>
<li><code>api_key</code>(Opcional): La clave de API utilizada para autenticar con la API de ElevenLabs. Aunque este parámetro es opcional en la firma de funciones, <strong>la clave de API debe ser proporcionada</strong> o bien a través de este argumento o <code>ELEVENLABS_API_KEY</code> variable ambiental. Si no se proporciona ninguno, se registrará un error y no se generará ningún discurso.</li>

<li><code>model</code>(Opcional): El identificador modelo para usar para la síntesis del habla (por defecto: <code>eleven_turbo_v2_5</code>). Opciones: <code>eleven_turbo_v2_5</code>, <code>eleven_multilingual_v2</code>, <code>eleven_turbo_v2</code>, <code>eleven_monolingual_v1</code>, <code>eleven_multilingual_v1</code>.</li>

<li><code>output_format</code>(Opcional): El formato de audio de salida y la calidad (por defecto: <code>mp3_44100_128</code>). Opciones: <code>mp3_22050_32</code>, <code>mp3_44100_32</code>, <code>mp3_44100_64</code>, <code>mp3_44100_96</code>, <code>mp3_44100_128</code>, <code>mp3_44100_192</code>, <code>pcm_16000</code>, <code>pcm_22050</code>, <code>pcm_24000</code>, ¨C138C, ¨C139C.</li>

<li><code>output_folder</code>(Opcional): La carpeta donde se guardarán los archivos de audio generados (por defecto: <code>SINAPSIS_CACHE_DIR/elevenlabs/audios</code>).</li>

<li><code>stream</code>(Opcional): Si es cierto, el audio es devuelto como un flujo; de lo contrario, se guarda en un archivo (por defecto: <code>False</code>).</li>

<li><code>voice</code>(Opcional): Voz para la síntesis del discurso. Puede ser un ID de voz (str), nombre (str), o ElevenLabs objeto de voz (Voice) (por defecto: Ninguno).</li>

<li><code>voice_description</code>(Requerido): Una descripción de la voz que se utilizará para la síntesis. Este campo es obligatorio y ayuda a definir las características o estilo de la voz.</li>

<li><code>voice_settings</code>(Opcional): Diccionario de configuración de control de voz:<ul>
<li><code>stability</code>: Controla la aleatoriedad de voz y el rango emocional (rango: 0.0 a 1.0).</li>

<li><code>similarity_boost</code>: Ajusta cuán de cerca coincide la voz con el original (rango: 0.0 a 1.0).</li>

<li><code>style</code>: Amplifica el estilo del orador, consumiendo más recursos (rango: 0,0 a 1.0).</li>

<li><code>use_speaker_boost</code>: Aumenta la similitud con el altavoz con mayor costo computacional (boolean: <code>True</code> o <code>False</code>).</li>

<li><code>speed</code>: Ajusta la velocidad del habla (rango: 0.7 a 1.2, predeterminado: 1.0).
</li>
</ul></li>
</ul></li>
</ul>
<blockquote>

[! TIP]
Usa el comando de CLI <code>sinapsis info --example-template-config TEMPLATE_NAME</code> para producir un ejemplo Agente config para la Plantilla especificado en <strong><em>TEMPLATE_NAME</em></strong>.

</blockquote>

Por ejemplo, para <strong><em>11LabsTTS</em></strong> usa <code>sinapsis info --example-template-config ElevenLabsTTS</code> para producir un config de ejemplo como:

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
<h2 id="example">📚 Ejemplo de uso</h2>
Este ejemplo muestra cómo utilizar el <strong>OnceLabsVoiceGeneration</strong> plantilla para convertir texto en discurso. Genera discurso basado en una voz creada a partir de la descripción del usuario y guarda el archivo de audio resultante localmente.


<details><summary><strong><span style="font-size: 1.4em;">Config</span></strong></summary>
</details>


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



Esta configuración define un <strong>Agente</strong> y una secuencia de <strong>plantillas</strong> para la síntesis del discurso, utilizando una voz personalizada creada a través de <strong>Once laboratorios</strong>.

<blockquote>

[!IMPORTANT]
La plantilla TextInput corresponde a <a href="https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_readers">sinapsis-data-readers</a>. Si desea utilizar el ejemplo, asegúrese de instalar el paquete.

</blockquote>

Para ejecutar la configuración, utilice el CLI:

```bash
sinapsis run name_of_config.yml
```
<h2 id="webapp">🌐 Aplicación web</h2>
Las aplicaciones web incluidas en este proyecto muestran la modularidad de las plantillas de OnceLabs, en este caso para tareas de generación de discursos.

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
Oncelabs requiere una clave de API para ejecutar cualquier inferencia. Para empezar, visite el <a href="https://elevenlabs.io">sitio web oficial</a> y crear una cuenta. Si ya tienes una cuenta, ve a la <a href="https://elevenlabs.io/app/settings/api-keys">Página de claves de API</a> para generar una señal.

[!IMPORTANT]
Establezca su var env usando <code> export ELEVENLABS_API_KEY='your-api-key'</code>

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
docker compose -f docker/compose_apps.yaml up -d sinapsis-elevenlabs
```
<ol start="3">
<li><strong>Compruebe los registros</strong></li>
</ol>

```bash
docker logs -f sinapsis-elevenlabs
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
uv run webapps/generic_tts_apps/elevenlabs_tts_app.py
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

