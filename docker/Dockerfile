
FROM sinapsis-nvidia:base
RUN apt-get update && apt-get install -y cuda-toolkit-12-4 python3-dev git espeak-ng

ENV CMAKE_ARGS="-DGGML_CUDA=on"
ENV FORCE_CMAKE="1"
# sync all requirements including optional ones
COPY . /app/
WORKDIR /app

RUN uv sync --frozen

RUN uv pip install sinapsis-speech[all] --extra-index-url https://pypi.sinapsis.tech

