from django import forms
from .models import CustomWorkout

class CustomWorkoutForm(forms.ModelForm):
    class Meta:
        model = CustomWorkout
        fields = ['name', 'description', 'exercises']

        labels = {
            'name': 'Workout Name',
            'description': 'Description',
            'exercises': 'Exercises',
        }

        help_texts = {
            'name': 'Enter a descriptive name for your workout.',
            'description': 'Provide additional details about your workout.',
            'exercises': 'List the exercises included in the workout.',
        }

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),  # Customize widget for multi-line input
        }
