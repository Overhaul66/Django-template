# Salon Management Backend — Walkthrough

## ✅ Results

| Check | Status |
|---|---|
| `python manage.py check` | ✅ 0 issues |
| `python manage.py makemigrations` | ✅ All migrations generated |
| `python manage.py migrate` | ✅ All migrations applied |
| `pytest apps/ -v` | ✅ **7/7 tests passed** |

---

## Project Structure

```
salon/
├── apps/
│   ├── common/          # BaseModel, renderers, exception handler, seed command
│   ├── users/           # CustomUser, Customer, SalonManager, SalonEmployee
│   ├── salons/          # Salon, SalonImage, SalonService, BusinessHours
│   ├── employees/       # Manager-facing employee admin CRUD
│   ├── scheduling/      # EmployeeAvailability + on-demand schedule generation
│   ├── appointments/    # Appointment lifecycle + core scheduling engine
│   └── notifications/   # In-app notifications + Celery task
├── config/
│   ├── settings.py      # Full config (JWT, Spectacular, CORS, Celery)
│   ├── urls.py          # Root URL patterns + Swagger routes
│   └── celery.py        # Celery application
├── Dockerfile
├── docker-compose.yml   # PostgreSQL + Redis + Django + Celery worker + beat
├── local.env            # Local environment config (gitignored)
├── .env.example         # Committed env template
├── .gitignore
├── pytest.ini
└── requirements.txt
```

---

## Key Architecture Decisions

### Manager → Salon (ForeignKey)
A `SalonManager` can own **multiple** salons via `ForeignKey`. This was the key change from the original spec (OneToOne → ForeignKey).

### Service-Oriented Architecture
Business logic lives entirely in `services.py` files. Views only:
1. Validate input via serializers
2. Call service functions
3. Return responses

Queries live in `selectors.py`.

### Uniform API Response Format
All responses are wrapped by `ApiResponseRenderer`:
```json
{ "success": true, "message": "...", "data": {...} }
// errors:
{ "success": false, "message": "Validation failed.", "errors": {...} }
```

---

## API Endpoints Summary

### Auth — `/api/auth/`
| Method | Path | Description |
|---|---|---|
| `POST` | `/api/auth/register/` | Register (Customer, Manager, Employee) |
| `POST` | `/api/auth/login/` | JWT login |
| `POST` | `/api/auth/refresh/` | Refresh token |
| `POST` | `/api/auth/logout/` | Blacklist token |
| `POST` | `/api/auth/password/change/` | Change password |
| `POST` | `/api/auth/password/reset/` | Request reset token |
| `POST` | `/api/auth/password/reset/confirm/` | Confirm reset |

### Salons — `/api/salons/`
| Method | Path | Description |
|---|---|---|
| `GET` | `/api/salons/` | Browse salons (with filters) |
| `POST` | `/api/salons/` | Manager creates salon |
| `GET` | `/api/salons/me/` | Manager's owned salons |
| `PATCH` | `/api/salons/me/` | Update owned salon |
| `DELETE` | `/api/salons/me/` | Delete owned salon |
| `*` | `/api/services/` | CRUD for salon services |

### Employees — `/api/employees/`
| Method | Path | Description |
|---|---|---|
| `POST` | `/api/employees/` | Manager creates employee account |
| `GET` | `/api/employees/` | Manager lists their employees |
| `PATCH` | `/api/employees/{id}/` | Edit employee |
| `DELETE` | `/api/employees/{id}/` | Delete employee |
| `POST` | `/api/employees/{id}/reset-password/` | Reset employee password |

### Appointments — `/api/appointments/`
| Method | Path | Description |
|---|---|---|
| `POST` | `/api/appointments/` | Customer books appointment (auto-assigns employee) |
| `GET` | `/api/appointments/` | List own appointments (role-filtered) |
| `PATCH` | `/api/appointments/{id}/cancel/` | Cancel appointment |
| `GET` | `/api/manager/dashboard/` | Manager dashboard metrics |
| `GET` | `/api/my/appointments/` | Employee's assigned appointments |
| `PATCH` | `/api/my/appointments/{id}/status/` | Employee updates status |

### Schedule — `/api/my/schedule/`
| Method | Path | Description |
|---|---|---|
| `GET` | `/api/my/schedule/` | Employee's weekly schedule |

### Notifications — `/api/notifications/`
| Method | Path | Description |
|---|---|---|
| `GET` | `/api/notifications/` | User's notifications |
| `PATCH` | `/api/notifications/{id}/mark-read/` | Mark as read |

### API Docs
| Path | Description |
|---|---|
| `/api/docs/` | Swagger UI |
| `/api/redoc/` | ReDoc |
| `/api/schema/` | OpenAPI JSON schema |

---

## Scheduling Engine

The core scheduling logic in [services.py](file:///c:/Users/zumaw/Desktop/codes/project/salon/apps/appointments/services.py):

1. **Validates salon hours** — start/end time must fall within `BusinessHours` for the weekday
2. **Checks employee leave/break** — queries `EmployeeAvailability` for LEAVE/BREAK/BOOKED blocks
3. **Checks double bookings** — queries `Appointment` for PENDING/CONFIRMED/IN_PROGRESS overlaps
4. **Balances workload** — picks the employee with the fewest appointments on that date
5. **Creates BOOKED availability block** — atomically prevents any concurrent double booking

---

## How to Run

```bash
# Create and activate virtual env
python -m venv .env
.env\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Seed sample data
python manage.py seed_data

# Start dev server
python manage.py runserver

# Run tests
pytest apps/ -v
```

### With Docker
```bash
docker-compose up --build
```

> [!TIP]
> Visit **http://localhost:8000/api/docs/** for the interactive Swagger UI once the server is running.

---

## Seed Data Accounts

After running `python manage.py seed_data`:

| Role | Email | Password |
|---|---|---|
| Manager | `manager@salon.com` | `password123` |
| Employee (Glow & Co) | `john.stylist@salon.com` | `password123` |
| Employee (Gents Cut) | `bob.barber@salon.com` | `password123` |
| Customer | `customer1@gmail.com` | `password123` |


# Salon Management Backend — Walkthrough

## ✅ Results

| Check | Status |
|---|---|
| `python manage.py check` | ✅ 0 issues |
| `python manage.py makemigrations` | ✅ All migrations generated |
| `python manage.py migrate` | ✅ All migrations applied |
| `pytest apps/ -v` | ✅ **7/7 tests passed** |

---

## Project Structure

```
salon/
├── apps/
│   ├── common/          # BaseModel, renderers, exception handler, seed command
│   ├── users/           # CustomUser, Customer, SalonManager, SalonEmployee
│   ├── salons/          # Salon, SalonImage, SalonService, BusinessHours
│   ├── employees/       # Manager-facing employee admin CRUD
│   ├── scheduling/      # EmployeeAvailability + on-demand schedule generation
│   ├── appointments/    # Appointment lifecycle + core scheduling engine
│   └── notifications/   # In-app notifications + Celery task
├── config/
│   ├── settings.py      # Full config (JWT, Spectacular, CORS, Celery)
│   ├── urls.py          # Root URL patterns + Swagger routes
│   └── celery.py        # Celery application
├── Dockerfile
├── docker-compose.yml   # PostgreSQL + Redis + Django + Celery worker + beat
├── local.env            # Local environment config (gitignored)
├── .env.example         # Committed env template
├── .gitignore
├── pytest.ini
└── requirements.txt
```

---

## Key Architecture Decisions

### Manager → Salon (ForeignKey)
A `SalonManager` can own **multiple** salons via `ForeignKey`. This was the key change from the original spec (OneToOne → ForeignKey).

### Service-Oriented Architecture
Business logic lives entirely in `services.py` files. Views only:
1. Validate input via serializers
2. Call service functions
3. Return responses

Queries live in `selectors.py`.

### Uniform API Response Format
All responses are wrapped by `ApiResponseRenderer`:
```json
{ "success": true, "message": "...", "data": {...} }
// errors:
{ "success": false, "message": "Validation failed.", "errors": {...} }
```

---

## API Endpoints Summary

### Auth — `/api/auth/`
| Method | Path | Description |
|---|---|---|
| `POST` | `/api/auth/register/` | Register (Customer, Manager, Employee) |
| `POST` | `/api/auth/login/` | JWT login |
| `POST` | `/api/auth/refresh/` | Refresh token |
| `POST` | `/api/auth/logout/` | Blacklist token |
| `POST` | `/api/auth/password/change/` | Change password |
| `POST` | `/api/auth/password/reset/` | Request reset token |
| `POST` | `/api/auth/password/reset/confirm/` | Confirm reset |

### Salons — `/api/salons/`
| Method | Path | Description |
|---|---|---|
| `GET` | `/api/salons/` | Browse salons (with filters) |
| `POST` | `/api/salons/` | Manager creates salon |
| `GET` | `/api/salons/me/` | Manager's owned salons |
| `PATCH` | `/api/salons/me/` | Update owned salon |
| `DELETE` | `/api/salons/me/` | Delete owned salon |
| `*` | `/api/services/` | CRUD for salon services |

### Employees — `/api/employees/`
| Method | Path | Description |
|---|---|---|
| `POST` | `/api/employees/` | Manager creates employee account |
| `GET` | `/api/employees/` | Manager lists their employees |
| `PATCH` | `/api/employees/{id}/` | Edit employee |
| `DELETE` | `/api/employees/{id}/` | Delete employee |
| `POST` | `/api/employees/{id}/reset-password/` | Reset employee password |

### Appointments — `/api/appointments/`
| Method | Path | Description |
|---|---|---|
| `POST` | `/api/appointments/` | Customer books appointment (auto-assigns employee) |
| `GET` | `/api/appointments/` | List own appointments (role-filtered) |
| `PATCH` | `/api/appointments/{id}/cancel/` | Cancel appointment |
| `GET` | `/api/manager/dashboard/` | Manager dashboard metrics |
| `GET` | `/api/my/appointments/` | Employee's assigned appointments |
| `PATCH` | `/api/my/appointments/{id}/status/` | Employee updates status |

### Schedule — `/api/my/schedule/`
| Method | Path | Description |
|---|---|---|
| `GET` | `/api/my/schedule/` | Employee's weekly schedule |

### Notifications — `/api/notifications/`
| Method | Path | Description |
|---|---|---|
| `GET` | `/api/notifications/` | User's notifications |
| `PATCH` | `/api/notifications/{id}/mark-read/` | Mark as read |

### API Docs
| Path | Description |
|---|---|
| `/api/docs/` | Swagger UI |
| `/api/redoc/` | ReDoc |
| `/api/schema/` | OpenAPI JSON schema |

---

## Scheduling Engine

The core scheduling logic in [services.py](file:///c:/Users/zumaw/Desktop/codes/project/salon/apps/appointments/services.py):

1. **Validates salon hours** — start/end time must fall within `BusinessHours` for the weekday
2. **Checks employee leave/break** — queries `EmployeeAvailability` for LEAVE/BREAK/BOOKED blocks
3. **Checks double bookings** — queries `Appointment` for PENDING/CONFIRMED/IN_PROGRESS overlaps
4. **Balances workload** — picks the employee with the fewest appointments on that date
5. **Creates BOOKED availability block** — atomically prevents any concurrent double booking

---

## How to Run

```bash
# Create and activate virtual env
python -m venv .env
.env\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Seed sample data
python manage.py seed_data

# Start dev server
python manage.py runserver

# Run tests
pytest apps/ -v
```

### With Docker
```bash
docker-compose up --build
```

> [!TIP]
> Visit **http://localhost:8000/api/docs/** for the interactive Swagger UI once the server is running.

---

## Seed Data Accounts

After running `python manage.py seed_data`:

| Role | Email | Password |
|---|---|---|
| Manager | `manager@salon.com` | `password123` |
| Employee (Glow & Co) | `john.stylist@salon.com` | `password123` |
| Employee (Gents Cut) | `bob.barber@salon.com` | `password123` |
| Customer | `customer1@gmail.com` | `password123` |
