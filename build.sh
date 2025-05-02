#!/bin/bash

# Build script for Vercel deployment
echo "Starting build process for Vercel deployment..."

# Ensure directories exist
mkdir -p data

# Copy sample data files if they don't exist
if [ ! -f "data/nutrition_db.py" ]; then
  echo "Creating sample nutrition database..."
  cp data/nutrition_db.py.sample data/nutrition_db.py 2>/dev/null || echo "No sample database found"
fi

if [ ! -f "data/dish_types.py" ]; then
  echo "Creating sample dish types data..."
  cp data/dish_types.py.sample data/dish_types.py 2>/dev/null || echo "No sample dish types found"
fi

if [ ! -f "data/household_measurements.py" ]; then
  echo "Creating sample household measurements data..."
  cp data/household_measurements.py.sample data/household_measurements.py 2>/dev/null || echo "No sample measurements found"
fi

# Create an empty XML storage file
echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?><nutritionRequests></nutritionRequests>" > data/nutrition_history.xml

# Set up environment variables for Vercel
echo "VERCEL=1" > .env
echo "DISABLE_OPENAI=1" >> .env

echo "Build process completed successfully!"