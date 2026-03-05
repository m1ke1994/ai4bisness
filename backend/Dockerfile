FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_COLLECTSTATIC=0

# Устанавливаем Python-зависимости проекта.
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt \
    && pip install --no-cache-dir gunicorn

# Копируем исходный код backend.
COPY . /app

# Создаем пользователя без root-прав для запуска приложения.
RUN addgroup --system django \
    && adduser --system --ingroup django --home /app django \
    && chown -R django:django /app

USER django

EXPOSE 8000

# Запускаем collectstatic только при DJANGO_COLLECTSTATIC=1, затем стартуем gunicorn.
CMD ["sh", "-c", "if [ \"$DJANGO_COLLECTSTATIC\" = \"1\" ]; then python manage.py collectstatic --noinput; else echo \"Пропуск collectstatic: DJANGO_COLLECTSTATIC!=1\"; fi && gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120"]
