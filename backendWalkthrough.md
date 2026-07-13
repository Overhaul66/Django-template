# Django API Template Walkthrough

## What changed

This project has been reduced to a reusable Django starter foundation.

- The app-specific salon modules were removed from the default project wiring.
- The project now loads a minimal common app and a generic health-check endpoint.
- The default URL structure is ready for you to add your own apps.

## Current structure

```text
project/
├── apps/
│   └── common/          # Shared base models, views, and seed command
├── config/
│   ├── settings.py      # Core Django/DRF configuration
│   ├── urls.py          # Root URL patterns
│   └── celery.py        # Celery app entrypoint
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## What to do next

1. Add your own app under apps/
2. Register it in settings.py if needed
3. Define your domain routes in its own urls.py
4. Replace the health endpoint with real business logic

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
- Swagger UI: /api/docs/
- OpenAPI schema: /api/schema/
