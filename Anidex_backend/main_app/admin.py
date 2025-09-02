from django.contrib import admin
from .models import Animal

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('id', 'predicted_label', 'image', 'created_at')
    list_filter = ('predicted_label', 'created_at')
    search_fields = ('predicted_label', 'info')
    readonly_fields = ('image', 'created_at')
    ordering = ('-created_at',)
