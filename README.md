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

## Auth API endpoints
- `POST /api/auth/login/` (username/password -> token)
- `GET /api/auth/me/` (Bearer token required)

## Employees API (mobile integration)
- `GET /api/employees/` — paginated catalog with `count/next/previous/page/page_size/results`
- `GET /api/employees/?q=<text>` — search by full name, position or email
- `GET /api/employees/?department=<name>` — filter by department
- `GET /api/employees/?q=<text>&department=<name>&page=2&page_size=10` — combined filters + pagination
- `GET /api/employees/<id>/quick-contact/` — быстрый контакт (phone/email/messenger + приоритетный CTA link)
- API возвращает только активных сотрудников (`is_active=true`) для клиентского каталога.

Example request:
```bash
curl -H "Authorization: Token <TOKEN>" \
  "http://localhost:8000/api/employees/?q=иванов&department=hr&page=1&page_size=10"
```

Example response envelope:
```json
{
  "count": 42,
  "next": "http://localhost:8000/api/employees/?page=2&page_size=10",
  "previous": null,
  "page": 1,
  "page_size": 10,
  "results": [
    {
      "id": 1,
      "full_name": "Иван Иванов",
      "department": "HR"
    }
  ]
}
```

Quick-contact example:
```json
{
  "id": 1,
  "full_name": "Иван Иванов",
  "quick_contact": {
    "phone": "+79990001122",
    "email": "ivanov@example.com",
    "messenger": "@ivanov",
    "messenger_link": "https://t.me/ivanov"
  },
  "cta": {
    "type": "phone",
    "preferred_channel": "phone",
    "link": "tel:+79990001122"
  }
}
```

## News UI improvements
- Filter by title (`q`) and author (`author`)
- Pagination for news feed

## News API filters
- `GET /api/posts/?q=<title>`
- `GET /api/posts/?author=<author>`
- `GET /api/posts/?is_published=true|false`

## Observability
- `GET /api/health/` -> service metadata + DB status.

## Audit trail
- File: `logs/audit.log` (JSONL)
- Trigger: POST/PUT/PATCH/DELETE on `/api/*`
- Fields: `ts`, `method`, `path`, `status`, `user`

## QA smoke-run (Docker Compose, reproducible)
```bash
# 1) build + run
cp .env.example .env
docker compose up --build -d

# 2) apply migrations
docker compose exec web python manage.py migrate

# 3) create demo user for token auth (if missing)
docker compose exec web python manage.py shell -c "from django.contrib.auth import get_user_model; U=get_user_model(); U.objects.filter(username='qa').exists() or U.objects.create_user('qa', password='qa123456')"

# 4) get token
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login/ \
  -H 'Content-Type: application/json' \
  -d '{"username":"qa","password":"qa123456"}' | python3 -c 'import sys,json; print(json.load(sys.stdin)["token"])')

# 5) smoke checks
curl -s "http://localhost:8000/api/employees/?q=ИВАН&department=РАЗРАБОТ&page=1&page_size=5" \
  -H "Authorization: Token $TOKEN"

curl -s "http://localhost:8000/api/employees/1/quick-contact/" \
  -H "Authorization: Token $TOKEN"

# 6) teardown
docker compose down
```
