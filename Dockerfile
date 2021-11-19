FROM python:3.8-alpine

ENV POETRY_VERSION=1.1.0

RUN apk update --no-cache
RUN apk add --update --no-cache gcc g++ libxslt-dev libressl-dev musl-dev openssl-dev libffi-dev


RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

COPY . /app

RUN python manage.py migrate
