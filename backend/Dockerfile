FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_COLLECTSTATIC=0

RUN apt-get update \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt \
    && pip install --no-cache-dir gunicorn

COPY . /app

RUN addgroup --system django \
    && adduser --system --ingroup django --home /app django \
    && chown -R django:django /app

USER django

EXPOSE 8000

CMD ["sh", "/app/entrypoint.sh"]
