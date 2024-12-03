from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Group, GroupExpense, GroupGoal, GroupMembership, GroupInvitation, Contribution
from finances.models import   Expense
from .forms import GroupForm, GroupExpenseForm, GroupGoalForm, JoinGroupForm, GroupInvitationForm
from django.core.mail import send_mail
from decimal import Decimal
from django.urls import reverse
from django.http import Http404
from django.db.models import Sum
from users.utils import update_user_savings, update_user_savings
from django.utils.timezone import now
import uuid
import string
import random
# Create your views here.




@login_required
def group_list(request):
    groups = Group.objects.filter(
        members=request.user
    ) | Group.objects.filter(owner=request.user)
    return render(request, 'groups/group_list.html', {'groups': groups})


def generate_unique_code():
    while True:
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        if not Group.objects.filter(unique_code=code).exists():
            return code

@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.owner = request.user
            group.unique_code = generate_unique_code()  
            group.save()
            group.members.add(request.user)
            messages.success(request, 'Group created successfully!')
            return redirect('groups:group_list')
    else:
        form = GroupForm()
    return render(request, 'groups/create_group.html', {'form': form})





@login_required
def join_group(request):
    if request.method == 'POST':
        form = JoinGroupForm(request.POST)
        if form.is_valid():
            unique_code = form.cleaned_data['unique_code']
            try:
                group = Group.objects.get(unique_code=unique_code)
                if request.user in group.members.all():
                    messages.info(request, 'You are already a member of this group.')
                else:
                    group.members.add(request.user)
                    messages.success(request, f'You have joined the group "{group.name}"!')
                return redirect('groups:group_list')  
            except Group.DoesNotExist:
                messages.error(request, 'Invalid group code. Please try again.')
    else:
        form = JoinGroupForm()
    return render(request, 'groups/join_group.html', {'form': form})


@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    goal = group.goal if hasattr(group, 'goal') else None
    expense = group.expense if hasattr(group, 'expense') else None
    
    total_spent = request.user.expenses.aggregate(total_spent=Sum('amount'))['total_spent'] or Decimal(0)
    remaining_savings = request.user.savings - total_spent

    

    if request.method == "POST":
        is_for_goal = request.POST.get("is_for_goal") == "True"
        contribution_amount = Decimal(request.POST.get("amount", 0))
        user_share = 0
        if is_for_goal and goal:
            user_share = goal.target_amount / group.members.count() if group.members.count() > 0 else 0
        elif not is_for_goal and expense:
            user_share = expense.amount / group.members.count() if group.members.count() > 0 else 0

        if contribution_amount > remaining_savings:
            messages.error(request, "You don't have enough savings to contribute this amount.")
        elif contribution_amount > user_share:
            messages.error(request, "Contribution exceeds your required share.")
        else:
            if is_for_goal and goal:
                if contribution_amount > goal.target_amount - goal.current_amount:
                    messages.error(request, "Contribution exceeds the remaining goal amount.")
                else:
                    contribution, created = Contribution.objects.get_or_create(
                        group=group,
                        user=request.user,
                        is_for_goal=True,
                        defaults={"amount": contribution_amount},
                    )
                    if not created:
                        contribution.amount += contribution_amount
                        contribution.save()

                    goal.current_amount += contribution_amount
                    goal.save()

                    remaining_savings = update_user_savings(request.user, contribution_amount)

                    category_name = "Goal Contributions"  
                    Expense.objects.create(
                        user=request.user,
                        category=category_name,
                        amount=contribution_amount,
                        date=now(),
                        note=f"Contribution to goal: {goal.name}"
                    )

                    messages.success(request, f"Successfully contributed ${contribution_amount} to the goal.")

            elif not is_for_goal and expense:
                if contribution_amount > expense.remaining_amount:
                    messages.error(request, "Contribution exceeds the remaining expense amount.")
                else:
                    contribution, created = Contribution.objects.get_or_create(
                        group=group,
                        user=request.user,
                        is_for_goal=False,
                        defaults={"amount": contribution_amount},
                    )
                    if not created:
                        contribution.amount += contribution_amount
                        contribution.save()

                    expense.contributed_amount += contribution_amount
                    expense.save()

                    remaining_savings = update_user_savings(request.user, contribution_amount)

                    category_name = expense.get_category_display()  
                    Expense.objects.create(
                        user=request.user,
                        category=category_name,
                        amount=contribution_amount,
                        date=now(),
                        note=f"Contribution to group expense: {expense.get_category_display()}"
                    )

                    messages.success(request, f"Successfully contributed ${contribution_amount} to the expense.")

    return render(request, 'groups/group_detail.html', {
        'group': group,
        'goal': goal,
        'expense': expense,
        'remaining_savings': remaining_savings,
        'users': group.members.all(),
    })
















@login_required
def accept_invitation(request, group_id, token):
    invitation = get_object_or_404(GroupInvitation, group_id=group_id, token=token)

    group = invitation.group
    if group.owner == request.user:
        messages.success(request, "You have successfully joined the group.")
        group.members.add(request.user)  
        return redirect("groups:group_detail", group_id=group.id)
    else:
        messages.error(request, "Invalid invitation.")
        return redirect("groups:group_detail", group_id=group.id)





@login_required
def add_or_update_goal(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if not request.user == group.owner:
        messages.error(request, "Only the group owner can set or update goals.")
        return redirect('groups:group_detail', group_id=group_id)

    try:
        goal = group.goal
    except GroupGoal.DoesNotExist:
        goal = None

    if request.method == "POST":
        form = GroupGoalForm(request.POST, instance=goal)
        if form.is_valid():
            new_goal = form.save(commit=False)
            new_goal.group = group
            new_goal.save()
            messages.success(request, "Goal successfully set!")
            return redirect('groups:group_detail', group_id=group_id)
    else:
        form = GroupGoalForm(instance=goal)

    return render(request, 'groups/add_goal.html', {'form': form, 'group': group})






def add_or_update_expense(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if not request.user in group.members.all() and request.user != group.owner:
        messages.error(request, "You are not authorized to add or update expenses for this group.")
        return redirect('groups:group_detail', group_id=group.id)

    try:
        expense = group.expense  
    except GroupExpense.DoesNotExist:
        expense = None

    if request.method == "POST":
        form = GroupExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            new_expense = form.save(commit=False)
            new_expense.group = group
            new_expense.created_by = request.user
            new_expense.save()
            messages.success(request, "Expense saved successfully!")
            return redirect('groups:group_detail', group_id=group.id)
    else:
        form = GroupExpenseForm(instance=expense)

    return render(request, 'groups/add_expense.html', {'form': form, 'group': group})




@login_required
def add_member(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if group.owner != request.user:
        messages.error(request, "Only the group owner can add members.")
        return redirect("groups:group_detail", group_id=group_id)

    if request.method == "POST":
        form = GroupInvitationForm(request.POST)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.group = group
            invitation.save()
            invite_url = request.build_absolute_uri(
                reverse("groups:accept_invitation", args=[invitation.token])
            )
            send_mail(
                subject=f"You are invited to join the group: {group.name}",
                message=f"Hi! You've been invited to join the group '{group.name}'. "
                        f"Click the link to join: {invite_url}",
                from_email="admin@example.com",
                recipient_list=[invitation.email],
            )

            messages.success(request, f"Invitation sent to {invitation.email}.")
            return redirect("groups:group_detail", group_id=group_id)
    else:
        form = GroupInvitationForm()

    return render(request, "groups/add_member.html", {"form": form, "group": group})

