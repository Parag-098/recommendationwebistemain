from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_page, name='search'),
    path('search-by-name/', views.search_by_name, name='search_by_name'),  # ✅ New path
    path('results/', views.search_results, name='results'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('top_recipes/', views.top_recipes, name='top_recipes'),  # ✅ This handles name search
]

