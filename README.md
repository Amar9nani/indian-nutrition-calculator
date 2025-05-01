# Indian Nutrition Calculator

A Python-based nutrition calculator for Indian dishes that estimates nutritional values per standard serving based on dish name.

![Indian Nutrition Calculator](generated-icon.png)

## About This Project

The Indian Nutrition Calculator is a web application developed as part of an assignment for VYB AI. It addresses the unique challenge of calculating nutrition for Indian recipes, which often lack standardized measurements and nutritional information compared to Western counterparts.

## Features

- **Instant Nutrition Calculation**: Enter any Indian dish name and get nutrition information
- **AI-Powered Recipe Extraction**: Uses OpenAI API to extract recipe information for dishes with offline fallback
- **Standardized Measurements**: Converts traditional Indian measurements to standard units
- **Nutrition Analysis**: Calculates calories, protein, carbs, fat, and fiber per standard serving
- **Visual Display**: Charts for easy interpretation of nutritional information
- **JSON Output**: Provides structured data output for integration with other applications
- **Calculation History**: Stores previous calculations in local XML storage for easy reference
- **Zero-configuration Setup**: Works on any system without database or API key setup

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
- **Data Storage**: XML-based local storage
- **API Integration**: OpenAI API for recipe extraction (with offline fallback)
- **Visualization**: Chart.js for nutrition data visualization
- **Data Processing**: Custom algorithms for ingredient mapping and measurement conversion

## Getting Started

### Prerequisites

- Python 3.11 or higher

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/indian-nutrition-calculator.git
   cd indian-nutrition-calculator
   ```

2. Install dependencies:
   ```
   pip install flask==2.3.3 flask-sqlalchemy==3.0.5 gunicorn==23.0.0 openai==1.11.0 psycopg2-binary==2.9.9 python-dotenv==1.0.0 email-validator==2.1.0
   ```

3. Run the application:
   ```
   flask run --host=0.0.0.0 --port=5000
   # OR
   python main.py
   # OR 
   gunicorn --bind 0.0.0.0:5000 --reload main:app
   ```

4. Open your browser and navigate to `http://localhost:5000`

## Running on Any System Without Errors

This application is designed to work seamlessly on any local system without requiring complex setup:

### Zero Configuration Setup

- **No Database Required**: The application uses local XML storage instead of a database
- **Default API Keys**: Built-in placeholder API key ensures the app works without OpenAI credentials
- **Auto-creating Directories**: Required folders are automatically created on first run
- **Fallback Recipes**: Pre-defined recipes for common dishes work without API access
- **Error Handling**: Robust error handling prevents crashes from missing data
- **OpenAI Version Compatibility**: Automatically handles OpenAI library version differences

### Fixing Common Errors

If you encounter an error related to the OpenAI library (like `TypeError: Client.__init__() got an unexpected keyword argument 'proxies'`), you can:

1. **Option 1**: Do nothing! The application will automatically detect version issues and use pre-defined recipe data instead.

2. **Option 2**: Update your OpenAI library:
   ```
   pip install openai==1.11.0
   ```

3. **Option 3**: Run with `--no-openai` flag to completely disable OpenAI integration:
   ```
   python main.py --no-openai
   ```

### Tips for Different Operating Systems

#### Windows
```
# Command Prompt
set FLASK_APP=main.py
set FLASK_DEBUG=1
flask run --host=0.0.0.0 --port=5000

# PowerShell
$env:FLASK_APP = "main.py"
$env:FLASK_DEBUG = 1
flask run --host=0.0.0.0 --port=5000
```

#### macOS/Linux
```
export FLASK_APP=main.py
export FLASK_DEBUG=1
flask run --host=0.0.0.0 --port=5000
```

#### Using Python Directly (All Systems)
```
python main.py
```

### Optional: Adding Your OpenAI API Key

While not required, you can add your own OpenAI API key for better recipe extraction:

1. Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your_actual_openai_key
   ```

2. Restart the application

### Local Development in VS Code

For detailed instructions on setting up and running the project in Visual Studio Code, see [LOCAL_DEV_GUIDE.md](LOCAL_DEV_GUIDE.md)

### Deployment

For detailed instructions on deploying this application to various cloud platforms, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

## Project Structure

- `app.py`: Main Flask application with route definitions
- `nutrition_calculator.py`: Core logic for nutrition calculation
- `data_provider.py`: Provides access to nutritional data and measurement standards
- `recipe_fetcher.py`: Fetches recipes using OpenAI API with offline fallbacks
- `xml_storage.py`: Manages local XML-based data storage
- `main.py`: Application entry point with automatic directory creation
- `data/`: Contains nutrition database, reference data, and XML storage files
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