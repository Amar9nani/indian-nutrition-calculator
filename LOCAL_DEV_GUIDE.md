# Local Development Guide

This guide explains how to run the Indian Nutrition Calculator project locally in Visual Studio Code.

## Prerequisites

1. **Python**: Make sure Python 3.11 or higher is installed
2. **Git**: Install Git to clone the repository
3. **VS Code**: Install Visual Studio Code
4. **VS Code Extensions**: Install the following extensions:
   - Python extension
   - Pylance

## Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/indian-nutrition-calculator.git
cd indian-nutrition-calculator
```

## Step 2: Set Up a Virtual Environment

In VS Code terminal:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

## Step 3: Install Dependencies

```bash
pip install flask==2.3.3 flask-sqlalchemy==3.0.5 gunicorn==23.0.0 openai==1.11.0 psycopg2-binary==2.9.9 python-dotenv==1.0.0 email-validator==2.1.0
```

## Step 4: Set Up Environment Variables (Optional)

The application has default keys, but you can create a `.env` file in the root directory to override them:

```
OPENAI_API_KEY=your_openai_api_key
```

If you have a real OpenAI API key, replace the placeholder above with your actual key.

## Step 5: Start the Application

In the VS Code terminal with your virtual environment activated:

```bash
# For development
flask run --host=0.0.0.0 --port=5000

# Alternatively, use gunicorn
gunicorn --bind 0.0.0.0:5000 --reload main:app
```

## Step 6: Access the Application

Open your browser and navigate to:

```
http://localhost:5000
```

## Debugging in VS Code

1. Create a `.vscode/launch.json` file with the following content:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "main.py",
                "FLASK_DEBUG": "1"
            },
            "args": [
                "run",
                "--host=0.0.0.0",
                "--port=5000"
            ],
            "jinja": true,
            "justMyCode": true
        }
    ]
}
```

2. Set breakpoints in your code
3. Start debugging by pressing F5 or clicking the green play button in the Run and Debug panel

## XML Storage

This app uses XML files to store nutrition history. The storage is located in the `data` directory:

- `data/nutrition_history.xml`: Stores all nutrition calculations

The XML storage automatically creates this file if it doesn't exist, so no special setup is required. The application handles all reading and writing to this file.

## Troubleshooting

- **Module Not Found Errors**: Make sure you've installed all dependencies and activated your virtual environment
- **OpenAI API Errors**: If you see API rate limits or connection errors, this is likely because the default placeholder API key is being used. Add your own OpenAI API key to the `.env` file
- **Port Already in Use**: Change the port number in your run command if 5000 is already in use
- **File Permission Issues**: If you encounter errors related to writing XML files, check that your application has write permissions to the `data` directory

## Key Files

- `main.py`: Application entry point
- `app.py`: Main Flask application logic
- `nutrition_calculator.py`: Core calculation engine
- `data_provider.py`: Data access layer
- `recipe_fetcher.py`: Recipe extraction with OpenAI

## Running Tests

```bash
# If you have pytest installed
pytest
```

## Need Help?

Contact: namarnadh.9@gmail.com