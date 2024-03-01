from django.db import models
from django.contrib.auth.models import User


class Workout(models.Model):
    # Fields for the Workout model
    name = models.CharField(max_length=40)
    description = models.TextField()
    duration = models.PositiveIntegerField()
    duration_unit = models.CharField(
        max_length=10,
        choices=[
            ('seconds', 'Seconds'),
            ('minutes', 'Minutes'),
            ('hours', 'Hours'),
        ],
        default='minutes'
    )
    exercises = models.ManyToManyField('Exercise', related_name='workouts')
    completed = models.BooleanField(default=False)

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

    # Choices for intensity levels
    INTENSITY_LEVELS = [
        ('L', 'Low'),
        ('M', 'Moderate'),
        ('V', 'Vigorous')
    ]
    intensity = models.CharField(
        max_length=20,
        choices=INTENSITY_LEVELS,
        default='M'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def get_duration_in_minutes(self):
        # Calculate and return the duration in minutes based on the unit
        if self.duration_unit == 'seconds':
            return self.duration / 60
        elif self.duration_unit == 'hours':
            return self.duration * 60
        else:
            return self.duration

    def save(self, *args, **kwargs):
        # Custom save method to ensure default exercises if less than 3
        super().save(*args, **kwargs)
        if self.exercises.count() < 3:
            default_exercises_count = 3 - self.exercises.count()
            for _ in range(default_exercises_count):
                # Create and add default exercises
                exercise = Exercise.objects.create(name="Exercise", description="Exercise description", weight=0,
                                                   equipment_required="None", difficulty_level='M', repetitions=5,
                                                   sets=3)
                self.exercises.add(exercise)

    def __str__(self):
        return self.name


class Exercise(models.Model):
    # Fields for the Exercise model
    name = models.CharField(max_length=40)
    description = models.TextField()
    weight = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)  # Adjusted precision
    equipment_required = models.CharField(max_length=50, null=True, blank=True, default='None')

    # Choices for difficulty levels
    DIFFICULTY_LEVELS = [
        ('VH', 'Very Hard'),
        ('H', 'Hard'),
        ('M', 'Moderate'),
        ('E', 'Easy')
    ]
    difficulty_level = models.CharField(
        max_length=20,
        choices=DIFFICULTY_LEVELS,
        default='M'
    )

    repetitions = models.PositiveIntegerField(null=True, blank=True)
    sets = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class CustomWorkout(models.Model):
    # Fields for the CustomWorkout model
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField()
    exercises = models.ManyToManyField(Exercise, related_name='custom_workouts')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
