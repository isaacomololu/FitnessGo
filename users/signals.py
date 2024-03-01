from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# Signal to create a profile when a new user is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Signal to save the profile when a user is saved
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    # Check if the user has a profile before saving
    if hasattr(instance, 'profile'):
        instance.profile.save()
