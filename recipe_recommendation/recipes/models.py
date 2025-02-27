from django.db import models

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    image_url = models.URLField(blank=True, null=True)  # Matches 'image' column
    cooking_time = models.IntegerField(blank=True, null=True)
    recipe_type = models.CharField(max_length=100, blank=True, null=True)  # Matches 'type' column
    ingredients = models.JSONField(blank=True, null=True)  # List of dictionaries
    directions = models.JSONField(blank=True, null=True)  # List of steps
    servings = models.CharField(max_length=50, blank=True, null=True)
    time = models.JSONField(blank=True, null=True)  # Stores prep, cook, and total time
    nutritions = models.JSONField(blank=True, null=True)  # Stores nutrition details

    def __str__(self):
        return self.title
