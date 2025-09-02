from transformers import ViTForImageClassification, ViTImageProcessor
from PIL import Image
import torch
import io
import requests
import json
from decouple import config  # <-- import decouple

class AnimalClassifier:
    def __init__(self):
        self.model_name = "google/vit-base-patch16-224"
        self.model = ViTForImageClassification.from_pretrained(self.model_name)
        self.processor = ViTImageProcessor.from_pretrained(self.model_name)
        self.api_key = config("NINJA_API_KEY")
        self.api_url = "https://api.api-ninjas.com/v1/animals"
        
    def classify_animal(self, image_file):
        """
        Classify an animal from an uploaded image file
        
        Args:
            image_file: Django uploaded file object
            
        Returns:
            str: Predicted animal class name
        """
        try:
            # Convert Django file to PIL Image
            image = Image.open(io.BytesIO(image_file.read()))
            
            # Process the image
            inputs = self.processor(images=image, return_tensors="pt")
            
            # Get prediction
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
                predicted_class_idx = logits.argmax(-1).item()
                predicted_class = self.model.config.id2label[predicted_class_idx]
            
            return predicted_class
            
        except Exception as e:
            print(f"Error in animal classification: {str(e)}")
            return "Unknown Animal"
    
    def classify_animal_from_path(self, image_path):
        """
        Classify an animal from an image file path
        
        Args:
            image_path: Path to the image file
            
        Returns:
            str: Predicted animal class name
        """
        try:
            # Load image from path
            image = Image.open(image_path)
            
            # Process the image
            inputs = self.processor(images=image, return_tensors="pt")
            
            # Get prediction
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
                predicted_class_idx = logits.argmax(-1).item()
                predicted_class = self.model.config.id2label[predicted_class_idx]
            
            return predicted_class
            
        except Exception as e:
            print(f"Error in animal classification: {str(e)}")
            return "Unknown Animal"
    
    def get_animal_info(self, animal_name):
        """
        Get detailed information about an animal from API Ninjas
        
        Args:
            animal_name: Name of the animal to get information about
            
        Returns:
            dict: Animal information or None if failed
        """
        try:
            headers = {
                'X-Api-Key': self.api_key
            }
            
            params = {
                'name': animal_name.lower()
            }
            
            response = requests.get(self.api_url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    return data[0]  # Return first result
                else:
                    return None
            else:
                print(f"API request failed with status code: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error getting animal info: {str(e)}")
            return None
    
    def classify_and_get_info(self, image_file):
        """
        Classify an animal and get detailed information
        
        Args:
            image_file: Django uploaded file object
            
        Returns:
            dict: Contains predicted_animal and animal_info
        """
        # Classify the animal
        predicted_animal = self.classify_animal(image_file)
        
        # Get detailed information
        animal_info = self.get_animal_info(predicted_animal)
        
        return {
            'predicted_animal': predicted_animal,
            'animal_info': animal_info
        }

# Create a global instance
classifier = AnimalClassifier()
