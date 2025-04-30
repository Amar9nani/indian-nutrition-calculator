# Household measurements conversion table to grams
# Values represent the weight in grams for each measurement unit
# Different conversions based on ingredient category

HOUSEHOLD_MEASUREMENTS = {
    # Cup measurements (in grams)
    "cup": {
        "default": 150,
        "liquid": 240,
        "rice": 180,
        "flour": 120,
        "sugar": 200,
        "vegetables": 150,
        "chopped_vegetables": 150,
        "grated_vegetables": 110,
        "lentils": 200,
        "oil": 220,
        "milk": 240,
        "yogurt": 245,
        "spice": 100
    },
    
    # Tablespoon measurements (in grams)
    "tablespoon": {
        "default": 15,
        "liquid": 15,
        "oil": 14,
        "ghee": 13,
        "butter": 14,
        "flour": 8,
        "sugar": 12,
        "salt": 15,
        "spice": 5,
        "powder": 7
    },
    
    # Teaspoon measurements (in grams)
    "teaspoon": {
        "default": 5,
        "liquid": 5,
        "oil": 4.5,
        "ghee": 4,
        "butter": 4.5,
        "flour": 3,
        "sugar": 4,
        "salt": 5,
        "spice": 2,
        "powder": 2.5
    },
    
    # Other common measurements
    "pinch": {
        "default": 0.5,
        "salt": 0.5,
        "spice": 0.5,
        "powder": 0.5
    },
    
    "handful": {
        "default": 30,
        "vegetables": 30,
        "chopped_vegetables": 30,
        "grated_vegetables": 25,
        "grains": 35,
        "nuts": 25,
        "herbs": 10
    },
    
    # Weight measurements
    "gram": {
        "default": 1
    },
    
    "kilogram": {
        "default": 1000
    },
    
    # Volume measurements
    "milliliter": {
        "default": 1,
        "liquid": 1,
        "oil": 0.92,
        "milk": 1.03
    },
    
    "liter": {
        "default": 1000,
        "liquid": 1000,
        "oil": 920,
        "milk": 1030
    },
    
    # Common household items
    "clove": {
        "default": 5,
        "garlic": 5
    },
    
    "piece": {
        "default": 15,
        "ginger": 15,
        "vegetable": 50,
        "meat": 60
    }
}
