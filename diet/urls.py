from django.urls import path
from .views import diet

urlpatterns = [
    path('diet/', diet, name='diet'),
]
