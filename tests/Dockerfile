FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /src

RUN pip install pip 'poetry==1.8.5'

RUN poetry config virtualenvs.create false --local

COPY ../poetry.lock pyproject.toml ./

RUN poetry install
