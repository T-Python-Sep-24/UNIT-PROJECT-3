from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from employee_leave.models import LeaveRequest
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from employee_leave.models import Profile


class UserCreationForm(forms.ModelForm):
    manager = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=True).exclude(username__in=['admin', 'shouq']),
        required=False,
        label="Manager"
    )

    group = forms.ModelChoiceField(
        queryset=Group.objects.exclude(name="HR"),
        initial=Group.objects.get(name="Employee"),
        required=True,
        label="User Role",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

            group = self.cleaned_data['group']
            user.groups.add(group)

            manager = self.cleaned_data['manager']
            profile = Profile.objects.create(user=user, manager=manager if manager else None)
            profile.save()

        return user

class EditUserForm(UserChangeForm):
    manager = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=True).exclude(username__in=['admin', 'shouq']),
        required=False,
        label="Manager"
    )

    hr = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='HR'),
        required=False,
        label="HR"
    )

    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        label="User Role"
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'manager', 'hr', 'group']

    def save(self, commit=True):
        user = super().save(commit=False)

        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

            group = self.cleaned_data['group']
            user.groups.clear()
            user.groups.add(group)

            manager = self.cleaned_data['manager']
            profile = user.profile
            if manager:
                profile.manager = manager

            hr = self.cleaned_data['hr']
            if hr:
                profile.hr = hr

            profile.save()

        return user


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['start_date', 'end_date', 'leave_type', 'reason', 'document', 'manager_reason' , 'hr']

    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    reason = forms.CharField(widget=forms.Textarea, required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.initial.get('leave_type'):
            self.initial['leave_type'] = 'sick'

        if 'leave_type' in self.data:
            if self.data.get('leave_type') == 'other':
                self.fields['reason'].required = True
            else:
                self.fields['reason'].required = False
        elif self.instance and self.instance.leave_type == 'other':
            self.fields['reason'].required = True


class ManagerCreationForm(forms.ModelForm):
    try:
        manager_group = Group.objects.get(name="Managers")
    except Group.DoesNotExist:
        manager_group = None

    if manager_group is None:
        raise ValueError("The 'Managers' group does not exist. Please create it before proceeding.")

    group = forms.ModelChoiceField(
        queryset=Group.objects.filter(name="Managers"),
        required=True,
        label="Role",
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial=manager_group
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True

        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

            group = self.cleaned_data['group']
            user.groups.add(group)

            profile = Profile.objects.create(user=user)
            profile.save()

        return user
    
class EditManagerForm(UserChangeForm):
    group = forms.ModelChoiceField(
        queryset=Group.objects.filter(name="Managers"),
        required=True,
        label="Role",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
    )
    
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password:
            if new_password != confirm_password:
                raise ValidationError("Password and Confirm Password must match.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True

        new_password = self.cleaned_data.get('new_password')
        if new_password:
            user.set_password(new_password)

        if commit:
            user.save()

            group = self.cleaned_data['group']
            user.groups.set([group])

            profile = Profile.objects.get(user=user)
            profile.save()

        return user
