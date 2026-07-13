# Django API Template

A clean, reusable Django starter project for building API-first applications.

## What is included

- Django + Django REST Framework setup
- Generic custom user model and profile endpoint
- JWT authentication configuration
- OpenAPI/Swagger documentation
- CORS and environment-based settings
- A basic health-check endpoint
- A simple seed command placeholder
- MinIO and boto3 dependencies for object storage integration

## Project structure

```text
apps/
├── common/     # Shared base logic, views, and seed command
└── users/      # Generic custom user model and profile endpoint

config/
├── settings.py
├── urls.py
└── celery.py
```

## Quick start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Useful endpoints

- GET /api/health/
- GET /api/users/me/
- Swagger UI: /api/docs/
- OpenAPI schema: /api/schema/

## Next steps

- Add your own app under apps/
- Extend the generic user model as needed
- Wire in your own business logic and serializers
- Configure storage, database, and auth settings for your project
