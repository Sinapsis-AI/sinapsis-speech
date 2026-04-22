<h1 align="center">
<br/>
<a href="https://sinapsis.tech/">
<img alt="" src="https://github.com/Sinapsis-AI/brand-resources/blob/main/sinapsis_logo/4x/logo.png?raw=true" width="300"/>
</a>
<br/>Sinapsis Speech
<br/>
</h1>

<h4 align="center"> Un mono-repositorio alberga múltiples paquetes y plantillas para una generación de voz versátil, texto a palabra, discurso a texto y más allá.</h4>

<p align="center">
<a href="#installation">🐍 Instalación</a> •
<a href="#packages">📦 Paquetes</a> •
<a href="#webapp">🌐 Aplicación Webs</a> •
<a href="#documentation">📙 Documentación</a> •
<a href="#packages">🔍 Licencia</a>
</p>
<h2 id="installation">🐍 Instalación</h2>

<blockquote>

[!IMPORTANT]
Los proyectos de sinapsis requieren Python 3.10 o superior.

</blockquote>

Este repo incluye paquetes para realizar síntesis de discursos utilizando diferentes herramientas:

* <code>sinapsis-elevenlabs</code>
* <code>sinapsis-f5-tts</code>
* <code>sinapsis-kokoro</code>
* <code>sinapsis-zonos</code>
* <code>sinapsis-orpheus-cpp</code>
* <code>sinapsis-parakeet</code>

Instalar usando el administrador de paquetes preferido. Recomendamos fuertemente el uso <code>uv</code>. Para instalar <code>uv</code>, consulta la <a href="https://docs.astral.sh/uv/getting-started/installation/#installation-methods">documentación oficial</a>.

Instalar con <code>uv</code>:

```bash
uv pip install sinapsis-elevenlabs --extra-index-url https://pypi.sinapsis.tech
```

O con solo <code>pip</code>:

```bash
pip install sinapsis-elevenlabs --extra-index-url https://pypi.sinapsis.tech
```

**Reemplaza <code>sinapsis-elevenlabs</code> con el nombre del paquete que pretendes instalar**.

<blockquote>

[!IMPORTANT]
Las plantillas en cada paquete pueden requerir dependencias adicionales. Para el desarrollo, recomendamos instalar el paquete todas las dependencias opcionales:

Con <code>uv</code>:

</blockquote>

```bash
uv pip install sinapsis-elevenlabs[all] --extra-index-url https://pypi.sinapsis.tech
```

O con solo <code>pip</code>:

```bash
pip install sinapsis-elevenlabs[all] --extra-index-url https://pypi.sinapsis.tech
```

**Asegúrate de sustituir <code>sinapsis-elevenlabs</code> con el nombre apropiado del paquete**.

<blockquote>

[!TIP]
También puedes instalar todos los paquetes dentro de este proyecto:

</blockquote>

```bash
uv pip install sinapsis-speech[all] --extra-index-url https://pypi.sinapsis.tech
```

<h2 id="packages">📦 Paquetes</h2>

Este repositorio se organiza en paquetes modulares, cada uno diseñado para la integración con diferentes herramientas de texto a voz. Estos paquetes proporcionan plantillas listas para usar para la síntesis de discursos. A continuación se presenta una visión general de los paquetes disponibles:

<details>
<summary id="elevenlabs"><strong><span style="font-size: 1.4em;"> Sinapsis ElevenLabs </span></strong></summary>

Este paquete ofrece un conjunto de plantillas y utilidades diseñadas para integrar, configurar y ejecutar sin esfuerzo **texto a palabra (TTS)**, **(STS)**, **clonación de voz**, y **Generación de voz** funcionalidades alimentadas por <a href="https://elevenlabs.io/">Once laboratorios</a>.

- **OnceLabsSTS**: Plantilla para transformar una voz en un personaje o estilo diferente usando la API de ElevenLabs Speech-to-Speech.

- **11LabsTTS**: Plantilla para convertir texto en discurso usando modelos de voz de ElevenLabs.

- **OnceLabsVoiceClone**: Plantilla para crear una copia sintética de una voz existente usando la API de ElevenLabs.

- **OnceLabsVoiceGeneration**: Plantilla para generar voces sintéticas personalizadas basadas en descripciones proporcionadas por el usuario.

Para instrucciones específicas y más detalles, ver el <a href="https://github.com/Sinapsis-AI/sinapsis-speech/blob/main/packages/sinapsis_elevenlabs/README.md">README.md</a>.

</details>

<details>
<summary id="f5tts"><strong><span style="font-size: 1.4em;"> Sinapsis F5-TTS</span></strong></summary>

Este paquete proporciona una plantilla para integrar, configurar y ejecutar sin problemas **texto a palabra (TTS)** funcionalidades alimentadas por <a href="https://github.com/SWivid/F5-TTS">F5TTS</a>.

* **F5TTSInference**: Convierte texto al discurso usando el modelo F5TTS con capacidades de clonación de voz.

Para instrucciones específicas y más detalles, ver el <a href="https://github.com/Sinapsis-AI/sinapsis-speech/blob/main/packages/sinapsis_f5_tts/README.md">README.md</a>.

</details>

<details>
<summary id="f5tts"><strong><span style="font-size: 1.4em;"> Sinapsis Kokoro</span></strong></summary>

Este paquete proporciona una plantilla única para integrar, configurar y ejecutar la síntesis de texto a palabra (TTS) usando la <a href="https://huggingface.co/hexgrad/Kokoro-82M">Kokoro 82M v1.0</a> modelo.

KokoroTTS: Convierte texto al discurso usando el modelo Kokoro TTS. La plantilla procesa paquetes de texto del contenedor de entrada, genera el audio correspondiente utilizando Kokoro, y añade los paquetes de audio resultantes al contenedor.
Para instrucciones específicas y más detalles, ver el <a href="https://github.com/Sinapsis-AI/sinapsis-speech/blob/main/packages/sinapsis_kokoro/README.md">README.md</a>.
</details>
<details>
<summary id="zonos"><strong><span style="font-size: 1.4em;"> Sinapsis Zonos</span></strong></summary>

Este paquete proporciona una plantilla única para integrar, configurar y ejecutar **texto a palabra (TTS)** y **clonación de voz** funcionalidades alimentadas por <a href="https://github.com/Zyphra/Zonos/tree/main">Zonos</a>.

* **ZonosTTS**: Plantilla para la conversión de texto al lenguaje o la clonación de voz basada en la presencia de una muestra de audio.

Para instrucciones específicas y más detalles, ver el <a href="https://github.com/Sinapsis-AI/sinapsis-speech/blob/main/packages/sinapsis_zonos/README.md">README.md</a>.

</details>

<details>
<summary id="orpheus-cpp"><strong><span style="font-size: 1.4em;"> Sinapsis Orppheus-CPP</span></strong></summary>

Este paquete proporciona una plantilla para integrar, configurar y ejecutar sin problemas **texto a palabra (TTS)** funcionalidades alimentadas por <a href="https://github.com/canopyai/Orpheus-TTS">Orpheus-TTS</a>.

* **OrpheusTTS**: Convierte texto al discurso usando el modelo Orpheus TTS con una avanzada síntesis de voz neuronal. La plantilla procesa paquetes de texto del contenedor de entrada, genera el audio correspondiente utilizando Orpheus TTS, y añade los paquetes de audio resultantes al contenedor. Características manejo de errores graciosas para condiciones fuera de memoria

Para instrucciones específicas y más detalles, ver el <a href="https://github.com/Sinapsis-AI/sinapsis-speech/blob/main/packages/sinapsis_orpheus_cpp/README.md">README.md</a>.

</details>

<details>
<summary id="parakeet-tdt"><strong><span style="font-size: 1.4em;"> Sinapsis Parakeet-TDT</span></strong></summary>

Este paquete proporciona una plantilla para integrar, configurar y ejecutar sin problemas **discurso a texto (STT)** funcionalidades alimentadas por <a href="https://huggingface.co/nvidia/parakeet-tdt-0.6b-v2">Modelo TDT de NVIDIA</a>.

* **ParakeetTDTInference**: Convierte el discurso en texto usando el modelo TDT 0.6B de NVIDIA. Esta plantilla procesa paquetes de audio del contenedor de entrada o rutas de archivo especificadas, realiza la transcripción con predicción de timetamp opcional, y añade los paquetes de texto resultantes al contenedor.

Para instrucciones específicas y más detalles, ver el <a href="https://github.com/Sinapsis-AI/sinapsis-speech/blob/main/packages/sinapsis_parakeet_tdt/README.md">README.md</a>.

</details>

<h2 id="webapp">🌐 Aplicación Webs</h2>

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
Si deseas habilitar el intercambio de aplicaciones externas en Gradio, <code>export GRADIO_SHARE_APP=True</code>

[!IMPORTANT]
Elevenlabs requiere una clave de API para ejecutar cualquier inferencia. Para empezar, visite el <a href="https://elevenlabs.io">sitio web oficial</a> y crear una cuenta. Si ya tienes una cuenta, ve a la <a href="https://elevenlabs.io/app/settings/api-keys">Página de claves de API</a> para generar una señal.

[!IMPORTANT]
Establezca su var env usando <code> export ELEVENLABS_API_KEY='your-api-key'</code>

[!IMPORTANT]
F5-TTS requiere un archivo de audio de referencia para la clonación de voz. Asegúrate de tener un archivo de audio de referencia en el directorio de artefactos.

[!NOTE]
La configuración del agente puede cambiarse a través de la <code>AGENT_CONFIG_PATH</code> env var. Puede comprobar las configuraciones disponibles en cada carpeta de configuración de paquetes.

</blockquote>

<details>
<summary id="docker"><strong><span style="font-size: 1.4em;">🐳 Docker</span></strong></summary>

**IMPORTANTE**: Esta imagen Docker depende de <code>sinapsis-nvidia:base</code> imagen. Para instrucciones detalladas, consulta el <a href="https://github.com/Sinapsis-ai/sinapsis?tab=readme-ov-file#docker">Sinapsis README</a>.

1.  **Construir la imagen de sinapsis-habla**:

```bash
docker compose -f docker/compose.yaml build
```

2. **Iniciar el contenedor de aplicaciones**:
- Para Once laboratorios:

```bash
docker compose -f docker/compose_apps.yaml up -d sinapsis-elevenlabs
```
- Para F5-TTS:

```bash
docker compose -f docker/compose_apps.yaml up -d sinapsis-f5_tts
```
- Para Kokoro:

```bash
docker compose -f docker/compose_apps.yaml up -d sinapsis-kokoro
```
- Para Zonos:

```bash
docker compose -f docker/compose_apps.yaml up -d sinapsis-zonos
```
- Para Orfeo-CPP:

```bash
docker compose -f docker/compose_apps.yaml up -d sinapsis-orpheus-tts
```
- Para el Parakeet:

```bash
docker compose -f docker/compose_apps.yaml up -d sinapsis-parakeet
```

3. **Comprueba los registros**
- Para Once laboratorios:

```bash
docker logs -f sinapsis-elevenlabs
```
- Para F5-TTS:

```bash
docker logs -f sinapsis-f5tts
```
- Para Kokoro:

```bash
docker logs -f sinapsis-kokoro
```
- Para Zonos:

```bash
docker logs -f sinapsis-zonos
```
- Para Orfeo-CPP:

```bash
docker logs -f sinapsis-orpheus-tts
```
- Para el Parakeet:

```bash
docker logs -f sinapsis-parakeet
```

4. **Los registros mostrarán la URL para acceder a la aplicación web, por ejemplo:**:

```bash
Running on local URL:  http://127.0.0.1:7860
```

**NOTA**: La url puede ser diferente, comprueba la salida de los registros.

5. **Para detener la aplicación**:

```bash
docker compose -f docker/compose_apps.yaml down
```
</details>

<details>

<summary id="virtual-environment"><summary id="docker"><strong><span style="font-size: 1.4em;">💻 UV</span></strong></summary>

Para ejecutar la aplicación web utilizando <code>uv</code> gestor de paquetes, siga estos pasos:

<blockquote>

[!IMPORTANT]
Si está usando sinapsis-orpheus-cpp, necesita exportar variables de entorno cuda:

</blockquote>

```bash
export CMAKE_ARGS="-DGGML_CUDA=on"
export FORCE_CMAKE="1"
export CUDACXX=$(command -v nvcc)
```

1.  **Sincronizar el entorno virtual**:

```bash
uv sync --frozen
```

2. **Instalar la rueda**:

```bash
uv pip install sinapsis-speech[all] --extra-index-url https://pypi.sinapsis.tech
```

3. **Ejecuta la aplicación web**:
- Para Once laboratorios:

```bash
uv run webapps/generic_tts_apps/elevenlabs_tts_app.py
```
- Para F5-TTS:

```bash
uv run webapps/packet_tts_apps/f5_tts_app.py
```
- Para Kokoro:

```bash
uv run webapps/packet_tts_apps/kokoro_tts_app.py
```
- Para Zonos:

```bash
uv run webapps/generic_tts_apps/zonos_tts_app.py
```

4. **El terminal mostrará la URL para acceder a la aplicación web (por ejemplo)**:

```bash
Running on local URL:  http://127.0.0.1:7860
```

**NOTA**: La URL puede variar; comprueba la salida de la terminal para la dirección correcta.

</details>

<h2 id="documentation">📙 Documentación</h2>

La documentación está disponible en el sitio <a href="https://docs.sinapsis.tech/docs">web de sinapsis</a>

Los tutoriales para diferentes proyectos dentro de sinapsis están disponibles en <a href="https://docs.sinapsis.tech/tutorials">la página de tutoriales de sinapsis</a>

<h2 id="license">🔍 Licencia</h2>

Este proyecto está licenciado bajo la licencia AGPLv3, que fomenta la colaboración abierta y el intercambio. Para más detalles, consulta el <a href="LICENSE">LICENSE</a> archivo.

Para uso comercial, consulta nuestra página <a href="https://sinapsis.tech">Sitio web de Sinapsis</a> para información sobre la obtención de una licencia comercial.

