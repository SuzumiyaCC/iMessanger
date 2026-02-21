# iMessanger / ХрюшинИТ Corporate Portal

Django-портал для внутренних новостей, блога и каталога сотрудников.

## Stack
- Django (latest stable in `5.x`)
- Django REST Framework
- PostgreSQL
- Docker Compose

## Run (Docker)
1. `cp .env.example .env`
2. `docker compose up --build`
3. Open: `http://localhost:8000`
4. API root: `http://localhost:8000/api/`

## Local dev (no Docker)
1. `python3 -m venv .venv && source .venv/bin/activate`
2. `pip install -r requirements.txt`
3. `python manage.py migrate`
4. `python manage.py runserver`

## Initial API endpoints
- `GET/POST /api/employees/`
- `GET/POST /api/posts/`
TOOL_EXEC_WRITE_OK

## Auth API endpoints
- `POST /api/auth/login/` (username/password -> token)
- `GET /api/auth/me/` (Bearer token required)

## News UI improvements
- Filter by title (`q`) and author (`author`)
- Pagination for news feed
