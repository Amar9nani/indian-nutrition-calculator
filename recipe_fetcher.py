import os
import logging
import json
from typing import Dict, Any, Optional

# Initialize logger first
logger = logging.getLogger(__name__)

# Check if OpenAI integration is explicitly disabled
if os.environ.get("DISABLE_OPENAI") == "1":
    logger.warning("OpenAI integration explicitly disabled. Using fallback recipes only.")
    OPENAI_AVAILABLE = False
else:
    # Try to import OpenAI, but handle case when it's not installed or has version issues
    try:
        from openai import OpenAI
        # Test create a client to check for compatibility issues
        try:
            test_client = OpenAI(api_key="test_key")
            OPENAI_AVAILABLE = True
        except TypeError:
            # Handle the specific TypeError with 'proxies' argument
            logger.warning("OpenAI package version incompatibility. Using fallback recipes only.")
            OPENAI_AVAILABLE = False
        except Exception:
            # Handle any other exception during test initialization
            logger.warning("OpenAI initialization failed. Using fallback recipes only.")
            OPENAI_AVAILABLE = False
    except ImportError:
        logger.warning("OpenAI package not available. Using fallback recipes only.")
        OPENAI_AVAILABLE = False

class RecipeFetcher:
    """Class to fetch recipes using OpenAI API"""
    
    def __init__(self):
        """Initialize the recipe fetcher with API credentials"""
        # Always initialize these variables
        self.api_key = None
        self.client = None
        
        # If OpenAI is not available or has compatibility issues, just use fallback recipes
        if not OPENAI_AVAILABLE:
            return
            
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            logger.warning("OpenAI API key not found, using fallback data")
        else:
            try:
                self.client = OpenAI(api_key=self.api_key)
            except Exception as e:
                # Log any exceptions and fall back to sample recipes
                logger.error(f"Error initializing OpenAI client: {str(e)}")
                self.client = None
        
    def fetch_recipe(self, dish_name: str) -> Optional[Dict[str, Any]]:
        """
        Fetch recipe for a given dish name
        
        Args:
            dish_name: Name of the Indian dish
            
        Returns:
            Dictionary with recipe data or None if fetch failed
        """
        if not self.client:
            # Fallback to sample data if API not available
            return self._get_sample_recipe(dish_name)
            
        try:
            # Use OpenAI API to fetch recipe
            prompt = f"""
            I need a detailed traditional Indian recipe for "{dish_name}". 
            
            Return ONLY a JSON object with these fields:
            1. "ingredients": array of objects with "name" and "quantity" 
               (name should be the base ingredient, quantity should be in household measurements like cups, tablespoons)
            2. "cooking_method": brief description of preparation method
            
            Example format:
            {{
              "ingredients": [
                {{"name": "paneer", "quantity": "250g"}},
                {{"name": "tomato", "quantity": "2 medium"}}
              ],
              "cooking_method": "sauté onions, add spices, simmer with tomatoes, add paneer"
            }}
            
            The recipe should be authentic and include all necessary ingredients with approximate quantities.
            Do not include substitutes or variations. Focus on standard ingredients for this dish.
            """
            
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.7,
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Validate response structure
            if not result.get('ingredients'):
                logger.error(f"Invalid recipe structure received for {dish_name}")
                return self._get_sample_recipe(dish_name)
                
            return result
            
        except Exception as e:
            logger.error(f"Error fetching recipe from OpenAI: {str(e)}")
            return self._get_sample_recipe(dish_name)
    
    def _get_sample_recipe(self, dish_name: str) -> Dict[str, Any]:
        """Fallback method to return sample recipes for common dishes"""
        dish_name_lower = dish_name.lower()
        
        # Sample recipes for common Indian dishes
        if 'paneer butter masala' in dish_name_lower:
            return {
                "ingredients": [
                    {"name": "Paneer", "quantity": "250g"},
                    {"name": "Butter", "quantity": "2 tablespoons"},
                    {"name": "Tomato", "quantity": "3 medium"},
                    {"name": "Onion", "quantity": "1 large"},
                    {"name": "Ginger", "quantity": "1 inch piece"},
                    {"name": "Garlic", "quantity": "4 cloves"},
                    {"name": "Green Chilli", "quantity": "2"},
                    {"name": "Cashew Nuts", "quantity": "10"},
                    {"name": "Cream", "quantity": "2 tablespoons"},
                    {"name": "Red Chilli Powder", "quantity": "1 teaspoon"},
                    {"name": "Turmeric Powder", "quantity": "1/2 teaspoon"},
                    {"name": "Garam Masala", "quantity": "1 teaspoon"},
                    {"name": "Salt", "quantity": "to taste"},
                    {"name": "Sugar", "quantity": "1/2 teaspoon"},
                    {"name": "Oil", "quantity": "1 tablespoon"}
                ],
                "cooking_method": "Sauté onions, add ginger-garlic paste, tomatoes, spices. Blend to make gravy. Add butter, cream and paneer cubes."
            }
        elif 'dal makhani' in dish_name_lower:
            return {
                "ingredients": [
                    {"name": "Black Gram Lentils", "quantity": "1 cup"},
                    {"name": "Kidney Beans", "quantity": "1/4 cup"},
                    {"name": "Butter", "quantity": "3 tablespoons"},
                    {"name": "Cream", "quantity": "2 tablespoons"},
                    {"name": "Onion", "quantity": "1 medium"},
                    {"name": "Tomato", "quantity": "2 medium"},
                    {"name": "Ginger", "quantity": "1 inch piece"},
                    {"name": "Garlic", "quantity": "4 cloves"},
                    {"name": "Green Chilli", "quantity": "1"},
                    {"name": "Cumin Seeds", "quantity": "1 teaspoon"},
                    {"name": "Red Chilli Powder", "quantity": "1 teaspoon"},
                    {"name": "Garam Masala", "quantity": "1 teaspoon"},
                    {"name": "Salt", "quantity": "to taste"}
                ],
                "cooking_method": "Soak and pressure cook lentils and beans. Sauté cumin seeds, onions, ginger-garlic. Add tomatoes, spices, cooked lentils, butter, and cream."
            }
        elif 'chicken curry' in dish_name_lower:
            return {
                "ingredients": [
                    {"name": "Chicken", "quantity": "500g"},
                    {"name": "Onion", "quantity": "2 medium"},
                    {"name": "Tomato", "quantity": "2 medium"},
                    {"name": "Ginger", "quantity": "1 inch piece"},
                    {"name": "Garlic", "quantity": "5 cloves"},
                    {"name": "Green Chilli", "quantity": "2"},
                    {"name": "Oil", "quantity": "3 tablespoons"},
                    {"name": "Cumin Seeds", "quantity": "1 teaspoon"},
                    {"name": "Turmeric Powder", "quantity": "1/2 teaspoon"},
                    {"name": "Coriander Powder", "quantity": "1 tablespoon"},
                    {"name": "Red Chilli Powder", "quantity": "1 teaspoon"},
                    {"name": "Garam Masala", "quantity": "1 teaspoon"},
                    {"name": "Salt", "quantity": "to taste"},
                    {"name": "Coriander Leaves", "quantity": "2 tablespoons"}
                ],
                "cooking_method": "Marinate chicken with spices. Sauté onions, ginger-garlic paste, add tomatoes and spices. Add chicken and cook until tender."
            }
        elif 'aloo gobi' in dish_name_lower:
            return {
                "ingredients": [
                    {"name": "Potato", "quantity": "2 medium"},
                    {"name": "Cauliflower", "quantity": "1 small"},
                    {"name": "Onion", "quantity": "1 medium"},
                    {"name": "Tomato", "quantity": "1 medium"},
                    {"name": "Ginger", "quantity": "1 inch piece"},
                    {"name": "Garlic", "quantity": "3 cloves"},
                    {"name": "Green Chilli", "quantity": "1"},
                    {"name": "Oil", "quantity": "2 tablespoons"},
                    {"name": "Cumin Seeds", "quantity": "1 teaspoon"},
                    {"name": "Turmeric Powder", "quantity": "1/2 teaspoon"},
                    {"name": "Coriander Powder", "quantity": "1 tablespoon"},
                    {"name": "Red Chilli Powder", "quantity": "1 teaspoon"},
                    {"name": "Garam Masala", "quantity": "1/2 teaspoon"},
                    {"name": "Salt", "quantity": "to taste"},
                    {"name": "Coriander Leaves", "quantity": "1 tablespoon"}
                ],
                "cooking_method": "Sauté cumin seeds, onions, add ginger-garlic, tomatoes, spices, potatoes and cauliflower florets. Cover and cook till vegetables are tender."
            }
        elif 'biryani' in dish_name_lower or 'chicken biryani' in dish_name_lower:
            return {
                "ingredients": [
                    {"name": "Basmati Rice", "quantity": "2 cups"},
                    {"name": "Chicken", "quantity": "500g"},
                    {"name": "Onion", "quantity": "2 large"},
                    {"name": "Tomato", "quantity": "1 medium"},
                    {"name": "Yogurt", "quantity": "1/2 cup"},
                    {"name": "Ginger", "quantity": "1 inch piece"},
                    {"name": "Garlic", "quantity": "6 cloves"},
                    {"name": "Green Chilli", "quantity": "3"},
                    {"name": "Ghee", "quantity": "3 tablespoons"},
                    {"name": "Biryani Masala", "quantity": "2 tablespoons"},
                    {"name": "Turmeric Powder", "quantity": "1/2 teaspoon"},
                    {"name": "Red Chilli Powder", "quantity": "1 teaspoon"},
                    {"name": "Coriander Leaves", "quantity": "1/4 cup"},
                    {"name": "Mint Leaves", "quantity": "1/4 cup"},
                    {"name": "Salt", "quantity": "to taste"}
                ],
                "cooking_method": "Marinate chicken with yogurt and spices. Cook rice separately. Layer rice and chicken masala, dum cook on low heat."
            }
        elif 'palak paneer' in dish_name_lower:
            return {
                "ingredients": [
                    {"name": "Paneer", "quantity": "250g"},
                    {"name": "Spinach", "quantity": "500g"},
                    {"name": "Onion", "quantity": "1 medium"},
                    {"name": "Tomato", "quantity": "1 medium"},
                    {"name": "Ginger", "quantity": "1 inch piece"},
                    {"name": "Garlic", "quantity": "4 cloves"},
                    {"name": "Green Chilli", "quantity": "2"},
                    {"name": "Cream", "quantity": "2 tablespoons"},
                    {"name": "Butter", "quantity": "1 tablespoon"},
                    {"name": "Cumin Seeds", "quantity": "1 teaspoon"},
                    {"name": "Garam Masala", "quantity": "1 teaspoon"},
                    {"name": "Turmeric Powder", "quantity": "1/4 teaspoon"},
                    {"name": "Red Chilli Powder", "quantity": "1/2 teaspoon"},
                    {"name": "Salt", "quantity": "to taste"}
                ],
                "cooking_method": "Blanch spinach and blend to paste. Sauté cumin, onions, ginger-garlic paste, tomatoes, spices. Add spinach paste, simmer, add paneer cubes and cream."
            }
        elif 'chole' in dish_name_lower or 'chana masala' in dish_name_lower:
            return {
                "ingredients": [
                    {"name": "Chickpeas", "quantity": "2 cups"},
                    {"name": "Onion", "quantity": "2 medium"},
                    {"name": "Tomato", "quantity": "3 medium"},
                    {"name": "Ginger", "quantity": "1.5 inch piece"},
                    {"name": "Garlic", "quantity": "6 cloves"},
                    {"name": "Green Chilli", "quantity": "2"},
                    {"name": "Oil", "quantity": "3 tablespoons"},
                    {"name": "Cumin Seeds", "quantity": "1 teaspoon"},
                    {"name": "Bay Leaf", "quantity": "2"},
                    {"name": "Cinnamon Stick", "quantity": "1 inch"},
                    {"name": "Cloves", "quantity": "3"},
                    {"name": "Cardamom", "quantity": "2"},
                    {"name": "Turmeric Powder", "quantity": "1/2 teaspoon"},
                    {"name": "Coriander Powder", "quantity": "2 teaspoons"},
                    {"name": "Red Chilli Powder", "quantity": "1 teaspoon"},
                    {"name": "Garam Masala", "quantity": "1 teaspoon"},
                    {"name": "Amchur Powder", "quantity": "1 teaspoon"},
                    {"name": "Salt", "quantity": "to taste"},
                    {"name": "Coriander Leaves", "quantity": "2 tablespoons"}
                ],
                "cooking_method": "Soak and pressure cook chickpeas. Sauté whole spices, add onions, ginger-garlic paste, tomatoes, ground spices. Add chickpeas and simmer."
            }
        elif 'tandoori chicken' in dish_name_lower:
            return {
                "ingredients": [
                    {"name": "Chicken", "quantity": "1 kg"},
                    {"name": "Yogurt", "quantity": "1 cup"},
                    {"name": "Lemon Juice", "quantity": "2 tablespoons"},
                    {"name": "Ginger", "quantity": "1.5 inch piece"},
                    {"name": "Garlic", "quantity": "8 cloves"},
                    {"name": "Tandoori Masala", "quantity": "3 tablespoons"},
                    {"name": "Red Chilli Powder", "quantity": "1 teaspoon"},
                    {"name": "Turmeric Powder", "quantity": "1/2 teaspoon"},
                    {"name": "Garam Masala", "quantity": "1 teaspoon"},
                    {"name": "Mustard Oil", "quantity": "2 tablespoons"},
                    {"name": "Salt", "quantity": "to taste"}
                ],
                "cooking_method": "Make cuts in chicken pieces. Prepare marinade with yogurt, spices, ginger-garlic paste. Marinate chicken for 4+ hours. Bake or grill until cooked."
            }
        elif 'samosa' in dish_name_lower:
            return {
                "ingredients": [
                    {"name": "All-Purpose Flour", "quantity": "2 cups"},
                    {"name": "Potato", "quantity": "3 medium"},
                    {"name": "Green Peas", "quantity": "1/2 cup"},
                    {"name": "Onion", "quantity": "1 medium"},
                    {"name": "Ginger", "quantity": "1 inch piece"},
                    {"name": "Green Chilli", "quantity": "2"},
                    {"name": "Coriander Leaves", "quantity": "2 tablespoons"},
                    {"name": "Cumin Seeds", "quantity": "1 teaspoon"},
                    {"name": "Coriander Powder", "quantity": "1 teaspoon"},
                    {"name": "Garam Masala", "quantity": "1/2 teaspoon"},
                    {"name": "Amchur Powder", "quantity": "1 teaspoon"},
                    {"name": "Red Chilli Powder", "quantity": "1/2 teaspoon"},
                    {"name": "Oil", "quantity": "3 tablespoons"},
                    {"name": "Ghee", "quantity": "3 tablespoons"},
                    {"name": "Salt", "quantity": "to taste"},
                    {"name": "Oil for frying", "quantity": "as needed"}
                ],
                "cooking_method": "Make dough with flour, oil, salt. Prepare filling with boiled potatoes, peas, spices. Make cone-shaped samosas, fill and seal. Deep fry until golden brown."
            }
        elif 'butter chicken' in dish_name_lower or 'murgh makhani' in dish_name_lower:
            return {
                "ingredients": [
                    {"name": "Chicken", "quantity": "750g"},
                    {"name": "Butter", "quantity": "4 tablespoons"},
                    {"name": "Cream", "quantity": "4 tablespoons"},
                    {"name": "Yogurt", "quantity": "1/2 cup"},
                    {"name": "Tomato", "quantity": "5 medium"},
                    {"name": "Onion", "quantity": "2 medium"},
                    {"name": "Ginger", "quantity": "2 inch piece"},
                    {"name": "Garlic", "quantity": "8 cloves"},
                    {"name": "Green Chilli", "quantity": "3"},
                    {"name": "Kashmiri Red Chilli Powder", "quantity": "2 teaspoons"},
                    {"name": "Garam Masala", "quantity": "1.5 teaspoons"},
                    {"name": "Cumin Powder", "quantity": "1 teaspoon"},
                    {"name": "Turmeric Powder", "quantity": "1/2 teaspoon"},
                    {"name": "Kasoori Methi", "quantity": "1 tablespoon"},
                    {"name": "Sugar", "quantity": "1 teaspoon"},
                    {"name": "Salt", "quantity": "to taste"},
                    {"name": "Oil", "quantity": "2 tablespoons"}
                ],
                "cooking_method": "Marinate chicken with yogurt and spices. Grill/roast chicken. Prepare gravy with butter, tomatoes, onions, spices. Add cream and cooked chicken."
            }
        elif 'dosa' in dish_name_lower:
            return {
                "ingredients": [
                    {"name": "Rice", "quantity": "3 cups"},
                    {"name": "Urad Dal", "quantity": "1 cup"},
                    {"name": "Fenugreek Seeds", "quantity": "1 teaspoon"},
                    {"name": "Salt", "quantity": "to taste"},
                    {"name": "Oil", "quantity": "as needed"}
                ],
                "cooking_method": "Soak rice, urad dal, fenugreek seeds separately. Grind to smooth batter. Ferment overnight. Make thin crepes on hot griddle."
            }
        elif 'rajma' in dish_name_lower:
            return {
                "ingredients": [
                    {"name": "Kidney Beans", "quantity": "2 cups"},
                    {"name": "Onion", "quantity": "2 medium"},
                    {"name": "Tomato", "quantity": "3 medium"},
                    {"name": "Ginger", "quantity": "1.5 inch piece"},
                    {"name": "Garlic", "quantity": "6 cloves"},
                    {"name": "Green Chilli", "quantity": "2"},
                    {"name": "Cumin Seeds", "quantity": "1 teaspoon"},
                    {"name": "Bay Leaf", "quantity": "1"},
                    {"name": "Coriander Powder", "quantity": "1 tablespoon"},
                    {"name": "Red Chilli Powder", "quantity": "1 teaspoon"},
                    {"name": "Turmeric Powder", "quantity": "1/2 teaspoon"},
                    {"name": "Garam Masala", "quantity": "1 teaspoon"},
                    {"name": "Oil", "quantity": "3 tablespoons"},
                    {"name": "Salt", "quantity": "to taste"},
                    {"name": "Coriander Leaves", "quantity": "2 tablespoons"}
                ],
                "cooking_method": "Soak and pressure cook kidney beans. Sauté cumin seeds, bay leaf, onions, ginger-garlic paste, tomatoes, spices. Add cooked beans and simmer."
            }
        else:
            # Generic recipe for unknown dishes
            return {
                "ingredients": [
                    {"name": "Main Ingredient", "quantity": "250g"},
                    {"name": "Onion", "quantity": "1 medium"},
                    {"name": "Tomato", "quantity": "1 medium"},
                    {"name": "Ginger", "quantity": "1 inch piece"},
                    {"name": "Garlic", "quantity": "3 cloves"},
                    {"name": "Green Chilli", "quantity": "1"},
                    {"name": "Oil", "quantity": "2 tablespoons"},
                    {"name": "Cumin Seeds", "quantity": "1 teaspoon"},
                    {"name": "Turmeric Powder", "quantity": "1/2 teaspoon"},
                    {"name": "Coriander Powder", "quantity": "1 tablespoon"},
                    {"name": "Red Chilli Powder", "quantity": "1 teaspoon"},
                    {"name": "Garam Masala", "quantity": "1/2 teaspoon"},
                    {"name": "Salt", "quantity": "to taste"},
                    {"name": "Coriander Leaves", "quantity": "1 tablespoon"}
                ],
                "cooking_method": "Standard Indian cooking method with tempering, sautéing and simmering."
            }
