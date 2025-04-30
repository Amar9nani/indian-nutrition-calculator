import os
import logging
import json
from flask import Flask, render_template, request, jsonify, flash
from nutrition_calculator import NutritionCalculator

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")

# Initialize nutrition calculator
nutrition_calculator = NutritionCalculator()

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate_nutrition():
    """Calculate nutrition for a dish"""
    try:
        dish_name = request.form.get('dish_name')
        if not dish_name:
            flash('Please enter a dish name', 'error')
            return render_template('index.html')
        
        logger.info(f"Calculating nutrition for: {dish_name}")
        result = nutrition_calculator.calculate_nutrition(dish_name)
        
        if not result:
            flash('Could not calculate nutrition for this dish. Please try another dish.', 'error')
            return render_template('index.html')
            
        return render_template('result.html', result=result, dish_name=dish_name)
        
    except Exception as e:
        logger.error(f"Error calculating nutrition: {str(e)}")
        flash(f"An error occurred: {str(e)}", 'error')
        return render_template('index.html')

@app.route('/api/calculate', methods=['POST'])
def api_calculate_nutrition():
    """API endpoint to calculate nutrition for a dish"""
    try:
        data = request.get_json()
        dish_name = data.get('dish_name')
        
        if not dish_name:
            return jsonify({"error": "Dish name is required"}), 400
            
        result = nutrition_calculator.calculate_nutrition(dish_name)
        
        if not result:
            return jsonify({"error": "Could not calculate nutrition for this dish"}), 404
            
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
