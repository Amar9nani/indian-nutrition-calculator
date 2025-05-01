import os
import logging
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, flash
from nutrition_calculator import NutritionCalculator
from xml_storage import XMLStorage

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "indian_nutrition_calculator_secret_key"  # Default secret key

# Add a default OpenAI API key (this is just a placeholder)
os.environ.setdefault("OPENAI_API_KEY", "sk-placeholder-api-key")
# If you have a real key, you can set it in your environment or replace it here

# Initialize XML storage for nutrition history
xml_storage = XMLStorage()

# Initialize nutrition calculator
nutrition_calculator = NutritionCalculator()

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/calculate', methods=['GET', 'POST'])
def calculate_nutrition():
    """Calculate nutrition for a dish"""
    try:
        if request.method == 'POST':
            dish_name = request.form.get('dish_name')
        else:  # GET request
            dish_name = request.args.get('dish_name')
            
        if not dish_name:
            flash('Please enter a dish name', 'error')
            return render_template('index.html')
        
        logger.info(f"Calculating nutrition for: {dish_name}")
        result = nutrition_calculator.calculate_nutrition(dish_name)
        
        if not result:
            flash('Could not calculate nutrition for this dish. Please try another dish.', 'error')
            return render_template('index.html')
        
        # Add dish_name to the result for storage
        result['dish_name'] = dish_name
        
        # Save the result to XML storage
        try:
            xml_storage.save_nutrition_request(result)
            logger.info(f"Saved nutrition data for {dish_name} to XML storage")
        except Exception as storage_error:
            logger.error(f"Error saving to XML storage: {str(storage_error)}")
            # Continue processing even if storage save fails
            
        return render_template('result.html', result=result, dish_name=dish_name)
        
    except Exception as e:
        logger.error(f"Error calculating nutrition: {str(e)}")
        flash(f"An error occurred: {str(e)}", 'error')
        return render_template('index.html')

@app.route('/api/calculate', methods=['GET', 'POST'])
def api_calculate_nutrition():
    """API endpoint to calculate nutrition for a dish"""
    try:
        if request.method == 'POST':
            data = request.get_json() if request.is_json else request.form
            dish_name = data.get('dish_name')
        else:  # GET request
            dish_name = request.args.get('dish_name')
        
        if not dish_name:
            return jsonify({"error": "Dish name is required"}), 400
            
        result = nutrition_calculator.calculate_nutrition(dish_name)
        
        if not result:
            return jsonify({"error": "Could not calculate nutrition for this dish"}), 404
        
        # Add dish_name to the result for storage
        result['dish_name'] = dish_name
        
        # Save the result to XML storage
        try:
            xml_storage.save_nutrition_request(result)
            logger.info(f"Saved nutrition data for {dish_name} to XML storage (API request)")
        except Exception as storage_error:
            logger.error(f"Error saving to XML storage (API request): {str(storage_error)}")
            # Continue processing even if storage save fails
            
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/history')
def view_history():
    """View history of nutrition calculations"""
    try:
        # Fetch all records from XML storage
        nutrition_history = xml_storage.get_all_nutrition_requests()
        return render_template('history.html', history=nutrition_history)
    except Exception as e:
        logger.error(f"Error fetching history: {str(e)}")
        flash(f"An error occurred while fetching history: {str(e)}", 'error')
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
