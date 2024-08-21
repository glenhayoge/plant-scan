from rest_framework import viewsets
from .models import Plant
from .serializers import PlantSerializer
from google.cloud import vision
from google.cloud.vision_v1 import types
from rest_framework.response import Response
from rest_framework import status

class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer

    def create(self, request, *args, **kwargs):
        image_file = request.FILES.get('image')

        # Use the Google Gemini API to identify the plant
        client = vision.ImageAnnotatorClient()
        image = types.Image(content=image_file.read())
        response = client.label_detection(image=image)
        labels = response.label_annotations

        # Find the most likely plant label
        plant_label = next((label for label in labels if 'plant' in label.description.lower()), None)
        if plant_label:
            plant_name = plant_label.description
            plant_description = 'This plant is a ' + plant_name
        else:
            plant_name = 'Unknown'
            plant_description = 'We could not identify the plant in the image.'

        # Create the plant object
        plant = Plant.objects.create(
            name=plant_name,
            description=plant_description,
            image=image_file
        )

        serializer = self.get_serializer(plant)
        return Response(serializer.data, status=status.HTTP_201_CREATED)