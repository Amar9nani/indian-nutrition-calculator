import logging
import difflib
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

def fuzzy_match(ingredient_name: str, available_ingredients: List[str], threshold: float = 0.8) -> Optional[str]:
    """
    Perform fuzzy matching to find the closest ingredient name in the database
    
    Args:
        ingredient_name: Name of the ingredient to match
        available_ingredients: List of available ingredient names in the database
        threshold: Minimum similarity score to consider a match (0.0 to 1.0)
        
    Returns:
        Matched ingredient name or None if no match found
    """
    # First try direct substring matching
    ingredient_lower = ingredient_name.lower()
    
    # Special cases and common synonyms
    synonyms = {
        "tomato": ["tomatoes"],
        "potato": ["potatoes", "aloo"],
        "onion": ["onions", "pyaz"],
        "chili": ["chilli", "chilies", "chillies"],
        "coriander": ["cilantro", "dhania"],
        "cumin": ["jeera"],
        "turmeric": ["haldi"],
        "ghee": ["clarified butter"],
        "oil": ["vegetable oil", "cooking oil", "mustard oil", "olive oil", "sunflower oil"],
        "bell pepper": ["capsicum"],
        "eggplant": ["aubergine", "brinjal", "baingan"],
        "cottage cheese": ["paneer"],
        "black gram lentils": ["urad dal", "black dal", "maa ki dal"],
        "red lentils": ["masoor dal"],
        "yellow lentils": ["moong dal", "toor dal", "arhar dal"],
        "fenugreek": ["methi"],
        "asafoetida": ["hing"],
        "green chilli": ["green chili", "hari mirch"],
        "red chilli powder": ["red chili powder", "lal mirch"]
    }
    
    # Check if the ingredient is a synonym
    for main_ingredient, alt_names in synonyms.items():
        if ingredient_lower in alt_names and main_ingredient in available_ingredients:
            return main_ingredient
    
    # Check if ingredient name is a substring of any available ingredient
    for available in available_ingredients:
        if ingredient_lower in available.lower() or available.lower() in ingredient_lower:
            return available
    
    # If no direct match, try fuzzy matching
    matches = difflib.get_close_matches(ingredient_lower, [i.lower() for i in available_ingredients], n=1, cutoff=threshold)
    if matches:
        # Find the original case version
        for available in available_ingredients:
            if available.lower() == matches[0]:
                return available
    
    return None

def convert_to_grams(measurement: Dict[str, Any], ingredient: str, data_provider) -> float:
    """
    Convert a household measurement to grams
    
    Args:
        measurement: Dictionary with amount and unit
        ingredient: Name of the ingredient
        data_provider: DataProvider instance
        
    Returns:
        Weight in grams
    """
    amount = measurement.get('amount', 1.0)
    unit = measurement.get('unit', 'cup')
    
    # Get the ingredient category for better conversion
    ingredient_category = data_provider.get_ingredient_category(ingredient)
    
    # Get conversion factor based on unit and ingredient category
    conversion_factor = data_provider.get_measurement_conversion(unit, ingredient_category)
    
    # If no specific conversion factor found, try default
    if not conversion_factor:
        conversion_factor = data_provider.get_measurement_conversion(unit, 'default')
        
    # If still no conversion factor, use reasonable defaults
    if not conversion_factor:
        if unit == 'cup':
            conversion_factor = 150
        elif unit == 'tablespoon':
            conversion_factor = 15
        elif unit == 'teaspoon':
            conversion_factor = 5
        elif unit == 'gram' or unit == 'g':
            conversion_factor = 1
        elif unit == 'kilogram' or unit == 'kg':
            conversion_factor = 1000
        elif unit == 'milliliter' or unit == 'ml':
            conversion_factor = 1
        elif unit == 'liter' or unit == 'l':
            conversion_factor = 1000
        elif unit == 'pinch':
            conversion_factor = 0.5
        elif unit == 'handful':
            conversion_factor = 30
        elif unit == 'piece' or unit == 'clove':
            conversion_factor = 10
        else:
            # Default if unit is unknown
            logger.warning(f"Unknown unit: {unit}, using default conversion of 10g")
            conversion_factor = 10
    
    # Calculate weight in grams
    weight_grams = amount * conversion_factor
    
    logger.debug(f"Converted {amount} {unit} of {ingredient} ({ingredient_category}) to {weight_grams}g")
    
    return weight_grams

def calculate_nutrition_values(ingredients: List[Dict[str, Any]], total_weight: float, serving_weight: float) -> Dict[str, float]:
    """
    Calculate nutrition values per serving based on ingredients
    
    Args:
        ingredients: List of ingredients with weights and nutrition data
        total_weight: Total weight of the dish in grams
        serving_weight: Weight of a single serving in grams
        
    Returns:
        Dictionary with calculated nutrition values per serving
    """
    total_nutrition = {
        'calories': 0,
        'protein': 0,
        'carbs': 0,
        'fat': 0,
        'fiber': 0
    }
    
    # Calculate total nutrition from all ingredients
    for item in ingredients:
        weight_grams = item['weight_grams']
        nutrition = item['nutrition']
        
        # Calculate nutrition based on weight (nutrition values are per 100g)
        factor = weight_grams / 100.0
        
        total_nutrition['calories'] += nutrition['calories'] * factor
        total_nutrition['protein'] += nutrition['protein'] * factor
        total_nutrition['carbs'] += nutrition['carbs'] * factor
        total_nutrition['fat'] += nutrition['fat'] * factor
        total_nutrition['fiber'] += nutrition.get('fiber', 0) * factor
    
    # Calculate ratio for serving size
    ratio = serving_weight / total_weight if total_weight > 0 else 1.0
    
    # Apply ratio to get nutrition per serving
    nutrition_per_serving = {
        'calories': round(total_nutrition['calories'] * ratio),
        'protein': round(total_nutrition['protein'] * ratio),
        'carbs': round(total_nutrition['carbs'] * ratio),
        'fat': round(total_nutrition['fat'] * ratio),
        'fiber': round(total_nutrition['fiber'] * ratio, 1)
    }
    
    return nutrition_per_serving
