from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from finances.models import Expense, Budget, Category
from goals.models import Goal
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db import models
from goals.forms import AddMoneyToGoalForm
from decimal import Decimal
from django.utils.timezone import now
# Create your views here.



@login_required
def home(request):
    user = request.user

    total_expenses = Expense.objects.filter(user=user).aggregate(total_spent=Sum('amount'))['total_spent'] or Decimal(0)
    salary = user.salary or Decimal(0)
    remaining_savings = salary - total_expenses
    goal_summary = Goal.objects.filter(user=user)
    goal_data = [
        {
            'id': goal.id,
            'name': goal.name,
            'progress': min(goal.progress(), 100),  
            'current_amount': goal.current_amount,
            'target_amount': goal.target_amount,
            'deadline': goal.deadline,
        }
        for goal in goal_summary
    ]

    expense_summary = list(
        Expense.objects.filter(user=user)
        .values('category__name')
        .annotate(total_spent=Sum('amount'))
    )

    if request.method == 'POST' and 'add_money_to_goal' in request.POST:
        goal_id = request.POST.get('goal_id')
        amount = Decimal(request.POST.get('amount'))
        try:
            goal = Goal.objects.get(id=goal_id, user=user)
            if remaining_savings >= amount:
                contributed_amount = min(amount, goal.target_amount - goal.current_amount)
                goal.current_amount += contributed_amount
                goal.save()

                expense_category, _ = Category.objects.get_or_create(name="Goal Contributions")
                Expense.objects.create(
                    user=user,
                    category=expense_category,
                    amount=contributed_amount,
                    date=now(),
                    note=f"Contribution to goal: {goal.name}"
                )
                remaining_savings -= contributed_amount

                if goal.progress() >= 100:
                    messages.success(request, f"Goal {goal.name} is now complete!")
                else:
                    messages.success(request, f"Added ${contributed_amount} to your goal: {goal.name}")
            else:
                messages.error(request, "Insufficient savings to add money to goal.")
        except Goal.DoesNotExist:
            messages.error(request, "Goal not found.")

    return render(request, 'users/home.html', {
        'total_expenses': total_expenses,
        'remaining_savings': remaining_savings,
        'salary': salary,
        'goal_summary': goal_data,
        'expense_summary': expense_summary,
    })





def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You have successfully logged in!')
            return redirect('home')  
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            messages.success(request, 'Account created successfully!')
            return redirect('home')  
        else:
            messages.error(request, 'Error creating account. Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'users/signup.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':  
        logout(request)
        messages.success(request, 'You have been logged out.')
        return redirect('home')  
    return redirect('home')