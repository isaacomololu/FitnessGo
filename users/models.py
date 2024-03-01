from django.db import models
from django.contrib.auth.models import User


# Define a user profile model extending from Django's Model class
class Profile(models.Model):
    # Link each profile to a User instance, using a one-to-one relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Additional profile fields
    age = models.PositiveIntegerField(blank=True, null=True)

    # Choices for gender field
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    # Define a CharField for gender with predefined choices
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,  # Make this field optional
    )

    # Choices for fitness goals
    FITNESS_GOALS_CHOICES = [
        ('SF', 'Stay Fit'),
        ('LW', 'Lose Weight'),
        ('BM', 'Build Muscle'),
        ('KF', 'Keep Fit'),
        ('IE', 'Improve Endurance'),
    ]

    # Define a CharField for fitness goals with default choice
    fitness_goal = models.CharField(
        max_length=20,
        choices=FITNESS_GOALS_CHOICES,
        default='SF'
    )

    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    # Displays the profile as the username
    def __str__(self):
        return self.user.username