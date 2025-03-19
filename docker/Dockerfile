
FROM sinapsis-nvidia:base
RUN apt-get update && apt-get install -y cuda-toolkit-12-4 python3-dev
COPY . /app/
WORKDIR /app

RUN uv sync --frozen

RUN uv pip install sinapsis-speech[all] --extra-index-url https://pypi.sinapsis.tech

