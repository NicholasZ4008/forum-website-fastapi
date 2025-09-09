# Forum API Server (FastAPI)

A lightweight, efficient FastAPI server for managing email subscriptions for The Forum University.

## Overview

The Forum API is a RESTful web service built with FastAPI that provides endpoints for managing email subscriptions. It uses PostgreSQL as the database and features automatic API documentation, email validation, and CSV export functionality.

## Features

- Email subscription management (CRUD operations)
- Email validation using Pydantic
- CORS support for cross-origin requests
- PostgreSQL database integration with SQLAlchemy
- Automatic API documentation with Swagger UI and ReDoc
- CSV export functionality
- Health check endpoint
- Database connection testing
- Docker support

## Prerequisites

- Python 3.8 or later
- PostgreSQL database
- pip (Python package manager)

## Setup

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/forum-api-fastapi.git
   cd forum-api-fastapi
   ```

2. Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. Set up your PostgreSQL database and update the `DATABASE_URL` in `.env`

## Running the API

### Development
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 3000
```

### Production
```bash
uvicorn main:app --host 0.0.0.0 --port 3000
```

The API will be available at:
- http://localhost:3000

## API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:3000/docs
- **ReDoc**: http://localhost:3000/redoc
- **OpenAPI JSON**: http://localhost:3000/openapi.json

## Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t forum-api .
   ```

2. Run the container:
   ```bash
   docker run -d --name forum-api -p 3000:3000 --env-file .env forum-api
   ```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /emails  | Get all email subscriptions |
| GET    | /emails/{id} | Get a specific email subscription by ID |
| POST   | /emails  | Add a new email subscription |
| PUT    | /emails/{id} | Update an existing email subscription |
| DELETE | /emails/{id} | Remove an email subscription |
| GET    | /export  | Export all emails as CSV |
| GET    | /health  | Health check endpoint |
| GET    | /test-connect | Test database connection |

## Request & Response Examples

### POST /emails

Request:
```json
{
  "email_name": "user@example.com"
}
```

Response (201 Created):
```json
{
  "id": 1,
  "email_name": "user@example.com"
}
```

### PUT /emails/{id}

Request:
```json
{
  "email_name": "newemail@example.com"
}
```

Response: 204 No Content

### Error Response Example

```json
{
  "detail": "Email already registered"
}
```

## Database Schema

```sql
CREATE TABLE emails (
    id SERIAL PRIMARY KEY,
    email_name VARCHAR UNIQUE NOT NULL
);
```

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string (required)

## CORS Configuration

The API is configured to accept requests from:
- http://localhost:3000 (development frontend)
- https://localhost:3000 (development frontend with HTTPS)
- http://theforumuniversity.com (production frontend)
- https://theforumuniversity.com (production frontend with HTTPS)
- http://www.theforumuniversity.com (production with www)
- https://www.theforumuniversity.com (production with www and HTTPS)
- http://api.theforumuniversity.com (API subdomain)
- https://api.theforumuniversity.com (API subdomain with HTTPS)

## Key Differences from .NET Version

1. **Email Validation**: Uses Pydantic's `EmailStr` for automatic email validation
2. **Automatic Documentation**: FastAPI generates interactive docs automatically
3. **Type Hints**: Full Python type hint support for better IDE experience
4. **Dependency Injection**: Uses FastAPI's dependency injection for database sessions
5. **Async Support**: Built-in async support for better performance
6. **Error Handling**: Structured error responses with HTTP status codes

## Development Features

- Hot reload with `--reload` flag
- Automatic request/response validation
- Built-in testing support with pytest
- Type checking support

## Testing

You can test the API using:
1. The built-in Swagger UI at `/docs`
2. curl commands
3. Any HTTP client like Postman or Insomnia

Example curl command:
```bash
curl -X POST "http://localhost:3000/emails" \
     -H "Content-Type: application/json" \
     -d '{"email_name": "test@example.com"}'
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

[MIT License](LICENSE)