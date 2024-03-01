from django.shortcuts import render
from .models import DietPlan


def diet(request):
    # Retrieve all diet plans
    diet_plans = DietPlan.objects.all()

    # Render the 'diet.html' template with the retrieved diet plans
    return render(request, 'diet.html', {'diet_plans': diet_plans})
