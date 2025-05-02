# Vercel Deployment Guide

This document provides detailed information about how the Vercel deployment works and how to troubleshoot any issues.

## How Vercel Deployment Works

Vercel is a serverless platform that's ideal for deploying web applications. Here's how our application has been configured to work with Vercel:

### 1. Serverless Architecture

- **API Routes**: The main entry point is `api/index.py` which loads our Flask application
- **Statelessness**: Vercel functions are stateless, so we use in-memory storage instead of files

### 2. Key Files

- **vercel.json**: Configures the build settings and routes for Vercel
- **api/index.py**: The serverless function entry point
- **api/requirements.txt**: Python dependencies specifically for Vercel
- **xml_storage.py**: Includes special handling for Vercel's read-only filesystem

### 3. Environment Variables

- **VERCEL**: Set to "1" to detect the Vercel environment
- **DISABLE_OPENAI**: Set to "1" to reduce complexity in the serverless environment
- **OPENAI_API_KEY**: Optional - you can add this in the Vercel dashboard

## Troubleshooting

### Common Issues

1. **"Internal Server Error" on First Deployment**
   - **Solution**: Wait a few minutes for the deployment to fully initialize
   - **Alternative**: Try deploying again

2. **Missing Static Assets**
   - **Solution**: Ensure static files are correctly referenced using Flask's `url_for` function
   - **Alternative**: Check that static files are included in your Git repository

3. **OpenAI Integration Not Working**
   - **Solution**: By default, OpenAI is disabled in Vercel. To enable it:
     - Remove `"DISABLE_OPENAI": "1"` from vercel.json
     - Add your OpenAI API key in the Vercel dashboard under Environment Variables
     - Redeploy the application

### Vercel Logs

To check logs for troubleshooting:

1. Go to your Vercel dashboard
2. Select your project
3. Click on "Deployments"
4. Select the most recent deployment
5. Click on "Functions"
6. Click on the function (typically "api/index.py")
7. View the logs to see any errors

## Advanced Configuration

### Custom Domains

To use a custom domain:

1. Go to your Vercel dashboard
2. Select your project
3. Navigate to "Settings" > "Domains"
4. Add your custom domain
5. Follow the instructions to configure DNS settings

### Environment Variables

To add environment variables:

1. Go to your Vercel dashboard
2. Select your project
3. Navigate to "Settings" > "Environment Variables"
4. Add key-value pairs as needed
5. Redeploy your application

### Updating Your Deployment

To update your deployment after making changes:

1. Commit your changes to Git
2. Run `vercel` again, or
3. Set up GitHub integration to deploy automatically

## Performance Optimization

1. **Cold Start Times**: Vercel functions can have "cold start" times. Keep your code minimal.

2. **API Response Size**: Large responses can increase costs. Keep responses concise.

3. **Database Connections**: Use connection pooling for database connections.

## Security Best Practices

1. Use environment variables for sensitive information
2. Implement proper CORS settings
3. Use authentication where necessary
4. Validate user input
5. Use HTTPS

## Limitations to Be Aware Of

1. **Read-Only Filesystem**: Cannot write to the filesystem
2. **Function Execution Time**: Limited to 10 seconds for Hobby plans
3. **Request Body Size**: Limited to 4.5MB
4. **Statelessness**: Each function invocation is independent

## Further Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Vercel CLI Commands](https://vercel.com/docs/cli)
- [Python on Vercel](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Environment Variables](https://vercel.com/docs/projects/environment-variables)