import os
import xml.etree.ElementTree as ET
from datetime import datetime
import json
from pathlib import Path

class XMLStorage:
    """Storage class for saving nutrition requests to XML file"""
    
    def __init__(self, file_path='data/nutrition_history.xml'):
        """Initialize the XML storage with the specified file path"""
        self.file_path = file_path
        self.root_tag = 'nutrition_history'
        
        # Create directory if it doesn't exist
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Check if file exists, if not create it with root element
        if not os.path.exists(file_path):
            root = ET.Element(self.root_tag)
            tree = ET.ElementTree(root)
            tree.write(file_path)
    
    def save_nutrition_request(self, nutrition_data):
        """
        Save nutrition calculation data to XML
        
        Args:
            nutrition_data (dict): Dictionary with nutrition calculation data
        """
        try:
            # Parse existing XML file
            tree = ET.parse(self.file_path)
            root = tree.getroot()
            
            # Create new entry element
            entry = ET.SubElement(root, 'entry')
            ET.SubElement(entry, 'id').text = str(len(root) + 1)
            ET.SubElement(entry, 'dish_name').text = nutrition_data.get('dish_name', '')
            ET.SubElement(entry, 'dish_type').text = nutrition_data.get('dish_type', '')
            ET.SubElement(entry, 'created_at').text = datetime.now().isoformat()
            
            # Add nutrition values
            nutrition = ET.SubElement(entry, 'nutrition_values')
            nutrition_per_serving = nutrition_data.get('nutrition_per_serving', {})
            ET.SubElement(nutrition, 'calories').text = str(nutrition_per_serving.get('calories', 0))
            ET.SubElement(nutrition, 'protein').text = str(nutrition_per_serving.get('protein', 0))
            ET.SubElement(nutrition, 'carbs').text = str(nutrition_per_serving.get('carbs', 0))
            ET.SubElement(nutrition, 'fat').text = str(nutrition_per_serving.get('fat', 0))
            ET.SubElement(nutrition, 'fiber').text = str(nutrition_per_serving.get('fiber', 0))
            
            # Store ingredients and serving size as JSON strings
            ET.SubElement(entry, 'ingredients_json').text = json.dumps(nutrition_data.get('ingredients', []))
            ET.SubElement(entry, 'serving_size_json').text = json.dumps(nutrition_data.get('serving_size', {}))
            
            # Save updated XML
            tree.write(self.file_path)
            return True
        except Exception as e:
            print(f"Error saving nutrition data to XML: {e}")
            return False
    
    def get_all_nutrition_requests(self):
        """
        Retrieve all nutrition requests from XML
        
        Returns:
            list: List of dictionaries with nutrition data
        """
        try:
            # Check if file exists
            if not os.path.exists(self.file_path):
                return []
            
            tree = ET.parse(self.file_path)
            root = tree.getroot()
            
            entries = []
            for entry in root.findall('entry'):
                entry_data = {
                    'id': int(entry.find('id').text),
                    'dish_name': entry.find('dish_name').text,
                    'dish_type': entry.find('dish_type').text,
                    'created_at': datetime.fromisoformat(entry.find('created_at').text),
                    'calories': float(entry.find('nutrition_values/calories').text),
                    'protein': float(entry.find('nutrition_values/protein').text),
                    'carbs': float(entry.find('nutrition_values/carbs').text),
                    'fat': float(entry.find('nutrition_values/fat').text),
                    'fiber': float(entry.find('nutrition_values/fiber').text),
                    'ingredients_json': entry.find('ingredients_json').text,
                    'serving_size_json': entry.find('serving_size_json').text,
                }
                entries.append(entry_data)
            
            # Sort by created_at in descending order (newest first)
            entries.sort(key=lambda x: x['created_at'], reverse=True)
            return entries
        except Exception as e:
            print(f"Error retrieving nutrition history: {e}")
            return []