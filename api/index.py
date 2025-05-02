import os
import sys
import logging
from flask import Flask, Response, redirect, url_for, render_template

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Before importing any application code, set up the environment
# Mark that we're in Vercel environment
os.environ["VERCEL"] = "1"

# By default, disable OpenAI to reduce complexity
os.environ["DISABLE_OPENAI"] = "1" 

# Required for some Flask applications
os.environ["FLASK_APP"] = "app.py"

# Ensure data directory exists (will be ignored in read-only filesystem)
try:
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(__file__), '../data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        logger.info(f"Created data directory at {data_dir}")
except Exception as e:
    logger.warning(f"Could not create data directory: {str(e)}")

# Import the Flask app from app.py
try:
    # Add parent directory to path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # Now import the app
    from app import app
    logger.info("Successfully imported Flask application")
except Exception as e:
    logger.error(f"Error importing app: {str(e)}")
    # Create a minimal Flask app for error reporting
    app = Flask(__name__)
    
    @app.route('/')
    def error():
        return Response(
            "Error initializing application. Please check server logs.\n" + 
            f"Error details: {str(e)}",
            status=500
        )
    
    @app.route('/health')
    def health():
        return {"status": "error", "message": str(e)}

# This is needed for Vercel serverless deployment
# The file is named index.py and is in the api directory
# This allows Vercel to find and use this Flask app as the entrypoint