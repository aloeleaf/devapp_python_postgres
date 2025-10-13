# dev_app_flask_postgresdb - Architecture Documentation

## Overview

This is a containerized Flask web application with PostgreSQL database, orchestrated using Docker Compose and exposed via Traefik reverse proxy.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Traefik Reverse Proxy                   │
│          (devapp.bpkornyekitvsz.birosagiad.hu)             │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTPS (443)
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   Docker Network: traefikproxy              │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   Docker Network: app-network               │
│                                                             │
│  ┌────────────────────────┐      ┌────────────────────────┐│
│  │   Flask Web Service    │      │  PostgreSQL Database   ││
│  │  (devapp-web)          │◄────►│  (devapp-db)          ││
│  │                        │      │                        ││
│  │  - Python 3.9          │      │  - PostgreSQL 16       ││
│  │  - Flask 3.0.0         │      │  - Alpine Linux        ││
│  │  - Gunicorn 21.2.0     │      │  - Port: 5432          ││
│  │  - Port: 5000          │      │  - Volume: pg-data     ││
│  │  - Auto-reload enabled │      │  - Health checks       ││
│  └────────────────────────┘      └────────────────────────┘│
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Project Structure

```
dev_app_flask_postgresdb/
│
├── app/
│   └── main.py                      # Flask application entry point
│
├── docker-compose/
│   ├── build/
│   │   ├── PYTHON_DOCKERFILE        # Dockerfile for Flask container
│   │   └── requirements.txt         # Python dependencies
│   │
│   └── devapp_base.yml              # Docker Compose configuration
│
├── .env                             # Environment variables (not in git)
├── README.md                        # User guide
├── ARCHITECTURE.md                  # This file
└── .gitignore                       # Git ignore rules

Docker Volumes:
└── pg-data/                         # PostgreSQL persistent data storage
```

## Technology Stack

### Web Application Layer
- **Python**: 3.9-slim
- **Framework**: Flask 3.0.0
- **WSGI Server**: Gunicorn 21.2.0
- **Database Driver**: psycopg2-binary 2.9.9

### Database Layer
- **Database**: PostgreSQL 16 (Alpine)
- **Data Persistence**: Docker named volume (`pg-data`)
- **Health Monitoring**: pg_isready checks

### Infrastructure Layer
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Reverse Proxy**: Traefik (external)
- **Networking**: Bridge network (app-network) + Traefik network

## Component Details

### 1. Flask Web Service (`web`)

**Container Name**: `devapp-web`

**Build Process**:
- Base image: `python:3.9-slim`
- Installs system dependencies: gcc, libpq-dev, postgresql-client
- Installs Python packages from `requirements.txt`
- Supports HTTP/HTTPS proxy configuration

**Runtime Configuration**:
- Runs Gunicorn with auto-reload for development
- Binds to `0.0.0.0:5000`
- Hot-reload enabled via volume mount of `main.py`
- Waits for database health check before starting

**Environment Variables**:
```
POSTGRES_HOST=db
POSTGRES_DATABASE=devappdb
POSTGRES_USER=dbappuser
POSTGRES_PASSWORD=p1ssw2rd
POSTGRES_PORT=5432
FLASK_APP=app/main.py
FLASK_ENV=development
FLASK_DEBUG=1
```

**Exposed Endpoints**:
- `/` - Hello World page
- `/db_test` - Database connection test (JSON response)

### 2. PostgreSQL Database Service (`db`)

**Container Name**: `devapp-db`

**Image**: `postgres:16-alpine`

**Data Persistence**:
- Volume: `pg-data` mounted at `/var/lib/postgresql/data`
- Survives container restarts and removals

**Health Check**:
- Command: `pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DATABASE}`
- Interval: 10 seconds
- Timeout: 5 seconds
- Retries: 5
- Start period: 10 seconds

**Environment Variables**:
```
POSTGRES_DB=devappdb
POSTGRES_USER=dbappuser
POSTGRES_PASSWORD=p1ssw2rd
```

## Network Architecture

### Internal Network: `app-network`
- **Type**: Bridge network
- **Purpose**: Communication between Flask and PostgreSQL
- **Isolation**: Services are not directly accessible from host

### External Network: `traefikproxy`
- **Type**: External network
- **Purpose**: Integration with Traefik reverse proxy
- **Access**: Provides HTTPS access to the application

## Request Flow

```
1. User Request
   └─► https://devapp.bpkornyekitvsz.birosagiad.hu

2. Traefik Reverse Proxy
   ├─► SSL/TLS termination
   ├─► Route matching
   └─► Forward to devapp-web:5000

3. Gunicorn (WSGI Server)
   ├─► Receives HTTP request
   ├─► Passes to Flask app
   └─► Returns response

4. Flask Application
   ├─► Routes request to handler
   ├─► Connects to PostgreSQL (if needed)
   │   └─► psycopg2 → devapp-db:5432
   └─► Returns JSON/HTML response

5. Response Flow
   └─► Flask → Gunicorn → Traefik → User
```

## Database Connection Flow

```python
# Connection with retry logic
1. Flask app attempts connection
2. If failed, retry up to 5 times
3. Wait 5 seconds between retries
4. Connection parameters from environment:
   - host: db (Docker DNS)
   - database: devappdb
   - user: dbappuser
   - password: p1ssw2rd
   - port: 5432
```

## Security Considerations

### Current Implementation
- ✅ Database credentials in `.env` file (not in git)
- ✅ HTTPS via Traefik
- ✅ Isolated Docker networks
- ✅ Non-root user in containers (Python image default)
- ✅ Minimal base images (Alpine for PostgreSQL)

### Recommendations for Production
- 🔒 Use Docker secrets instead of `.env` for sensitive data
- 🔒 Implement database connection pooling
- 🔒 Add rate limiting
- 🔒 Enable Flask security headers
- 🔒 Regular security updates for base images
- 🔒 Implement application-level authentication
- 🔒 Add SQL injection protection (use parameterized queries)
- 🔒 Enable PostgreSQL SSL connections

## Deployment Process

### Development Deployment
```bash
# 1. Build and start services
docker-compose -f docker-compose/devapp_base.yml up --build -d

# 2. View logs
docker-compose -f docker-compose/devapp_base.yml logs -f

# 3. Stop services
docker-compose -f docker-compose/devapp_base.yml down
```

### Production Deployment
```bash
# 1. Build without cache
docker-compose -f docker-compose/devapp_base.yml build --no-cache

# 2. Start in detached mode
docker-compose -f docker-compose/devapp_base.yml up -d

# 3. Verify health
docker-compose -f docker-compose/devapp_base.yml ps
```

## Monitoring and Debugging

### Container Status
```bash
docker-compose -f docker-compose/devapp_base.yml ps
```

### Application Logs
```bash
# Web service logs
docker logs devapp-web -f

# Database logs
docker logs devapp-db -f

# All services
docker-compose -f docker-compose/devapp_base.yml logs -f
```

### Database Access
```bash
# Connect to PostgreSQL
docker exec -it devapp-db psql -U dbappuser -d devappdb

# View tables
\dt

# Exit
\q
```

### Health Checks
- Database: Automatic via `pg_isready`
- Web App: Access `/db_test` endpoint for connection status

## Scalability Considerations

### Current Limitations
- Single web container
- Single database instance
- No load balancing (handled by Traefik)
- No database replication

### Scaling Options
1. **Horizontal Scaling (Web)**:
   - Add more web containers
   - Traefik handles load balancing automatically

2. **Database Scaling**:
   - Implement read replicas
   - Use connection pooling (pgBouncer)
   - Consider managed PostgreSQL services

3. **Caching**:
   - Add Redis for session storage
   - Implement application-level caching

## Backup and Recovery

### Database Backup
```bash
# Backup
docker exec devapp-db pg_dump -U dbappuser devappdb > backup.sql

# Restore
docker exec -i devapp-db psql -U dbappuser devappdb < backup.sql
```

### Volume Backup
```bash
# Backup volume data
docker run --rm \
  -v pg-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/pg-data-backup.tar.gz /data
```

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `COMPOSE_PROJECT_NAME` | devapp | Prefix for container names |
| `POSTGRES_HOST` | db | Database hostname |
| `POSTGRES_DATABASE` | devappdb | Database name |
| `POSTGRES_USER` | dbappuser | Database user |
| `POSTGRES_PASSWORD` | p1ssw2rd | Database password |
| `POSTGRES_PORT` | 5432 | Database port |
| `FLASK_APP` | app/main.py | Flask entry point |
| `FLASK_ENV` | development | Flask environment |
| `FLASK_DEBUG` | 1 | Debug mode |
| `HTTP_PROXY` | - | HTTP proxy URL |
| `HTTPS_PROXY` | - | HTTPS proxy URL |
| `NO_PROXY` | - | Proxy exclusions |

## Troubleshooting

### Common Issues

**1. Database connection fails**
- Check if database is healthy: `docker-compose ps`
- Verify environment variables in `.env`
- Check logs: `docker logs devapp-db`

**2. Module not found errors**
- Rebuild containers: `docker-compose build --no-cache`
- Verify `requirements.txt` is correct

**3. Port conflicts**
- Check if port 5432 or 5000 is already in use
- Modify ports in `docker-compose/devapp_base.yml`

**4. Traefik routing issues**
- Verify Traefik network exists: `docker network ls`
- Check Traefik configuration
- Verify labels in docker-compose file

## Future Enhancements

- [ ] Add database migrations (Alembic/Flask-Migrate)
- [ ] Implement proper ORM (SQLAlchemy)
- [ ] Add API documentation (Swagger/OpenAPI)
- [ ] Implement logging aggregation
- [ ] Add application metrics (Prometheus)
- [ ] Create automated tests
- [ ] Add CI/CD pipeline
- [ ] Implement database seeding
- [ ] Add environment-specific configs (dev/staging/prod)

---

**Last Updated**: October 13, 2025  
**Version**: 1.0  
**Maintainer**: Development Team