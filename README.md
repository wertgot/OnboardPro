# OnboardPro — Django REST API

Бэкенд системы онбординга сотрудников. Только API, SQLite, без Docker.

## Быстрый старт

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

API: `http://127.0.0.1:8000/`

## Демо-учётные записи

| Логин | Пароль | Роль |
|-------|--------|------|
| `hr@company.com` | `demo1234` | HR |
| `employee@company.com` | `demo1234` | Employee |
| `admin@demo.com` | `demo1234` | Admin |

## JWT

```http
POST /api/v1/auth/token/
{"username": "hr@company.com", "password": "demo1234"}

POST /api/v1/auth/token/refresh/
{"refresh": "<refresh_token>"}
```

Заголовок: `Authorization: Bearer <access_token>`

## Основные эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| GET/POST | `/api/v1/programs/` | Программы онбординга |
| GET/POST | `/api/v1/instances/` | Экземпляры онбординга |
| GET | `/api/v1/instances/{id}/` | BFF: детали с этапами и задачами |
| PATCH | `/api/v1/instances/{id}/tasks/{tid}/` | Отметить задачу выполненной |
| GET/POST | `/api/v1/documents/` | Документы |
| POST | `/api/v1/documents/{id}/sign/` | Подписать документ |
| GET | `/api/v1/documents/{id}/file/` | Скачать файл |
| GET/POST | `/api/v1/quizzes/` | Тесты |
| POST | `/api/v1/quizzes/{id}/attempt/` | Пройти тест |
| GET | `/api/v1/analytics/` | Аналитика (HR/Admin) |
| GET/PATCH | `/api/v1/users/` | Пользователи |
| GET | `/mobile/v1/my-tasks/?status=pending` | Задачи (мобайл) |
| PATCH | `/mobile/v1/my-tasks/{id}/` | `{"done": true}` |

Регистрация новой компании (без авторизации):

```http
POST /api/v1/auth/register/
{
  "company_name": "Acme",
  "company_slug": "acme",
  "username": "owner",
  "email": "owner@acme.com",
  "password": "secret"
}
```

## Структура приложений

- `accounts` — пользователи, JWT, мультиарендность (Company)
- `programs` — программы, этапы, задачи
- `instances` — экземпляры онбординга, прогресс
- `documents` — загрузка и подписание файлов
- `quizzes` — тесты и попытки
- `notifications` — email-уведомления
- `analytics` — сводки для HR
- `web_bff` — агрегированный ответ для веб-клиента
- `mobile_bff` — компактный API для мобильного клиента

## База данных

SQLite: `db.sqlite3` в корне проекта.
