# Vercel Deployment Configuration

This document explains how the Vercel deployment is set up for the Indian Nutrition Calculator.

## Files Added/Modified for Vercel Deployment

1. **api/index.py**: Serverless entry point for Vercel
2. **api/requirements.txt**: Dependencies for Vercel's Python runtime
3. **vercel.json**: Configuration for Vercel deployment
4. **xml_storage.py**: Modified to use in-memory storage in Vercel environment
5. **.vercelignore**: Specifies files to exclude from deployment
6. **.gitignore-vercel**: Git ignore file specifically for Vercel
7. **app.py**: Added health check endpoint
8. **VERCEL_GUIDE.md**: Detailed guide for troubleshooting Vercel deployments

## Key Features

- **Environment Detection**: Automatically detects when running in Vercel
- **In-Memory Storage**: Uses memory instead of file system in serverless environment
- **Static Asset Handling**: Properly configured for static assets
- **Health Check Endpoint**: Available at `/health` to verify deployment
- **Error Handling**: Robust error handling specific to Vercel
- **OpenAI Integration**: Disabled by default but can be enabled

## Deployment Steps

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Deploy the Application**:
   ```bash
   vercel
   ```

3. **Verify Deployment**:
   - Check the `/health` endpoint
   - Test the main application functionality

## Environment Variables

- **VERCEL**: Set to "1" to indicate Vercel environment
- **DISABLE_OPENAI**: Set to "1" by default, can be removed to enable OpenAI
- **OPENAI_API_KEY**: Add this in the Vercel dashboard if you want to use OpenAI

## How It Works

1. When deployed to Vercel, the serverless function in `api/index.py` is the entry point
2. This loads the Flask application from `app.py`
3. XML storage is automatically switched to in-memory mode
4. Static assets are served directly by Vercel

## Troubleshooting

If you encounter issues, please refer to the detailed [VERCEL_GUIDE.md](VERCEL_GUIDE.md).