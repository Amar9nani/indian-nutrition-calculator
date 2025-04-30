import logging
from typing import Dict, List, Any, Optional

from data.nutrition_db import NUTRITION_DB
from data.household_measurements import HOUSEHOLD_MEASUREMENTS
from data.dish_types import DISH_TYPES, DISH_TYPE_CATEGORIES

logger = logging.getLogger(__name__)

class DataProvider:
    """Class to provide access to nutritional data and measurement standards"""
    
    def __init__(self):
        """Initialize the data provider with required data sources"""
        self.nutrition_db = NUTRITION_DB
        self.household_measurements = HOUSEHOLD_MEASUREMENTS
        self.dish_types = DISH_TYPE_CATEGORIES
        self.serving_sizes = DISH_TYPES
    
    def get_nutrition_item(self, ingredient_name: str) -> Optional[Dict[str, Any]]:
        """
        Get nutrition information for an ingredient
        
        Args:
            ingredient_name: Name of the ingredient
            
        Returns:
            Dictionary with nutritional values or None if not found
        """
        # Try direct match first
        if ingredient_name in self.nutrition_db:
            return self.nutrition_db[ingredient_name]
            
        # Try lowercase match
        ingredient_lower = ingredient_name.lower()
        for key, value in self.nutrition_db.items():
            if key.lower() == ingredient_lower:
                return value
                
        return None
    
    def get_all_ingredients(self) -> List[str]:
        """Get list of all ingredients in the nutrition database"""
        return list(self.nutrition_db.keys())
    
    def get_measurement_conversion(self, unit: str, ingredient_category: str = None) -> Optional[float]:
        """
        Get conversion factor from household measurement to grams
        
        Args:
            unit: Household measurement unit (cup, tablespoon, etc.)
            ingredient_category: Category of ingredient (optional)
            
        Returns:
            Conversion factor to grams or None if not found
        """
        if unit in self.household_measurements:
            if ingredient_category and ingredient_category in self.household_measurements[unit]:
                return self.household_measurements[unit][ingredient_category]
            return self.household_measurements[unit].get('default', None)
        return None
    
    def get_dish_types(self) -> Dict[str, List[str]]:
        """Get mapping of dish types to their identifying keywords"""
        return self.dish_types
    
    def get_serving_size(self, dish_type: str) -> Dict[str, Any]:
        """
        Get standard serving size for a dish type
        
        Args:
            dish_type: Type of dish (Wet Sabzi, Dry Sabzi, etc.)
            
        Returns:
            Dictionary with serving size information
        """
        if dish_type in self.serving_sizes:
            return self.serving_sizes[dish_type]
            
        # Default serving size if dish type is unknown
        logger.warning(f"Unknown dish type: {dish_type}, using default serving size")
        return {
            'measurement': 'katori',
            'description': '200ml_katori',
            'volume_ml': 200,
            'weight_grams': 180
        }
    
    def get_ingredient_category(self, ingredient_name: str) -> str:
        """
        Determine the category of an ingredient for measurement conversion
        
        Args:
            ingredient_name: Name of the ingredient
            
        Returns:
            Category of the ingredient (liquid, spice, vegetable, etc.)
        """
        # Simple categorization based on ingredient name
        ingredient_lower = ingredient_name.lower()
        
        # Liquids
        if any(liquid in ingredient_lower for liquid in ['water', 'milk', 'oil', 'juice', 'stock', 'cream']):
            return 'liquid'
            
        # Spices
        if any(spice in ingredient_lower for spice in ['powder', 'masala', 'spice', 'salt', 'turmeric', 'cumin', 'coriander']):
            return 'spice'
            
        # Grains
        if any(grain in ingredient_lower for grain in ['rice', 'flour', 'dal', 'lentil']):
            return 'grain'
            
        # Vegetables
        if any(veg in ingredient_lower for veg in ['tomato', 'onion', 'potato', 'carrot', 'peas', 'bell pepper', 'capsicum']):
            return 'vegetable'
            
        # Meats
        if any(meat in ingredient_lower for meat in ['chicken', 'mutton', 'beef', 'fish']):
            return 'meat'
            
        # Default to solid
        return 'solid'
