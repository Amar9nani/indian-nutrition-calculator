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
                # Safe getters to handle potentially missing elements
                def safe_get_text(element_path):
                    element = entry.find(element_path)
                    return element.text if element is not None else ""
                
                def safe_get_float(element_path, default=0.0):
                    element = entry.find(element_path)
                    if element is not None and element.text:
                        try:
                            return float(element.text)
                        except (ValueError, TypeError):
                            return default
                    return default
                
                def safe_get_int(element_path, default=0):
                    element = entry.find(element_path)
                    if element is not None and element.text:
                        try:
                            return int(element.text)
                        except (ValueError, TypeError):
                            return default
                    return default
                
                # Parse created_at date safely
                created_at_str = safe_get_text('created_at')
                try:
                    created_at = datetime.fromisoformat(created_at_str) if created_at_str else None
                except (ValueError, TypeError):
                    created_at = None
                
                entry_data = {
                    'id': safe_get_int('id'),
                    'dish_name': safe_get_text('dish_name'),
                    'dish_type': safe_get_text('dish_type'),
                    'created_at': created_at,
                    'calories': safe_get_float('nutrition_values/calories'),
                    'protein': safe_get_float('nutrition_values/protein'),
                    'carbs': safe_get_float('nutrition_values/carbs'),
                    'fat': safe_get_float('nutrition_values/fat'),
                    'fiber': safe_get_float('nutrition_values/fiber'),
                    'ingredients_json': safe_get_text('ingredients_json'),
                    'serving_size_json': safe_get_text('serving_size_json'),
                }
                entries.append(entry_data)
            
            # Sort by created_at in descending order (newest first)
            # If created_at is None, put at the end
            entries.sort(key=lambda x: (x['created_at'] is None, x['created_at'] or datetime.min), reverse=True)
            return entries
        except Exception as e:
            print(f"Error retrieving nutrition history: {e}")
            return []