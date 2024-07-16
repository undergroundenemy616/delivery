FROM python:3.12-bullseye

#RUN apt-get clean && apt-get update && apt-get install -y locales
#RUN locale-gen ru_RU.UTF-8 && update-locale LANG=ru_RU.UTF-8
RUN apt update && apt install python3-pip -y

EXPOSE 8000

ENV app app
RUN apt-get update && \
    apt-get install -y locales && \
    apt-get install -y python-dev-is-python3 libldap2-dev libsasl2-dev libssl-dev librdkafka-dev netcat-openbsd && \
    echo ru_RU.UTF-8 UTF-8 >> /etc/locale.gen && \
    locale-gen && \
    python -m pip install poetry && \
    poetry config virtualenvs.create false

WORKDIR /app

COPY src/pyproject.toml src/poetry.lock ./
RUN python -m pip install --upgrade pip && poetry install --no-root --no-cache

COPY ./src .