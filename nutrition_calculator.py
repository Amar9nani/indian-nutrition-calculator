import logging
import json
import re
from typing import Dict, List, Any, Optional

from recipe_fetcher import RecipeFetcher
from data_provider import DataProvider
from utils.helpers import fuzzy_match, convert_to_grams, calculate_nutrition_values

logger = logging.getLogger(__name__)

class NutritionCalculator:
    """Main class for calculating nutrition values of Indian dishes"""
    
    def __init__(self):
        """Initialize the nutrition calculator with required data sources"""
        self.recipe_fetcher = RecipeFetcher()
        self.data_provider = DataProvider()
        self.ingredient_patterns = self._build_ingredient_patterns()
        
    def _build_ingredient_patterns(self) -> Dict[str, re.Pattern]:
        """Build regex patterns for ingredient parsing"""
        patterns = {}
        for ingredient in self.data_provider.get_all_ingredients():
            # Create pattern to match ingredient name with variations
            pattern_str = r'\b' + re.escape(ingredient.lower()) + r'\b'
            # Also add pattern for plural form
            if ingredient.endswith('o'):
                pattern_str += r'|\b' + re.escape(ingredient.lower()) + r'es\b'
            elif not ingredient.endswith('s'):
                pattern_str += r'|\b' + re.escape(ingredient.lower()) + r's\b'
            patterns[ingredient] = re.compile(pattern_str, re.IGNORECASE)
            
        return patterns
    
    def calculate_nutrition(self, dish_name: str) -> Optional[Dict[str, Any]]:
        """
        Calculate nutrition for a given dish
        
        Args:
            dish_name: Name of the Indian dish
            
        Returns:
            Dictionary with nutritional information or None if calculation failed
        """
        try:
            # Step 1: Fetch recipe
            recipe = self.recipe_fetcher.fetch_recipe(dish_name)
            if not recipe or not recipe.get('ingredients'):
                logger.error(f"Failed to fetch recipe for {dish_name}")
                return None
                
            # Step 2: Identify dish type
            dish_type = self._identify_dish_type(dish_name, recipe)
            logger.info(f"Identified dish type: {dish_type}")
            
            # Step 3: Map ingredients to nutrition database
            mapped_ingredients = self._map_ingredients(recipe['ingredients'])
            if not mapped_ingredients:
                logger.error(f"Failed to map ingredients for {dish_name}")
                return None
                
            # Step 4: Convert quantities to grams
            ingredients_in_grams = self._standardize_quantities(mapped_ingredients, dish_type)
            
            # Step 5: Calculate total nutrition
            total_nutrition = self._calculate_total_nutrition(ingredients_in_grams)
            
            # Step 6: Calculate nutrition per serving
            serving_size = self.data_provider.get_serving_size(dish_type)
            total_weight = sum(item['weight_grams'] for item in ingredients_in_grams)
            
            # Prepare result in the expected format
            nutrition_per_serving = self._calculate_nutrition_per_serving(
                total_nutrition, total_weight, serving_size
            )
            
            result = {
                f"estimated_nutrition_per_{serving_size['description']}": nutrition_per_serving,
                "dish_type": dish_type,
                "serving_size": serving_size,
                "ingredients_used": [
                    {
                        "ingredient": item['ingredient'],
                        "quantity": item['display_quantity']
                    } for item in ingredients_in_grams
                ]
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error calculating nutrition: {str(e)}")
            return None
    
    def _identify_dish_type(self, dish_name: str, recipe: Dict[str, Any]) -> str:
        """Identify the dish type based on name and ingredients"""
        dish_types = self.data_provider.get_dish_types()
        
        # First try to determine dish type from dish name
        dish_name_lower = dish_name.lower()
        for dish_type, keywords in dish_types.items():
            for keyword in keywords:
                if keyword.lower() in dish_name_lower:
                    return dish_type
        
        # If not found by name, try to determine by ingredients and cooking method
        ingredients_text = " ".join([i['name'] for i in recipe['ingredients']])
        cooking_hints = recipe.get('cooking_method', '')
        
        if cooking_hints:
            combined_text = ingredients_text + " " + cooking_hints
        else:
            combined_text = ingredients_text
            
        combined_text = combined_text.lower()
        
        # Check for specific indicators
        if 'gravy' in combined_text or 'curry' in combined_text:
            if 'chicken' in combined_text or 'mutton' in combined_text or 'fish' in combined_text:
                return "Non-Veg Curry"
            return "Wet Sabzi"
            
        if 'dal' in combined_text or 'lentil' in combined_text:
            return "Dal"
            
        if 'paneer' in combined_text:
            if 'gravy' in combined_text or 'curry' in combined_text:
                return "Wet Sabzi"
            return "Dry Sabzi"
            
        if 'rice' in combined_text:
            return "Rice"
            
        if 'roti' in combined_text or 'naan' in combined_text or 'paratha' in combined_text:
            return "Bread"
            
        # Default to most common type
        return "Wet Sabzi"
    
    def _map_ingredients(self, ingredients: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Map ingredients from recipe to nutrition database"""
        mapped_ingredients = []
        
        for ingredient in ingredients:
            ingredient_name = ingredient['name']
            quantity = ingredient.get('quantity', '')
            
            # Try direct match first
            nutrition_item = self.data_provider.get_nutrition_item(ingredient_name)
            
            # If no direct match, try fuzzy matching
            if not nutrition_item:
                matched_name = fuzzy_match(
                    ingredient_name,
                    self.data_provider.get_all_ingredients()
                )
                if matched_name:
                    nutrition_item = self.data_provider.get_nutrition_item(matched_name)
                    logger.info(f"Fuzzy matched '{ingredient_name}' to '{matched_name}'")
                    ingredient_name = matched_name
            
            # If still no match, log and skip
            if not nutrition_item:
                logger.warning(f"No match found for ingredient: {ingredient_name}")
                continue
                
            mapped_ingredients.append({
                'ingredient': ingredient_name,
                'raw_quantity': quantity,
                'nutrition': nutrition_item
            })
            
        return mapped_ingredients
    
    def _standardize_quantities(self, mapped_ingredients: List[Dict[str, Any]], dish_type: str) -> List[Dict[str, Any]]:
        """Convert ingredient quantities to grams using standard measurements"""
        standardized_ingredients = []
        
        for item in mapped_ingredients:
            ingredient = item['ingredient']
            raw_quantity = item['raw_quantity']
            nutrition = item['nutrition']
            
            # Convert raw quantity to a standard household measurement
            measurement, display_quantity = self._parse_quantity(raw_quantity, ingredient)
            
            # Convert standard measurement to grams
            weight_grams = convert_to_grams(measurement, ingredient, self.data_provider)
            
            # Skip ingredients with zero weight
            if weight_grams <= 0:
                logger.warning(f"Zero weight for ingredient: {ingredient}, quantity: {raw_quantity}")
                continue
                
            standardized_ingredients.append({
                'ingredient': ingredient,
                'raw_quantity': raw_quantity,
                'display_quantity': display_quantity,
                'weight_grams': weight_grams,
                'nutrition': nutrition
            })
            
        return standardized_ingredients
    
    def _parse_quantity(self, raw_quantity: str, ingredient: str) -> tuple:
        """Parse raw quantity string into structured measurement"""
        if not raw_quantity:
            # Default quantities for common ingredients
            defaults = {
                'salt': '1 teaspoon',
                'water': '1 cup',
                'oil': '2 tablespoons',
                'ghee': '1 tablespoon',
                'spices': '1 teaspoon',
                'ginger': '1 inch piece',
                'garlic': '2 cloves',
                'turmeric': '1/2 teaspoon',
                'red chili powder': '1/2 teaspoon',
                'garam masala': '1/2 teaspoon'
            }
            
            for key, value in defaults.items():
                if key in ingredient.lower():
                    raw_quantity = value
                    break
            else:
                # Generic default
                raw_quantity = '1/4 cup'
                
        # Extract number and unit from raw quantity
        number_pattern = r'(\d+(?:\.\d+)?|\d+\/\d+|\d+\s+\d+\/\d+)'
        unit_pattern = r'(cup|cups|tablespoon|tablespoons|tbsp|teaspoon|teaspoons|tsp|gram|grams|g|kg|ml|liter|liters|pinch|handful|piece|clove|cloves)'
        
        number_match = re.search(number_pattern, raw_quantity)
        unit_match = re.search(unit_pattern, raw_quantity, re.IGNORECASE)
        
        amount = 1.0
        unit = "cup"
        
        if number_match:
            number_str = number_match.group(1)
            # Handle fractions
            if '/' in number_str:
                if ' ' in number_str:
                    # Mixed fraction (e.g. "1 1/2")
                    whole, fraction = number_str.split(' ')
                    numerator, denominator = fraction.split('/')
                    amount = float(whole) + float(numerator) / float(denominator)
                else:
                    # Simple fraction (e.g. "1/2")
                    numerator, denominator = number_str.split('/')
                    amount = float(numerator) / float(denominator)
            else:
                amount = float(number_str)
        
        if unit_match:
            unit = unit_match.group(1).lower()
            
            # Standardize units
            if unit in ['tablespoon', 'tablespoons', 'tbsp']:
                unit = 'tablespoon'
            elif unit in ['teaspoon', 'teaspoons', 'tsp']:
                unit = 'teaspoon'
            elif unit in ['cup', 'cups']:
                unit = 'cup'
            elif unit in ['gram', 'grams', 'g']:
                unit = 'gram'
            elif unit in ['kg']:
                unit = 'kilogram'
            elif unit in ['ml']:
                unit = 'milliliter'
            elif unit in ['liter', 'liters']:
                unit = 'liter'
            elif unit in ['clove', 'cloves']:
                unit = 'clove'
            elif unit in ['piece']:
                unit = 'piece'
            elif unit in ['pinch']:
                unit = 'pinch'
            elif unit in ['handful']:
                unit = 'handful'
                
        # Create display quantity (for UI)
        display_quantity = f"{amount} {unit}"
        if amount != 1 and unit != 'handful' and unit != 'pinch':
            display_quantity += 's' if not unit.endswith('s') else ''
            
        measurement = {
            'amount': amount,
            'unit': unit
        }
        
        return measurement, display_quantity
    
    def _calculate_total_nutrition(self, ingredients: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate total nutrition values for all ingredients"""
        total_nutrition = {
            'calories': 0,
            'protein': 0,
            'carbs': 0,
            'fat': 0,
            'fiber': 0
        }
        
        for item in ingredients:
            weight_grams = item['weight_grams']
            nutrition = item['nutrition']
            
            # Calculate nutrition based on weight in grams
            # Nutrition values in database are per 100g
            factor = weight_grams / 100.0
            
            total_nutrition['calories'] += nutrition['calories'] * factor
            total_nutrition['protein'] += nutrition['protein'] * factor
            total_nutrition['carbs'] += nutrition['carbs'] * factor
            total_nutrition['fat'] += nutrition['fat'] * factor
            total_nutrition['fiber'] += nutrition.get('fiber', 0) * factor
            
        return total_nutrition
    
    def _calculate_nutrition_per_serving(self, total_nutrition: Dict[str, float], 
                                        total_weight: float, serving_size: Dict[str, Any]) -> Dict[str, float]:
        """Calculate nutrition values per standard serving"""
        # Skip invalid values
        if total_weight <= 0 or serving_size['weight_grams'] <= 0:
            logger.warning(f"Invalid weights: total={total_weight}, serving={serving_size['weight_grams']}")
            return total_nutrition
            
        # Calculate ratio of serving size to total weight
        ratio = serving_size['weight_grams'] / total_weight
        
        # Apply ratio to get nutrition per serving
        nutrition_per_serving = {
            'calories': round(total_nutrition['calories'] * ratio),
            'protein': round(total_nutrition['protein'] * ratio),
            'carbs': round(total_nutrition['carbs'] * ratio),
            'fat': round(total_nutrition['fat'] * ratio),
            'fiber': round(total_nutrition['fiber'] * ratio, 1)
        }
        
        return nutrition_per_serving
