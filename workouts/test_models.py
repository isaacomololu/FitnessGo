from django.db import models
import re
import bcrypt
from decimal import Decimal

class UserManager(models.Manager):
    def register(self, **kwargs):
        errors = []

        if len(kwargs["username"][0]) < 2:
            errors.append('Username is required and must be at least 2 characters long.')

        USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9!@#$%^&*()?]*$')

        if not USERNAME_REGEX.match(kwargs["username"][0]):
            errors.append('Username must contain letters, numbers and basic characters only.')

        if len(User.objects.filter(username=kwargs["username"][0])) > 0:
            errors.append('Username is already registered to another user.')

        if len(kwargs["email"][0]) < 5:
            errors.append('Email field must be at least 5 characters.')
        else:
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
            if not EMAIL_REGEX.match(kwargs["email"][0]):
                errors.append('Email field is not a valid email format.')
            else:
                if len(User.objects.filter(email=kwargs["email"][0])) > 0:
                    errors.append('Email address is already registered to another user.')

        if len(kwargs["password"][0]) < 8 or len(kwargs["password_confirmation"][0]) < 8:
            errors.append('Password fields are required and must be at least 8 characters.')
        else:
            if kwargs["password"][0] != kwargs["password_confirmation"][0]:
                errors.append('Password and confirmation must match.')

        if kwargs["tos_accept"][0] == "on":
            kwargs["tos_accept"][0] = True
        else:
            errors.append("Terms of service must be accepted.")

        if len(errors) == 0:
            kwargs["password"][0] = bcrypt.hashpw((kwargs["password"][0]).encode(), bcrypt.gensalt(14))
            validated_user = {
                "logged_in_user": User(username=kwargs["username"][0], email=kwargs["email"][0], password=kwargs["password"][0], tos_accept=kwargs["tos_accept"][0]),
            }
            validated_user["logged_in_user"].save()
            return validated_user
        else:
            for error in errors:
                print("Validation Error: ", error)
            errors = {
                "errors": errors,
            }
            return errors

    def login(self, **kwargs):
        errors = []

        if len(kwargs["username"][0]) < 1 or len(kwargs["password"][0]) < 1:
            errors.append('All fields are required.')
        else:
            try:
                logged_in_user = User.objects.get(username=kwargs["username"][0])
                try:
                    password = kwargs["password"][0].encode()
                    hashed = logged_in_user.password.encode()
                    if not (bcrypt.checkpw(password, hashed)):
                        print("ERROR: PASSWORD IS INCORRECT")
                        errors.append("Username or password is incorrect.")
                except ValueError:
                    errors.append('This user is corrupt. Please contact the administrator.')
            except User.DoesNotExist:
                print("ERROR: USERNAME IS INVALID")
                errors.append('Username or password is incorrect.')

        if len(errors) == 0:
            validated_user = {
                "logged_in_user": logged_in_user,
            }
            return validated_user
        else:
            for error in errors:
                print("Validation Error: ", error)
            errors = {
                "errors": errors,
            }
            return errors

class WorkoutManager(models.Manager):
    def new(self, **kwargs):
        errors = []

        if len(kwargs["name"]) < 2:
            errors.append('Name is required and must be at least 2 characters long.')

        WORKOUT_REGEX = re.compile(r'^\s*[A-Za-z0-9!@#$%^&*"\':;/?,<.>()-_=+\]\[~`]+(?:\s+[A-Za-z0-9!@#$%^&*"\':;/?,<.>()-_=+\]\[~`]+)*\s*$')

        if not WORKOUT_REGEX.match(kwargs["name"]):
            errors.append('Name must contain letters, numbers and basic characters only.')

        if len(kwargs["description"]) < 2:
            errors.append('Description is required and must be at least 2 characters long.')

        if not WORKOUT_REGEX.match(kwargs["description"]):
            errors.append('Description must contain letters, numbers and basic characters only.')

        if len(errors) == 0:
            validated_workout = {
                "workout": Workout(name=kwargs["name"], description=kwargs["description"], user=kwargs["user"]),
            }
            validated_workout["workout"].save()
            return validated_workout
        else:
            for error in errors:
                print("Validation Error: ", error)
            errors = {
                "errors": errors,
            }
            return errors

    def update(self, **kwargs):
        errors = []

        if len(kwargs["name"]) < 2:
            errors.append('Name is required and must be at least 2 characters long.')

        WORKOUT_REGEX = re.compile(r'^\s*[A-Za-z0-9!@#$%^&*"\':;/?,<.>()-_=+\]\[~`]+(?:\s+[A-Za-z0-9!@#$%^&*"\':;/?,<.>()-_=+\]\[~`]+)*\s*$')

        if not WORKOUT_REGEX.match(kwargs["name"]):
            errors.append('Name must contain letters, numbers and basic characters only.')

        if len(kwargs["description"]) < 2:
            errors.append('Description is required and must be at least 2 characters long.')

        if not WORKOUT_REGEX.match(kwargs["description"]):
            errors.append('Description must contain letters, numbers and basic characters only.')

        if len(errors) == 0:
            workout = Workout.objects.filter(id=kwargs['workout_id']).update(name=kwargs['name'], description=kwargs["description"])
            updated_workout = {
                "updated_workout": workout
            }
            return updated_workout
        else:
            for error in errors:
                print("Validation Error: ", error)
            errors = {
                "errors": errors,
            }
            return errors

class ExerciseManager(models.Manager):
    def new(self, **kwargs):
        errors = []

        if not kwargs['name'] or not kwargs['weight'] or not kwargs['repetitions']:
            errors.append('All fields are required.')

        if len(kwargs["name"]) < 2:
            errors.append('Name is required and must be at least 2 characters long.')

        EXERCISE_REGEX = re.compile(r'^\s*[A-Za-z0-9!@#$%^&*"\':;/?,<.>()-_=+\]\[~`]+(?:\s+[A-Za-z0-9!@#$%^&*"\':;/?,<.>()-_=+\]\[~`]+)*\s*$')

        if not EXERCISE_REGEX.match(kwargs["name"]):
            errors.append('Name must contain letters, numbers and basic characters only.')

        try:
            kwargs["weight"] = round(float(kwargs["weight"]), 1)
            kwargs["repetitions"] = round(float(kwargs["repetitions"]), 1)
            if (kwargs["weight"] < 0) or (kwargs["repetitions"] < 0):
                errors.append('Weight and repetitions must be a positive number.')
        except ValueError:
            errors.append('Weight and repetitions must be a positive number only, containing at most one decimal place.')

        if len(errors) == 0:
            validated_exercise = {
                "exercise": Exercise(name=kwargs["name"], weight=kwargs["weight"], repetitions=kwargs["repetitions"], workout=kwargs["workout"]),
            }
            validated_exercise["exercise"].save()
            return validated_exercise
        else:
            for error in errors:
                print("Validation Error: ", error)
            errors = {
                "errors": errors,
            }
            return errors

class User(models.Model):
    username = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=22)
    tos_accept = models.BooleanField(default=False)
    level = models.IntegerField(default=1)
    level_name = models.CharField(max_length=15, default="Newbie")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Workout(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WorkoutManager()

class Exercise(models.Model):
    name = models.CharField(max_length=50)
    weight = models.DecimalField(max_digits=999, decimal_places=1)
    repetitions = models.DecimalField(max_digits=999, decimal_places=1)
    category = models.CharField(max_length=50, default="Strength Training")
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ExerciseManager()
