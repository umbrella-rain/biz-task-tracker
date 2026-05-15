<h1 align="center">Biz Task Tracker</h1>

<p align="center">
    <em>Async-first task tracking system for small businesses. Built for performance, designed for clarity.</em>
</p>

---

**Source Code**: <https://github.com/umbrella-rain/biz-task-tracker>

**Live API Demo**: <https://storied-rugelach-0a138f.netlify.app/>

---

Biz Task Tracker is a modern, asynchronous CRM-style API for managing clients, tasks, and team members. Built with Python and FastAPI, it leverages a fully async stack for high throughput and clean architecture.

The key features are:

* **Async-first**: Built on FastAPI and SQLAlchemy with `asyncpg` for non-blocking I/O end-to-end.
* **Secure**: JWT authentication with `bcrypt` password hashing. All endpoints protected by default.
* **Role-based access**: Admin / Manager / Worker roles with permission checks at the route level.
* **Clean architecture**: Repository Pattern separates business logic from data access.
* **Validated**: Strict request/response schemas with Pydantic v2.
* **Containerized**: Production-ready Dockerfile and Docker Compose setup.
* **Tested**: Pytest coverage for core endpoints with async test client.
* **Standards-based**: Auto-generated OpenAPI documentation (Swagger UI + ReDoc).

---

## Requirements

* Python 3.11+
* Docker & Docker Compose (recommended)
* PostgreSQL 15+ (if running without Docker)

## Installation

### With Docker (recommended)

​```bash
git clone https://github.com/umbrella-rain/biz-task-tracker.git
cd biz-task-tracker
docker-compose up --build
​```

### Without Docker

​```bash
pip install -r requirements.txt
cd backend
uvicorn main:app --reload
​```

## Example

### Register a user

​```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@biz.com", "password": "secret", "role": "admin"}'
​```

### Login and get a token

​```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@biz.com", "password": "secret"}'
​```

Response:

​```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
​```

### Create a task

​```bash
curl -X POST http://localhost:8000/tasks \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Call client", "description": "Discuss Q4 contract", "status": "new"}'
​```

## Interactive API Docs

Once the server is running, open your browser at <http://localhost:8000/docs> for the auto-generated **Swagger UI**, or <http://localhost:8000/redoc> for the **ReDoc** alternative.

## Running Tests

​```bash
cd backend
pytest -v
​```

## Project Structure

​```
biz-task-tracker/
├── backend/
│   ├── main.py          # FastAPI app and routes
│   ├── models.py        # SQLAlchemy ORM models
│   ├── schemas.py       # Pydantic schemas
│   ├── repository.py    # Data access layer
│   ├── database.py      # Async engine and session
│   ├── security.py      # JWT and password hashing
│   └── test_main.py     # Pytest test suite
├── frontend/            # HTML/CSS dashboard (WIP)
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
​```

## Roadmap

- [x] Async REST API with FastAPI
- [x] Repository Pattern
- [x] JWT authentication with role-based access
- [x] Docker & Docker Compose setup
- [x] Pytest coverage for core endpoints

## Contact

**LinkedIn**: [Danylo Blidar](https://pl.linkedin.com/in/danylo-blidar-4416bb365)

## License

This project is licensed under the terms of the MIT license.
