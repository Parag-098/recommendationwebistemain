from django import forms

class RecipeSearchForm(forms.Form):
    ingredients = forms.CharField(label="Enter ingredients (comma-separated)", required=False)
    max_cook_time = forms.IntegerField(label="Max Cooking Time (minutes)", required=False)
    recipe_type = forms.CharField(label="Recipe Type", required=False)
