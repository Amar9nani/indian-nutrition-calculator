# Project Dependencies

This document lists all dependencies required for the Indian Nutrition Calculator project.

## Python Packages

```
flask==2.3.3
flask-sqlalchemy==3.0.5
gunicorn==23.0.0
openai==1.11.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
email-validator==2.1.0
```

## Database

- PostgreSQL (Version 14 or higher recommended)

## External APIs

- OpenAI API (GPT-4o model for recipe extraction)

## Environment Variables

The following environment variables need to be set for the application to work properly:

- `OPENAI_API_KEY`: Your OpenAI API key
- `DATABASE_URL`: PostgreSQL connection string (format: postgresql://username:password@hostname:port/database_name)
- `SESSION_SECRET`: Secret key for Flask session

## Frontend Libraries (CDN)

- Bootstrap 5.3.0
- Bootstrap Icons 1.10.5
- Chart.js (latest version)