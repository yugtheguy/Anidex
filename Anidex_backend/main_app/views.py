from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import uuid
from .animal_classifier import classifier

@api_view(['POST'])
def upload_image(request):
    """
    Upload an image locally, classify the animal, and return the URL
    """
    if 'image' not in request.FILES:
        return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Get the uploaded file
        image_file = request.FILES['image']
        image_file.seek(0)
        
        # Classify the animal and get detailed information
        classification_result = classifier.classify_and_get_info(image_file)
        predicted_animal = classification_result.get('predicted_animal')
        animal_info = classification_result.get('animal_info')
        
        # ✅ Take only the first name if multiple
        if predicted_animal and "," in predicted_animal:
            predicted_animal = predicted_animal.split(",")[0].strip()

        print(f"Classification result: {predicted_animal}")
        
        # ✅ Handle missing info
        if not animal_info:
            return Response(
                {"error": f"No additional info available for {predicted_animal or 'this animal'}"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        print(f"Predicted animal: {predicted_animal}")
        print(f"Animal info: {animal_info}")
        
        # Reset file pointer again for saving
        image_file.seek(0)
        
        # Generate unique filename
        file_extension = os.path.splitext(image_file.name)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        # Save file to media directory
        file_path = default_storage.save(f'animals/{unique_filename}', ContentFile(image_file.read()))
        
        # Get the URL for the saved file
        image_url = request.build_absolute_uri(f'/media/{file_path}')
        
        # ✅ Normalize response so frontend always gets consistent shape
        return Response({
            "image_url": image_url,
            "predicted_animal": predicted_animal,
            "animal_info": {
                "name": animal_info.get("name"),
                "characteristics": {
                    "scientific_name": animal_info.get("taxonomy", {}).get("scientific_name"),
                    "habitat": animal_info.get("characteristics", {}).get("habitat"),
                    "diet": animal_info.get("characteristics", {}).get("diet"),
                    "lifespan": animal_info.get("characteristics", {}).get("lifespan"),
                    "weight": animal_info.get("characteristics", {}).get("weight"),
                    "top_speed": animal_info.get("characteristics", {}).get("top_speed"),
                    "slogan": animal_info.get("characteristics", {}).get("slogan"),
                },
                "locations": animal_info.get("locations", [])
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Failed to upload image: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
