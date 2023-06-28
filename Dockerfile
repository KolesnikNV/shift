FROM python:3.11-slim-buster


RUN apt-get update && \
    apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 -


WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-root


COPY shift /app/shift


RUN pip install uvicorn


CMD ["uvicorn", "shift.main:app", "--host", "0.0.0.0", "--port", "8000"]
