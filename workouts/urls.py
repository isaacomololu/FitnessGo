from django.urls import path
from .views import workout, dashboard, create_workout
# url routes
urlpatterns = [
    path('workout/<int:workout_id>/', workout, name='workout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('create_workout/', create_workout, name='create_workout'),
]
