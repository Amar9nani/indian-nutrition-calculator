# Indian Nutrition Calculator

A Python-based nutrition calculator for Indian dishes that estimates nutritional values per standard serving based on dish name.

![Indian Nutrition Calculator](generated-icon.png)

## About This Project

The Indian Nutrition Calculator is a web application developed as part of an assignment for VYB AI. It addresses the unique challenge of calculating nutrition for Indian recipes, which often lack standardized measurements and nutritional information compared to Western counterparts.

## Features

- **Instant Nutrition Calculation**: Enter any Indian dish name and get nutrition information
- **AI-Powered Recipe Extraction**: Uses OpenAI API to extract recipe information for dishes
- **Standardized Measurements**: Converts traditional Indian measurements to standard units
- **Nutrition Analysis**: Calculates calories, protein, carbs, fat, and fiber per standard serving
- **Visual Display**: Charts for easy interpretation of nutritional information
- **JSON Output**: Provides structured data output for integration with other applications
- **Calculation History**: Stores previous calculations in a database for future reference

## How It Works

1. **Recipe Extraction**: The application fetches a standardized recipe for the entered dish name
2. **Ingredient Mapping**: Maps ingredients to a nutrition database
3. **Quantity Conversion**: Converts traditional Indian measurements to standardized weights
4. **Dish Type Identification**: Identifies the type of dish to determine appropriate serving size
5. **Nutrition Calculation**: Calculates nutrition values based on ingredient quantities
6. **Per-Serving Standardization**: Normalizes nutrition to standard serving sizes for each dish type

## Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: PostgreSQL
- **API Integration**: OpenAI API for recipe extraction
- **Visualization**: Chart.js for nutrition data visualization
- **Data Processing**: Custom algorithms for ingredient mapping and measurement conversion

## Getting Started

### Prerequisites

- Python 3.11 or higher
- PostgreSQL database
- OpenAI API key

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/indian-nutrition-calculator.git
   cd indian-nutrition-calculator
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```
   export OPENAI_API_KEY=your_openai_api_key
   export DATABASE_URL=your_postgresql_connection_string
   ```

4. Run the application:
   ```
   gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
   ```

5. Open your browser and navigate to `http://localhost:5000`

## Project Structure

- `app.py`: Main Flask application with route definitions
- `nutrition_calculator.py`: Core logic for nutrition calculation
- `data_provider.py`: Provides access to nutritional data and measurement standards
- `recipe_fetcher.py`: Fetches recipes using OpenAI API
- `data/`: Contains nutrition database and reference data
- `templates/`: HTML templates for the web interface
- `static/`: CSS, JavaScript, and other static assets

## Key Challenges Addressed

- **Standardization of Measurements**: Converting Indian household measurements (katori, pinch, etc.) to standard units
- **Recipe Variation**: Handling regional variations in the same dish
- **Ingredient Mapping**: Matching Indian ingredients to nutrition databases
- **Serving Size Determination**: Establishing standard serving sizes for different dish types

## Future Enhancements

- User accounts to save favorite dishes and personal history
- Customization of recipes to adjust nutrition values
- Meal planning with combined nutrition calculations
- Mobile app version for on-the-go calculations

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- VYB AI for the assignment opportunity
- OpenAI for the API powering recipe extraction
- Indian culinary experts for guidance on standard measurements

## Contact

For any questions or feedback, please contact: namarnadh.9@gmail.com