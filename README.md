# OnboardPro

Система онбординга сотрудников: Django REST API + React + Docker.

## Docker (рекомендуется)

```bash
cp .env.example .env   # при необходимости отредактируйте
docker compose up --build
```

Откройте **http://localhost:8080** — Nginx раздаёт фронтенд и проксирует API.

> Порт 8080 выбран, чтобы не конфликтовать с другим сервисом на :80 (IIS/WSL и т.п.).

| Сервис   | Назначение                          |
|----------|-------------------------------------|
| nginx    | React static + reverse proxy (порт 80)|
| django   | API + Gunicorn                      |
| postgres | PostgreSQL 16                       |

Демо-аккаунты (создаются при старте `django`):

| Логин | Пароль | Роль |
|-------|--------|------|
| `hr@company.com` | `demo1234` | HR |
| `employee@company.com` | `demo1234` | Employee |
| `admin@demo.com` | `demo1234` | Admin |

## Локальная разработка без Docker

### Backend (SQLite)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Фронтенд: **http://localhost:5173** (прокси `/api` → Django :8000).

## Архитектура

```
┌─────────────┐     ┌─────────────┐     ┌──────────────┐
│   Browser   │────▶│    nginx    │────▶│    django    │
│  React SPA  │     │  :80        │     │  Gunicorn    │
└─────────────┘     └─────────────┘     └──────┬───────┘
                        /api, /mobile          │
                                                 ▼
                                          ┌──────────────┐
                                          │  PostgreSQL  │
                                          └──────────────┘
```

## API

- `POST /api/v1/auth/token/` — JWT
- `GET /api/v1/programs/` — программы
- `GET /api/v1/instances/{id}/` — BFF с этапами и задачами
- `PATCH /api/v1/instances/{id}/tasks/{tid}/` — отметить задачу
- `GET /api/v1/analytics/` — аналитика (HR)
- `GET /mobile/v1/my-tasks/` — мобильный BFF

## Структура

- `accounts`, `programs`, `instances`, … — Django-приложения
- `frontend/` — React (Vite + TypeScript)
- `nginx/` — конфиг и multi-stage Dockerfile (React build + nginx)
- `docker-compose.yml` — оркестрация
