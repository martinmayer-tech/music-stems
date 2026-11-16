# The stem separation service. Build the CPU image with `docker build .`.
# Build the GPU image with `docker build --build-arg STEMS_EXTRA=gpu .`.
FROM python:3.12-slim

# The extra of audio-separator to install: cpu or gpu.
ARG STEMS_EXTRA=cpu
# Keep this pin equal to the separation extra in pyproject.toml. A test checks it.
ARG AUDIO_SEPARATOR_VERSION=0.48.0

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --uid 1000 stems \
    && mkdir /data /models \
    && chown stems:stems /data /models

WORKDIR /app
COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir ".[service]" "audio-separator[${STEMS_EXTRA}]==${AUDIO_SEPARATOR_VERSION}"

ENV PYTHONPATH=/app/src/stem-core:/app/src/stem-service:/app/src/stem-web \
    STEMS_HOST=0.0.0.0 \
    STEMS_PORT=8000 \
    STEMS_DATA_DIR=/data \
    STEMS_MODEL_DIR=/models

USER stems
EXPOSE 8000
VOLUME ["/data", "/models"]

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/', timeout=3)"]

CMD ["python", "-m", "stem_service"]
