# Deployment Guide

This document outlines strategies for deploying the Indian Nutrition Calculator to various hosting platforms.

## Option 1: Deploying to Heroku

### Prerequisites

- Heroku account
- Heroku CLI installed
- PostgreSQL add-on

### Steps

1. **Create a Procfile**:
   Create a file named `Procfile` in the root directory with the content:
   ```
   web: gunicorn main:app
   ```

2. **Create a runtime.txt**:
   Create a file named `runtime.txt` with the content:
   ```
   python-3.11.0
   ```

3. **Initialize Git repository**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

4. **Create a Heroku app**:
   ```bash
   heroku create your-app-name
   ```

5. **Add PostgreSQL database**:
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

6. **Set environment variables**:
   ```bash
   heroku config:set OPENAI_API_KEY=your_openai_api_key
   heroku config:set SESSION_SECRET=your_session_secret
   ```

7. **Deploy to Heroku**:
   ```bash
   git push heroku master
   ```

8. **Open the app**:
   ```bash
   heroku open
   ```

## Option 2: Deploying to AWS Elastic Beanstalk

### Prerequisites

- AWS account
- AWS CLI installed
- EB CLI installed

### Steps

1. **Initialize EB application**:
   ```bash
   eb init -p python-3.11 nutrition-calculator
   ```

2. **Create EB environment**:
   ```bash
   eb create nutrition-calculator-env
   ```

3. **Configure environment variables**:
   In the AWS Management Console, navigate to the Elastic Beanstalk service, select your environment, and add the following environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `DATABASE_URL`: Your RDS PostgreSQL connection string (create an RDS instance if needed)
   - `SESSION_SECRET`: Your session secret key

4. **Deploy the application**:
   ```bash
   eb deploy
   ```

5. **Open the application**:
   ```bash
   eb open
   ```

## Option 3: Deploying to Google Cloud Run

### Prerequisites

- Google Cloud account
- gcloud CLI installed
- Project created in Google Cloud

### Steps

1. **Build a Docker image**:
   Create a `Dockerfile` in the root directory:
   ```dockerfile
   FROM python:3.11-slim

   WORKDIR /app

   COPY . .

   RUN pip install flask==2.3.3 flask-sqlalchemy==3.0.5 gunicorn==23.0.0 openai==1.11.0 psycopg2-binary==2.9.9 python-dotenv==1.0.0 email-validator==2.1.0

   ENV PORT=8080

   CMD exec gunicorn --bind :$PORT main:app
   ```

2. **Build and push the image**:
   ```bash
   gcloud builds submit --tag gcr.io/your-project-id/nutrition-calculator
   ```

3. **Deploy to Cloud Run**:
   ```bash
   gcloud run deploy nutrition-calculator \
     --image gcr.io/your-project-id/nutrition-calculator \
     --platform managed \
     --allow-unauthenticated \
     --region us-central1 \
     --set-env-vars="OPENAI_API_KEY=your_openai_api_key,DATABASE_URL=your_cloud_sql_connection_string,SESSION_SECRET=your_session_secret"
   ```

4. **Set up Cloud SQL**:
   Create a PostgreSQL instance in Cloud SQL and connect it to your Cloud Run service.

## Important Deployment Considerations

### 1. Database Migration

Before deploying to production, ensure the database schema is properly migrated:

```bash
# If using Flask-Migrate
flask db upgrade
```

### 2. Security

- Ensure all sensitive information is stored in environment variables
- Use HTTPS for all production deployments
- Set proper Content Security Policy headers
- Implement rate limiting to prevent abuse

### 3. Monitoring and Logging

- Set up error tracking (Sentry, Rollbar, etc.)
- Configure logging and monitoring
- Set up database performance monitoring
- Create alerts for system issues

### 4. Scaling

- Configure auto-scaling based on traffic
- Optimize database queries for performance
- Consider caching frequently requested data
- Use a CDN for static assets

### 5. Backup Strategy

- Set up regular database backups
- Implement automated backup verification
- Create a disaster recovery plan

## Continuous Integration/Continuous Deployment (CI/CD)

Consider setting up a CI/CD pipeline using:
- GitHub Actions
- GitLab CI/CD
- Jenkins
- CircleCI
- Travis CI