# myapp/urls.py
from django.urls import path
from .views import data_entry, visualize_data, attribute_trainer, home

urlpatterns = [
    path('add/', data_entry, name='data_entry'),
    path("display_data/", visualize_data, name="visualize_data"),
    path('practice/', attribute_trainer, name='attribute_trainer'),
    path('', home, name="home")
    # Add other URL patterns as needed
]
