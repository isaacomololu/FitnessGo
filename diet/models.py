from django.db import models


class DietPlan(models.Model):
    # Fields for the DietPlan model
    name = models.CharField(max_length=70)

    # Choices for fitness goals
    FITNESS_GOALS_CHOICES = [
        ('SF', 'Stay Fit'),
        ('LW', 'Lose Weight'),
        ('BM', 'Build Muscle'),
        ('KF', 'Keep Fit'),
        ('IE', 'Improve Endurance'),
    ]

    fitness_goal = models.CharField(
        max_length=20,
        choices=FITNESS_GOALS_CHOICES,
        default='SF'
    )

    # Meal plans for the day
    breakfast = models.TextField()
    lunch = models.TextField()
    dinner = models.TextField()
    snacks = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
