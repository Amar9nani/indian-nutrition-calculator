# Dish types with standard serving sizes
# For each dish type, defines the standard measurement, description, volume, and weight

DISH_TYPES = {
    "Wet Sabzi": {
        "measurement": "katori",
        "description": "200ml_katori",
        "volume_ml": 200,
        "weight_grams": 180
    },
    "Dry Sabzi": {
        "measurement": "katori",
        "description": "200ml_katori", 
        "volume_ml": 200,
        "weight_grams": 150
    },
    "Dal": {
        "measurement": "katori",
        "description": "200ml_katori",
        "volume_ml": 200,
        "weight_grams": 200
    },
    "Non-Veg Curry": {
        "measurement": "katori",
        "description": "200ml_katori",
        "volume_ml": 200,
        "weight_grams": 200
    },
    "Rice": {
        "measurement": "katori",
        "description": "200ml_katori",
        "volume_ml": 200,
        "weight_grams": 150
    },
    "Bread": {
        "measurement": "piece",
        "description": "1_piece",
        "volume_ml": None,
        "weight_grams": 30
    },
    "Raita": {
        "measurement": "katori",
        "description": "100ml_katori",
        "volume_ml": 100,
        "weight_grams": 100
    },
    "Chutney": {
        "measurement": "tablespoon",
        "description": "1_tablespoon",
        "volume_ml": 15,
        "weight_grams": 15
    }
}

# Dish type categories with keywords for identification
DISH_TYPE_CATEGORIES = {
    "Wet Sabzi": [
        "curry", "gravy", "masala", "paneer", "malai", "palak",
        "butter", "korma", "kadhai", "makhani", "do pyaza"
    ],
    "Dry Sabzi": [
        "fry", "bhaji", "saag", "sukhi", "dry", "roast", "bhuna",
        "tawa", "sukha", "aloo gobi", "aloo matar"
    ],
    "Dal": [
        "dal", "lentil", "sambar", "toor", "moong", "masoor",
        "chana", "rajma", "chole", "bean", "lobhia"
    ],
    "Non-Veg Curry": [
        "chicken", "mutton", "lamb", "fish", "prawn", "egg",
        "keema", "tikka masala", "vindaloo", "saag meat"
    ],
    "Rice": [
        "rice", "biryani", "pulao", "khichdi", "fried rice",
        "jeera rice", "lemon rice", "tamarind rice"
    ],
    "Bread": [
        "roti", "naan", "paratha", "chapati", "kulcha",
        "bhakri", "puri", "phulka", "thepla"
    ],
    "Raita": [
        "raita", "pachadi", "yogurt", "curd", "dahi"
    ],
    "Chutney": [
        "chutney", "pickle", "achar", "relish", "mint sauce",
        "tamarind sauce", "coconut", "coriander"
    ]
}
