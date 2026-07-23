<div align="center">

# 📝 python-notes-api

**A production-ready REST API for managing personal notes with JWT authentication.**

[![CI](https://github.com/yourusername/python-notes-api/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/python-notes-api/actions/workflows/ci.yml)
[![Lint](https://github.com/yourusername/python-notes-api/actions/workflows/lint.yml/badge.svg)](https://github.com/yourusername/python-notes-api/actions/workflows/lint.yml)
[![Docker](https://github.com/yourusername/python-notes-api/actions/workflows/docker.yml/badge.svg)](https://github.com/yourusername/python-notes-api/actions/workflows/docker.yml)
[![Security](https://github.com/yourusername/python-notes-api/actions/workflows/security.yml/badge.svg)](https://github.com/yourusername/python-notes-api/actions/workflows/security.yml)
[![codecov](https://codecov.io/gh/yourusername/python-notes-api/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/python-notes-api)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Docker Usage](#docker-usage)
- [Docker Compose Usage](#docker-compose-usage)
- [API Documentation](#api-documentation)
- [Authentication](#authentication)
- [Testing](#testing)
- [GitHub Actions](#github-actions)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [Roadmap](#roadmap)
- [License](#license)

---

## 🎯 Overview

`python-notes-api` is a fully-featured, production-ready REST API built with Python 3.12 and Flask. It provides a secure platform for users to create, read, update, and delete personal notes. The API implements JWT-based authentication, comprehensive input validation, structured logging, and is fully containerized with Docker.

This project serves as a **reference implementation** demonstrating modern Python backend development practices including:
- Clean architecture with separation of concerns
- Type-safe ORM with SQLAlchemy 2.0
- Automated testing with >90% code coverage
- Continuous Integration/Continuous Deployment (CI/CD) with GitHub Actions
- Container security scanning with Trivy
- Code quality enforcement with Ruff and Black

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Client / Browser                        │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/HTTPS
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    Nginx / Load Balancer                     │
│              (SSL termination, rate limiting)                │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    Gunicorn WSGI Server                      │
│              (4 workers, production-ready)                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    Flask Application                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   Routes    │  │    Auth     │  │     Validation      │ │
│  │  (REST API) │  │  (JWT)      │  │   (Marshmallow)     │ │
│  └──────┬──────┘  └─────────────┘  └─────────────────────┘ │
│         │                                                   │
│  ┌──────┴───────────────────────────────────────────────┐   │
│  │              SQLAlchemy ORM (SQLite)                  │   │
│  │  ┌─────────────┐  ┌───────────────────────────────┐  │   │
│  │  │   User      │  │            Note               │  │   │
│  │  │  - id (PK)  │  │  - id (PK)                   │  │   │
│  │  │  - username │  │  - title                     │  │   │
│  │  │  - email    │  │  - content                   │  │   │
│  │  │  - password │  │  - owner_id (FK -> User.id)  │  │   │
│  │  │  - created  │  │  - created_at                │  │   │
│  │  └─────────────┘  │  - updated_at                │  │   │
│  │                   └───────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## ✨ Features

- **🔐 JWT Authentication** — Secure Bearer token authentication for all note endpoints
- **📝 Full CRUD Operations** — Create, Read, Update, and Delete notes
- **👤 User Management** — Registration and login with bcrypt password hashing
- **🛡️ Input Validation** — Strict request validation using Marshmallow schemas
- **📊 Health Monitoring** — Built-in health check endpoint for container orchestration
- **🐳 Docker Ready** — Multi-stage Dockerfile with non-root user and health checks
- **🧪 Comprehensive Testing** — Unit and integration tests with >90% coverage
- **🔍 Security Scanning** — Automated vulnerability scanning with Bandit and Trivy
- **📈 CI/CD Pipeline** — GitHub Actions for linting, testing, building, and releasing
- **📦 Container Registry** — Automatic publishing to GitHub Container Registry (GHCR)

---

## 🛠️ Tech Stack

| Technology      | Version | Purpose                          |
|-----------------|---------|----------------------------------|
| Python          | 3.12    | Runtime language                 |
| Flask           | 3.0.3   | Web framework                    |
| SQLAlchemy      | 3.1.1   | ORM and database abstraction     |
| Flask-JWT-Extended | 4.6.0 | JWT authentication               |
| Marshmallow     | 3.21.3  | Request/response serialization   |
| Werkzeug        | 3.0.3   | WSGI utilities & password hashing|
| Gunicorn        | 23.0.0  | Production WSGI server           |
| SQLite          | —       | Embedded database                |
| Pytest          | 8.3.2   | Testing framework                |
| Ruff            | 0.5.6   | Fast Python linter               |
| Black           | 24.8.0  | Code formatter                   |
| MyPy            | 1.11.1  | Static type checking             |
| Bandit          | 1.7.9   | Security linter                  |
| Trivy           | —       | Container vulnerability scanner  |
| Docker          | —       | Containerization                 |

---

## 📁 Project Structure

```
python-notes-api/
├── .github/
│   └── workflows/
│       ├── ci.yml          # Run tests and generate coverage
│       ├── docker.yml      # Build image and run health checks
│       ├── lint.yml        # Ruff, Black, and MyPy checks
│       ├── release.yml     # Create releases and publish to GHCR
│       └── security.yml    # Bandit and Trivy security scans
├── app/
│   ├── __init__.py         # Package initialization
│   ├── config.py           # Environment configurations
│   ├── database.py         # SQLAlchemy setup
│   ├── models.py           # User and Note ORM models
│   ├── schemas.py          # Marshmallow validation schemas
│   ├── auth.py             # Authentication utilities
│   ├── routes.py           # API endpoint definitions
│   ├── utils.py            # Logging and helper functions
│   └── main.py             # Application factory
├── tests/
│   ├── conftest.py         # Pytest fixtures
│   ├── test_api.py         # Integration tests for CRUD
│   ├── test_auth.py        # Authentication tests
│   ├── test_database.py    # Database operation tests
│   └── test_models.py      # Model unit tests
├── Dockerfile              # Multi-stage Docker build
├── docker-compose.yml      # Production compose file
├── docker-compose.dev.yml  # Development compose file
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
├── pyproject.toml          # Project metadata & tool configs
├── pytest.ini             # Pytest configuration
├── .coveragerc            # Coverage settings
├── .gitignore             # Git ignore rules
├── .dockerignore          # Docker ignore rules
├── .env.example           # Environment variable template
├── LICENSE                # MIT License
└── README.md              # This file
```

---

## 🚀 Installation

### Prerequisites

- Python 3.12+
- pip
- Docker (optional)
- Docker Compose (optional)

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/python-notes-api.git
   cd python-notes-api
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your preferred values
   ```

5. **Run the application:**
   ```bash
   flask --app app.main run --host 0.0.0.0 --port 5000
   ```

6. **Verify it's running:**
   ```bash
   curl http://localhost:5000/api/v1/health
   ```

---

## 🐳 Docker Usage

### Build the Image

```bash
docker build -t python-notes-api:latest .
```

### Run the Container

```bash
docker run -d \
  --name notes-api \
  -p 5000:5000 \
  -e SECRET_KEY=your-secret-key \
  -e JWT_SECRET_KEY=your-jwt-secret \
  -e FLASK_ENV=production \
  python-notes-api:latest
```

### Check Logs

```bash
docker logs -f notes-api
```

### Stop and Remove

```bash
docker stop notes-api && docker rm notes-api
```

---

## 🐳 Docker Compose Usage

### Production Mode

```bash
docker-compose up -d
```

The API will be available at `http://localhost:5000`.

### Development Mode (with hot-reload)

```bash
docker-compose -f docker-compose.dev.yml up
```

### View Logs

```bash
docker-compose logs -f
```

### Stop Services

```bash
docker-compose down
```

### Remove Volumes

```bash
docker-compose down -v
```

---

## 📖 API Documentation

### Base URL

```
http://localhost:5000/api/v1
```

### Endpoints

| Method | Endpoint          | Auth Required | Description              |
|--------|-------------------|---------------|--------------------------|
| GET    | `/health`         | No            | Health check             |
| POST   | `/register`       | No            | Register a new user      |
| POST   | `/login`          | No            | Authenticate and get JWT |
| GET    | `/notes`          | Yes           | List all user notes      |
| GET    | `/notes/{id}`     | Yes           | Get a specific note      |
| POST   | `/notes`          | Yes           | Create a new note        |
| PUT    | `/notes/{id}`     | Yes           | Update an existing note  |
| DELETE | `/notes/{id}`     | Yes           | Delete a note            |

---

## 🔐 Authentication

### Register a New User

```bash
curl -X POST http://localhost:5000/api/v1/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

**Response:**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "created_at": "2024-01-15T10:30:00+00:00"
  }
}
```

### Login

```bash
curl -X POST http://localhost:5000/api/v1/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securepassword123"
  }'
```

**Response:**
```json
{
  "message": "Login successful",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer"
}
```

### Access Protected Endpoints

Include the token in the `Authorization` header:

```bash
curl -X GET http://localhost:5000/api/v1/notes \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

---

## 📝 API Examples

### Create a Note

```bash
curl -X POST http://localhost:5000/api/v1/notes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "Project Ideas",
    "content": "1. Build a CLI tool\n2. Learn Rust\n3. Contribute to open source"
  }'
```

### List All Notes

```bash
curl -X GET http://localhost:5000/api/v1/notes \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Get a Specific Note

```bash
curl -X GET http://localhost:5000/api/v1/notes/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Update a Note

```bash
curl -X PUT http://localhost:5000/api/v1/notes/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "Updated Project Ideas",
    "content": "New content here"
  }'
```

### Delete a Note

```bash
curl -X DELETE http://localhost:5000/api/v1/notes/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## 🧪 Testing

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=app --cov-report=term-missing --cov-report=html
```

### Run Specific Test File

```bash
pytest tests/test_auth.py -v
```

### Run in Watch Mode (requires pytest-watch)

```bash
ptw
```

### Coverage Report

After running tests with coverage, open the HTML report:

```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

---

## 🔄 GitHub Actions

This repository includes a comprehensive CI/CD pipeline:

| Workflow     | Trigger                          | Purpose                              |
|--------------|----------------------------------|--------------------------------------|
| `ci.yml`     | Push/PR to main, develop         | Run pytest with coverage reporting   |
| `lint.yml`   | Push/PR to main, develop         | Ruff, Black, and MyPy checks         |
| `docker.yml` | Push/PR to main, develop         | Build image and verify health check  |
| `security.yml` | Push/PR + weekly cron           | Bandit code scan + Trivy container scan |
| `release.yml` | Git tag push (`v*`)             | Create GitHub Release + publish to GHCR |

---

## 🚀 Deployment

### Deploy to a VPS / Cloud Server

1. Clone the repository on your server
2. Copy `.env.example` to `.env` and configure production secrets
3. Run with Docker Compose:
   ```bash
   docker-compose up -d
   ```
4. Set up a reverse proxy (Nginx or Traefik) with SSL

### Deploy to Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: notes-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: notes-api
  template:
    metadata:
      labels:
        app: notes-api
    spec:
      containers:
        - name: api
          image: ghcr.io/yourusername/python-notes-api:latest
          ports:
            - containerPort: 5000
          env:
            - name: SECRET_KEY
              valueFrom:
                secretKeyRef:
                  name: api-secrets
                  key: secret-key
          livenessProbe:
            httpGet:
              path: /api/v1/health
              port: 5000
            initialDelaySeconds: 10
            periodSeconds: 30
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Ensure all tests pass (`pytest`)
- Maintain >90% code coverage
- Run linting before committing (`ruff check . && black --check .`)
- Write clear, descriptive commit messages

---

## 🗺️ Roadmap

- [x] JWT Authentication
- [x] CRUD API for Notes
- [x] Docker & Docker Compose
- [x] GitHub Actions CI/CD
- [x] Security scanning (Bandit + Trivy)
- [x] Code coverage >90%
- [ ] OpenAPI/Swagger documentation
- [ ] Rate limiting
- [ ] Pagination for list endpoints
- [ ] Role-based access control (RBAC)
- [ ] PostgreSQL support
- [ ] Redis caching layer
- [ ] API versioning strategy
- [ ] Prometheus metrics endpoint

---

## 📸 Screenshots

> Placeholder for architecture diagrams, API testing screenshots, and CI/CD pipeline visuals.

```
[Architecture Diagram Placeholder]
[Postman Collection Screenshot Placeholder]
[GitHub Actions Pipeline Screenshot Placeholder]
[Coverage Report Screenshot Placeholder]
```

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ using Python 3.12, Flask, and modern DevOps practices.**

</div>
