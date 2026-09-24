FROM public.ecr.aws/docker/library/python:3.11-slim-bullseye

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /statlib
COPY . .

RUN pip install --no-cache-dir tox coverage

CMD ["tox"]
