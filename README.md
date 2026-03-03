# Flask PostgreSQL Application

Production-ready Flask application with PostgreSQL database, designed for corporate environments.

## 🏗️ Architecture

This application follows best practices for Flask applications in enterprise environments:

- **Application Factory Pattern**: Modular and testable application structure
- **Blueprint-based Routing**: Organized route handlers with versioned APIs
- **Service Layer**: Business logic separated from route handlers
- **Structured Logging**: JSON-formatted logs for centralized logging systems
- **Request Tracing**: Unique request IDs for tracking across services
- **Health Checks**: Kubernetes/Docker-ready liveness and readiness probes
- **Security Headers**: CORS, CSP, HSTS, and other security protections
- **Input Validation**: Marshmallow schemas for request validation
- **Database Migrations**: Flask-Migrate for schema version control
- **Containerized**: Docker and Docker Compose for consistent deployments
- **Reverse Proxy**: Traefik integration with SSL/TLS

## 📁 Project Structure

```
dev_app_flask_postgresdb/
├── app/
│   ├── __init__.py              # Application factory
│   ├── extensions.py            # Flask extensions (db, migrate)
│   ├── errors.py                # Error handlers
│   ├── models/                  # SQLAlchemy models
│   │   └── __init__.py
│   ├── routes/                  # Blueprint route handlers
│   │   ├── __init__.py
│   │   ├── main.py             # Main routes
│   │   ├── health.py           # Health check endpoints
│   │   └── api/                # Versioned API routes
│   │       └── __init__.py     # API v1 routes
│   ├── schemas/                 # Marshmallow validation schemas
│   │   └── __init__.py
│   ├── services/                # Business logic layer
│   │   └── __init__.py
│   ├── middleware/              # Request/response middleware
│   │   ├── __init__.py
│   │   ├── logging_middleware.py
│   │   ├── request_id.py
│   │   └── security.py
│   ├── utils/                   # Helper functions
│   │   └── __init__.py
│   ├── static/                  # Static files (CSS, JS, images)
│   └── templates/               # Jinja2 templates
├── docker-compose/
│   ├── devapp_base.yml         # Docker Compose configuration
│   └── build/
│       └── PYTHON_DOCKERFILE    # Application Dockerfile
├── tests/                       # Test suite
│   ├── conftest.py             # Pytest configuration
│   ├── unit/                   # Unit tests
│   └── integration/            # Integration tests
├── migrations/                  # Database migrations (generated)
├── logs/                        # Application logs
├── config.py                    # Configuration management
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
├── .env                         # Environment variables (not in git)
├── .gitignore                   # Git ignore rules
└── .dockerignore               # Docker ignore rules
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Git
- Network access (for corporate proxy settings)

### Installation

1. **Clone the repository** (or navigate to the project directory):
   ```bash
   cd /srv/containers/dev_app_flask_postgresdb
   ```

2. **Configure environment variables**:
   Edit `.env` file with your settings:
   ```bash
   # Project name
   COMPOSE_PROJECT_NAME=devapp_python_prostgres

   # Flask configuration
   FLASK_ENV=development
   FLASK_DEBUG=1

   # Database configuration
   POSTGRES_DATABASE=devappdb
   POSTGRES_USER=dbappuser
   POSTGRES_PASSWORD=your_secure_password
   POSTGRES_HOST=db
   POSTGRES_PORT=5432

   # Proxy settings (if applicable)
   HTTP_PROXY=http://proxy.example.com:3128
   HTTPS_PROXY=http://proxy.example.com:3128
   NO_PROXY=localhost,127.0.0.1,10.0.0.0/8
   ```

3. **Start the application**:
   ```bash
   docker compose up -d
   ```

4. **Check application status**:
   ```bash
   docker compose ps
   docker compose logs -f web
   ```

### Access the Application

- **Main Application**: http://devapp.bpkornyekitvsz.birosagiad.hu (via Traefik)
- **Local Access**: http://localhost:5000 (if exposed)
- **Health Check**: http://localhost:5000/health/live
- **API**: http://localhost:5000/api/v1/users

## 🔧 Development

### Database Migrations

Initialize migrations (first time only):
```bash
docker compose exec web flask db init
```

Create a new migration after model changes:
```bash
docker compose exec web flask db migrate -m "Description of changes"
```

Apply migrations:
```bash
docker compose exec web flask db upgrade
```

Rollback last migration:
```bash
docker compose exec web flask db downgrade
```

### Running Tests

Run all tests:
```bash
docker compose exec web pytest
```

Run with coverage:
```bash
docker compose exec web pytest --cov=app --cov-report=html
```

Run specific test file:
```bash
docker compose exec web pytest tests/unit/test_services.py
```

### Accessing the Database

Connect to PostgreSQL:
```bash
docker compose exec db psql -U dbappuser -d devappdb
```

### Viewing Logs

Application logs:
```bash
docker compose logs -f web
```

Database logs:
```bash
docker compose logs -f db
```

### Development Workflow

1. Make code changes in your editor
2. Application auto-reloads (Gunicorn with `--reload` flag)
3. Run tests to verify changes
4. Create migration if models changed
5. Commit changes to Git

## 📡 API Documentation

### Health Endpoints

#### Liveness Probe
```http
GET /health/live
```
Returns 200 if application is running.

#### Readiness Probe
```http
GET /health/ready
```
Returns 200 if application is ready to serve traffic (DB connected).

#### Application Info
```http
GET /health/info
```
Returns application metadata (version, environment, etc.).

### API v1 Endpoints

All API endpoints are prefixed with `/api/v1`.

#### List Users
```http
GET /api/v1/users?page=1&per_page=20
```

#### Get User
```http
GET /api/v1/users/{id}
```

#### Create User
```http
POST /api/v1/users
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com"
}
```

#### Update User
```http
PUT /api/v1/users/{id}
Content-Type: application/json

{
  "email": "newemail@example.com"
}
```

#### Delete User
```http
DELETE /api/v1/users/{id}
```

### Response Format

Success response:
```json
{
  "status": "success",
  "data": { ... },
  "message": "Optional message"
}
```

Error response:
```json
{
  "status": "error",
  "message": "Error description",
  "errors": { ... }
}
```

## 🔒 Security

### Implemented Security Features

- **CORS Configuration**: Controlled cross-origin access
- **Security Headers**: 
  - X-Frame-Options (clickjacking protection)
  - X-Content-Type-Options (MIME sniffing protection)
  - X-XSS-Protection (XSS filter)
  - Strict-Transport-Security (HTTPS enforcement)
  - Content-Security-Policy (resource loading control)
- **Request ID Tracking**: Unique IDs for request tracing
- **Structured Logging**: JSON logs for security auditing
- **Input Validation**: Marshmallow schema validation
- **SQL Injection Protection**: SQLAlchemy ORM
- **Environment Variables**: Sensitive data not in code

### Production Security Checklist

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Use strong database passwords
- [ ] Enable HTTPS/TLS (handled by Traefik)
- [ ] Configure CORS for specific origins only
- [ ] Review and update CSP headers
- [ ] Implement authentication/authorization
- [ ] Enable rate limiting
- [ ] Set up monitoring and alerting
- [ ] Regular security updates
- [ ] Database backups

## 🏢 Corporate Environment Features

### Proxy Support

Application supports corporate proxy environments. Configure in `.env`:
```env
HTTP_PROXY=http://proxy.company.com:3128
HTTPS_PROXY=http://proxy.company.com:3128
NO_PROXY=localhost,127.0.0.1,.company.com
```

### Logging

Structured JSON logging for integration with centralized logging systems (ELK, Splunk, etc.):
```json
{
  "asctime": "2026-03-03T10:30:45.123Z",
  "name": "app",
  "levelname": "INFO",
  "message": "Request completed",
  "method": "GET",
  "path": "/api/v1/users",
  "status_code": 200,
  "duration_ms": 45.23,
  "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Monitoring

Health check endpoints compatible with:
- Kubernetes/OpenShift liveness and readiness probes
- Docker HEALTHCHECK
- Load balancer health checks
- Monitoring systems (Prometheus, Nagios, etc.)

## 📦 Dependencies

### Core Dependencies

- **Flask 3.0.0**: Web framework
- **SQLAlchemy**: ORM and database toolkit
- **PostgreSQL**: Production database
- **Gunicorn**: WSGI HTTP server
- **Flask-Migrate**: Database migration tool
- **Flask-CORS**: CORS support
- **Marshmallow**: Data validation and serialization
- **python-json-logger**: Structured logging

See [requirements.txt](requirements.txt) for complete list.

## 🐛 Troubleshooting

### Container won't start

Check logs:
```bash
docker compose logs web
```

Verify environment variables:
```bash
docker compose config
```

### Database connection issues

Check database is healthy:
```bash
docker compose ps
docker compose logs db
```

Test connection:
```bash
docker compose exec web python -c "from app import create_app; from app.extensions import db; app = create_app(); app.app_context().push(); db.session.execute('SELECT 1')"
```

### Import errors in VS Code

Import errors are cosmetic - packages are installed in container, not on host. To fix:
1. Install Python packages locally, OR
2. Use VS Code Remote - Containers extension

### Application not accessible

1. Check Traefik proxy is running
2. Verify DNS/hosts file configuration
3. Check firewall rules
4. Review Traefik labels in docker-compose.yml

## 🔄 Deployment

### Production Considerations

1. **Environment Variables**:
   - Set `FLASK_ENV=production`
   - Set `FLASK_DEBUG=0`
   - Use strong `SECRET_KEY`
   - Secure database credentials

2. **Database**:
   - Use managed PostgreSQL service or dedicated server
   - Configure regular backups
   - Set up replication for high availability

3. **Application Server**:
   - Increase Gunicorn workers: `--workers 4`
   - Remove `--reload` flag
   - Set appropriate timeouts

4. **Monitoring**:
   - Set up application monitoring (New Relic, Datadog, etc.)
   - Configure log aggregation
   - Set up alerting

5. **Security**:
   - Review all security headers
   - Enable HTTPS only
   - Implement authentication
   - Set up WAF if available

## 📝 Git Workflow

Current branch:
```bash
git branch
```

Commit changes:
```bash
git add .
git commit -m "Description of changes"
git push origin main
```

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Write/update tests
4. Run test suite
5. Create pull request

## 📄 License

[Add your license information here]

## 📧 Support

For issues or questions, contact: [Add your contact information]

---

**Last Updated**: March 3, 2026
**Version**: 1.0.0
