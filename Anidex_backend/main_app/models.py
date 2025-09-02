from django.db import models
from django.utils import timezone

# Create your models here.

class Animal(models.Model):
    image = models.ImageField()  # Cloudinary will handle storage
    predicted_label = models.CharField(max_length=255, blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.predicted_label or "Unlabeled Animal"
