import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import Flask application
try:
    # Import the app from app.py (which is already initialized)
    from app import app as flask_app
except ImportError as e:
    logger.error(f"Error importing Flask application: {str(e)}")
    # If import fails, create a minimal app that returns an error
    from flask import Flask, render_template, request, jsonify, Response
    flask_app = Flask(__name__)
    
    @flask_app.route('/')
    def error_page():
        return Response("Application initialization error. Please check server logs.", status=500)

# Ensure the data directory exists for XML storage
data_dir = os.path.join(os.path.dirname(__file__), 'data')
if not os.path.exists(data_dir):
    try:
        os.makedirs(data_dir)
        logger.info("Created data directory")
    except Exception as e:
        logger.error(f"Error creating data directory: {str(e)}")

# For Vercel, we'll use app directly
app = flask_app

# Custom error handler for 500 errors
@app.errorhandler(500)
def server_error(e):
    logger.error(f"Server error: {str(e)}")
    return render_template('error.html', error="An internal server error occurred. Please try again later."), 500

# Custom error handler for 404 errors
@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', error="The page you're looking for doesn't exist."), 404

if __name__ == "__main__":
    # This block won't be used by Vercel but is helpful for local testing
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)