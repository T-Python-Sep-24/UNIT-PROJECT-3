from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .models import User
from finances.models import Expense, Budget
from goals.models import Goal
from groups.models import GroupGoal, GroupExpense
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db import models
from goals.forms import AddMoneyToGoalForm
from decimal import Decimal
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import Profile
from django.utils import timezone
from .utils import update_user_savings  
# Create your views here.





@login_required
def home(request):
    user = request.user

    total_expenses = user.expenses.aggregate(total_spent=Sum('amount'))['total_spent'] or Decimal(0)
    salary = user.salary or Decimal(0)
    user.savings = salary
    remaining_savings = user.savings - total_expenses

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
        user.expenses
            .values('category')
            .annotate(total_spent=Sum('amount'))
    )
    CATEGORY_CHOICES_DICT = dict(Expense._meta.get_field('category').choices)
    for expense in expense_summary:
        expense['category_name'] = CATEGORY_CHOICES_DICT.get(expense['category'], 'Unknown')

    group = user.groups.first()  

    if group:
        group_goal_summary = GroupGoal.objects.filter(group=group)
        group_goal_data = [
            {
                'id': goal.id,
                'name': goal.name,
                'progress': min(goal.progress(), 100),
                'current_amount': goal.current_amount,
                'target_amount': goal.target_amount,
                'deadline': goal.deadline,
            }
            for goal in group_goal_summary
        ]

        group_expense_summary = GroupExpense.objects.filter(group=group)
        group_expense_data = [
            {
                'category': expense.get_category_display(),
                'amount': expense.amount,
                'contributed_amount': expense.contributed_amount,
                'remaining_amount': expense.remaining_amount,
                'created_by': expense.created_by.username,
            }
            for expense in group_expense_summary
        ]
    else:
        group_goal_data = []
        group_expense_data = []

    if request.method == 'POST' and 'add_money_to_goal' in request.POST:
        goal_id = request.POST.get('goal_id')
        amount = Decimal(request.POST.get('amount'))
        try:
            goal = Goal.objects.get(id=goal_id, user=user)
            if remaining_savings >= amount:
                contributed_amount = min(amount, goal.target_amount - goal.current_amount)
                goal.current_amount += contributed_amount
                goal.save()

                Expense.objects.create(
                    user=user,
                    category="goal_contributions",
                    amount=contributed_amount,
                    date=timezone.now(),
                    note=f"Contribution to goal: {goal.name}"
                )

                remaining_savings = update_user_savings(user, contributed_amount)  

                if goal.progress() >= 100:
                    messages.success(request, f"Goal {goal.name} is now complete!")
                else:
                    messages.success(request, f"Added ${contributed_amount} to your goal: {goal.name}")
            else:
                messages.error(request, "Insufficient savings to add money to goal.")
        except Goal.DoesNotExist:
            messages.error(request, "Goal not found.")


    if request.method == 'POST' and 'add_expense' in request.POST:
        category = request.POST.get('category')
        amount = Decimal(request.POST.get('amount'))
        date = request.POST.get('date')
        note = request.POST.get('note', '')

        try:
            budget = Budget.objects.get(user=user, category=category)
        except Budget.DoesNotExist:
            budget = None

        if budget:
            total_expenses_for_category = user.expenses.filter(category=category).aggregate(Sum('amount'))['amount__sum'] or Decimal(0)
            total_expenses_for_category += amount  

            if total_expenses_for_category > budget.monthly_limit:
                messages.error(request, f"Expense exceeds your budget for {category}.")
            else:
                Expense.objects.create(
                    user=user,
                    category=category,
                    amount=amount,
                    date=date,
                    note=note
                )
                remaining_savings = update_user_savings(user, amount) 
                messages.success(request, "Expense added successfully.")
        else:
            Expense.objects.create(
                user=user,
                category=category,
                amount=amount,
                date=date,
                note=note
            )
            remaining_savings = update_user_savings(user, amount)  
            messages.success(request, "Expense added successfully.")


    return render(request, 'users/home.html', {
        'total_expenses': total_expenses,
        'remaining_savings': remaining_savings,
        'salary': salary,
        'goal_summary': goal_data,
        'expense_summary': expense_summary,
        'group_goal_summary': group_goal_data,
        'group_expense_summary': group_expense_data,
    })
















def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)  
        if form.is_valid():
            user = form.save()  
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home') 
        else:
            messages.error(request, 'Error creating account. Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You have successfully logged in!')
            return redirect('home')  
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out.')
        return redirect('home')  
    return redirect('home')



@login_required
def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'users/user_profile.html', {'user': user})
