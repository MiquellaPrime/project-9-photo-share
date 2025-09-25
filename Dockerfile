FROM python:3.11.11-slim-bookworm

ENV PHYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN pip install --upgrade wheel "poetry==2.1.3"

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY . .

RUN chmod +x prestart.sh

ENTRYPOINT ["./prestart.sh"]
