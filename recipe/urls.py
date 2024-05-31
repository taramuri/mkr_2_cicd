from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
]
