from django.shortcuts import render, redirect, get_object_or_404
from .models import Workout
from django.contrib.auth.decorators import login_required
from .forms import CustomWorkoutForm
from .models import CustomWorkout

# @login_required()
# def workouts(request, workout_id=None):
#     fitness_goal = request.user.profile.fitness_goal
#     recommended_workouts = Workout.objects.filter(profile=request.user.profile, profile__fitness_goal=fitness_goal)
#
#     if workout_id:
#         workout = get_object_or_404(Workout, pk=workout_id)
#         if request.method == 'POST':
#             form = CustomizeWorkoutForm(request.POST, instance=workout)
#             if form.is_valid():
#                 customized_workout = form.save(commit=False)
#                 customized_workout.user = request.user
#                 customized_workout.save()
#                 return redirect(to='dashboard')
#         else:
#             form = CustomizeWorkoutForm(instance=workout)
#         return render(request, 'customize_workouts', {'form': form, 'recommended_workouts': recommended_workouts})
#     return render(request, 'workout.html', {'recommended_workouts': recommended_workouts})


@login_required
def dashboard(request):
    all_workouts = Workout.objects.all()
    return render(request, 'dashboard.html', {'all_workouts': all_workouts})

@login_required
def create_workout(request):
    user_custom_workouts = CustomWorkout.objects.filter(user=request.user)
    print(user_custom_workouts)
    if request.method == 'POST':
        form = CustomWorkoutForm(request.POST)
        if form.is_valid():
            custom_workout = form.save(commit=False)
            custom_workout.user = request.user
            custom_workout.save()
            return redirect('dashboard')
    else:
        form = CustomWorkoutForm()
    return render(request, 'create_workout.html', {'user_custom_workouts':user_custom_workouts, 'form':form})

def workout(request, workout_id):
    workout_id = get_object_or_404(Workout, id=workout_id)
    return render(request, 'workout.html', {'workout_id':workout_id})