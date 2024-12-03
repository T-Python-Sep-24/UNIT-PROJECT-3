from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ExpenseForm, BudgetForm, SalaryForm
from .models import Expense, Budget
from users.models import User


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('home')  
    else:
        form = ExpenseForm()
    return render(request, 'finances/add_expense.html', {'form': form})


@login_required
def add_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('home') 
    else:
        form = BudgetForm()
    return render(request, 'finances/add_budget.html', {'form': form})


@login_required
def add_salary(request):
    if request.method == 'POST':
        form = SalaryForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')  
    else:
        form = SalaryForm(instance=request.user)
    return render(request, 'finances/add_salary.html', {'form': form})


