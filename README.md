# AI Landing: CMS Backend + Frontend + DB

## Запуск одной командой

```bash
docker compose up --build
```

После старта поднимаются:

- `frontend` на `http://localhost:3000`
- `backend` на `http://localhost:8000`
- `db` (PostgreSQL, внутренний сервис)

## Что делает backend при старте

1. Применяет миграции.
2. Запускает `seed_from_frontend --if-empty`.
3. Стартует Gunicorn.

Сидер читает контент из `nuxt-app/data/siteData.ts`, импортирует изображения из `nuxt-app/public/images` в `backend/media` и переносит тексты policy-страниц из `nuxt-app/pages/*.vue`.

## Админка

- URL: `http://localhost:8000/admin/`

Создать суперпользователя:

```bash
docker compose exec backend python manage.py createsuperuser
```

## API

Основные endpoints:

- `GET /api/site/`
- `GET /api/site-data/`
- `GET /api/sections/header/`
- `GET /api/sections/hero/`
- `GET /api/sections/steps/`
- `GET /api/sections/reviews/`
- `GET /api/footer/`
- `GET /api/pages/privacy/`
- `GET /api/pages/offer/`
- `GET /api/pages/terms/`

## Ручной запуск сидера

```bash
docker compose exec backend python manage.py seed_from_frontend
```

Без перезаписи уже заполненной БД:

```bash
docker compose exec backend python manage.py seed_from_frontend --if-empty
```
