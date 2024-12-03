from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddMoneyToGoalForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import GoalForm
from .models import Goal
# Create your views here.



@login_required
def add_goal(request):
    if request.method == 'POST':
        if Goal.objects.filter(user=request.user).count() >= 3:
            messages.error(request, "You can only have 3 goals.")
            return redirect('home')

        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user  
            goal.save()
            messages.success(request, "Goal added successfully!")
            return redirect('home')  
    else:
        form = GoalForm()
    return render(request, 'goals/add_goal.html', {'form': form})





@login_required
def goal_detail(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    return render(request, 'goals/goal_detail.html', {'goal': goal})
