import os
import logging
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from nutrition_calculator import NutritionCalculator

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the model
class NutritionRequest(db.Model):
    """Model for storing nutrition calculation requests and results"""
    __tablename__ = 'nutrition_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    dish_name = db.Column(db.String(255), nullable=False)
    dish_type = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Nutrition values
    calories = db.Column(db.Float)
    protein = db.Column(db.Float)
    carbs = db.Column(db.Float)
    fat = db.Column(db.Float)
    fiber = db.Column(db.Float)
    
    # JSON data
    ingredients_json = db.Column(db.Text)
    serving_size_json = db.Column(db.Text)
    
    def __repr__(self):
        return f"<NutritionRequest(dish_name='{self.dish_name}', dish_type='{self.dish_type}')>"

# Initialize database
with app.app_context():
    db.create_all()

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
        
        # Save the result to the database
        try:
            nutrition_request = NutritionRequest(
                dish_name=dish_name,
                dish_type=result.get('dish_type', ''),
                calories=result.get('nutrition_per_serving', {}).get('calories', 0),
                protein=result.get('nutrition_per_serving', {}).get('protein', 0),
                carbs=result.get('nutrition_per_serving', {}).get('carbs', 0),
                fat=result.get('nutrition_per_serving', {}).get('fat', 0),
                fiber=result.get('nutrition_per_serving', {}).get('fiber', 0),
                ingredients_json=json.dumps(result.get('ingredients', [])),
                serving_size_json=json.dumps(result.get('serving_size', {}))
            )
            db.session.add(nutrition_request)
            db.session.commit()
            logger.info(f"Saved nutrition data for {dish_name} to database")
        except Exception as db_error:
            logger.error(f"Error saving to database: {str(db_error)}")
            # Continue processing even if database save fails
            
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
        
        # Save the result to the database
        try:
            nutrition_request = NutritionRequest(
                dish_name=dish_name,
                dish_type=result.get('dish_type', ''),
                calories=result.get('nutrition_per_serving', {}).get('calories', 0),
                protein=result.get('nutrition_per_serving', {}).get('protein', 0),
                carbs=result.get('nutrition_per_serving', {}).get('carbs', 0),
                fat=result.get('nutrition_per_serving', {}).get('fat', 0),
                fiber=result.get('nutrition_per_serving', {}).get('fiber', 0),
                ingredients_json=json.dumps(result.get('ingredients', [])),
                serving_size_json=json.dumps(result.get('serving_size', {}))
            )
            db.session.add(nutrition_request)
            db.session.commit()
            logger.info(f"Saved nutrition data for {dish_name} to database (API request)")
        except Exception as db_error:
            logger.error(f"Error saving to database (API request): {str(db_error)}")
            # Continue processing even if database save fails
            
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/history')
def view_history():
    """View history of nutrition calculations"""
    try:
        # Fetch all records from the database, ordered by most recent first
        nutrition_history = NutritionRequest.query.order_by(NutritionRequest.created_at.desc()).all()
        return render_template('history.html', history=nutrition_history)
    except Exception as e:
        logger.error(f"Error fetching history: {str(e)}")
        flash(f"An error occurred while fetching history: {str(e)}", 'error')
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
