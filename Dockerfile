FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

COPY REQUIREMENTS.txt ./REQUIREMENTS.txt
RUN pip install --no-cache-dir -r REQUIREMENTS.txt

RUN groupadd --system app && useradd --system --gid app --home-dir /app app

COPY --chown=app:app app.py ./app.py
COPY --chown=app:app system_health ./system_health
COPY --chown=app:app static ./static

USER app

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
