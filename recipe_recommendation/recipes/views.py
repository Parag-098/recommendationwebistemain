import os
import pandas as pd
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator

# Get the absolute path of the CSV file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE_PATH = os.path.join(BASE_DIR, "data/Mainrecipe.csv")

# Function to safely load JSON data
def safe_json_load(value, default=None):
    """Safely loads JSON from a string and returns a default value if invalid."""
    if pd.isna(value) or value in ["", "null", None]:
        return default if default is not None else []
    try:
        return json.loads(value.replace("'", "\""))  # Convert single quotes to double quotes for valid JSON
    except json.JSONDecodeError:
        return default if default is not None else []

# Function to load recipes from CSV
def load_recipes():
    """Reads recipe data from a CSV file and returns a list of dictionaries."""
    df = pd.read_csv(CSV_FILE_PATH)
    df.rename(columns={"image": "image_url", "type": "recipe_type"}, inplace=True)

    recipes = []
    for _, row in df.iterrows():
        # Extract time details
        time_data = safe_json_load(row.get("time", ""), default=[])
        time_details = {}

        for item in time_data:
            label = item.get("Label", "").strip().replace(" ", "_").replace(":", "")  # Convert spaces to underscores
            value = item.get("Value", "").strip()
            time_details[label] = value

        # 🔥 Extract servings from multiple possible locations
        servings = row.get("servings", "").strip()  # Default to direct column

        # Check if servings exist in `time` column
        if not servings:
            for item in time_data:
                if "Servings" in item["Label"]:
                    servings = item["Value"]
                    break

        # Check `nutrition_details` for servings if still empty
        if not servings:
            nutrition_data = safe_json_load(row.get("nutritions", ""), default=[])
            for item in nutrition_data:
                if "Servings" in item["Label"]:
                    servings = item["Value"]
                    break

        # Extract nutrition details safely
        nutrition_details = {item["Label"]: item["Value"] for item in safe_json_load(row.get("nutritions", ""), default=[]) if isinstance(item, dict)}

        recipes.append({
            "id": row.get("id", ""),  
            "title": row.get("title", ""),
            "image_url": row.get("image_url", ""),
            "cooking_time": row.get("cooking_time", ""),
            "recipe_type": row.get("recipe_type", ""),
            "ingredients_list": safe_json_load(row.get("ingredients", ""), default=[]),
            "directions_list": safe_json_load(row.get("directions", ""), default=[]),
            "servings": servings if servings else "N/A",  # ✅ Ensure servings is not empty
            "time_details": time_details,
            "nutrition_details": nutrition_details,
        })
    
    return recipes



# Home Page
def home(request):
    return render(request, 'index.html')

# Search Page
def search_page(request):
    return render(request, 'search.html')

# Function to paginate results
def paginate_data(request, data, per_page=12):
    paginator = Paginator(data, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return page_obj

# Search Results (Filters Recipes from CSV)
def search_results(request):
    recipes = load_recipes()

    ingredients = request.GET.get("ingredients", "").strip().lower()
    max_cook_time = request.GET.get("max_cook_time", "").strip()
    recipe_type = request.GET.get("recipe_type", "").strip().lower()
    max_calories = request.GET.get("max_calories", "").strip()  # New filter

    # Filter by ingredients
    if ingredients:
        ingredient_list = [ing.strip() for ing in ingredients.split(",")]
        recipes = [
            r for r in recipes 
            if any(ing in ", ".join(str(item) for item in r["ingredients_list"]).lower() for ing in ingredient_list)
        ]

    # Filter by cooking time
    if max_cook_time:
        try:
            max_time = int(max_cook_time)
            recipes = [r for r in recipes if str(r["cooking_time"]).isdigit() and int(r["cooking_time"]) <= max_time]
        except ValueError:
            pass  # Ignore invalid inputs

    # ✅ Corrected: Filter by recipe type
    if recipe_type:
        recipes = [r for r in recipes if r["recipe_type"].lower() == recipe_type]

    # 🔥 New: Filter by Calories
    if max_calories:
        try:
            max_calories = int(max_calories)
            recipes = [
                r for r in recipes if "Calories" in r["nutrition_details"]
                and str(r["nutrition_details"]["Calories"]).isdigit()
                and int(r["nutrition_details"]["Calories"]) <= max_calories
            ]
        except ValueError:
            pass  # Ignore invalid inputs

    page_obj = paginate_data(request, recipes)

    return render(request, 'results.html', {'recipes': page_obj})

# Recipe Detail Page
def recipe_detail(request, recipe_id):
    recipes = load_recipes()
    recipe = next((r for r in recipes if str(r["id"]) == str(recipe_id)), None)

    if not recipe:
        return render(request, "404.html", status=404)

    return render(request, "recipe_detail.html", {
        "recipe": recipe,
        "time_details": recipe.get("time_details", {}),
        "nutrition_details": recipe.get("nutrition_details", {}),
        "servings": recipe.get("servings", "N/A"),
    })

# Show Top Recipes
def top_recipes(request):
    query = request.GET.get("recipe_name", "").strip().lower()
    recipes = load_recipes()

    if query:
        recipes = [r for r in recipes if query in r["title"].lower()]

    page_obj = paginate_data(request, recipes)

    return render(request, 'top_recipes.html', {'recipes': page_obj, 'query': query})

# Search by Name Page
def search_by_name(request):
    return render(request, 'search_by_name.html')

def about(request):
    return render(request, 'about.html')

def help_page(request):
    return render(request, 'help.html')

def contact_page(request):
    return render(request, 'contact.html')

def coming_soon(request):
    return render(request, 'coming_soon.html')