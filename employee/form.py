from django import forms
from employee.models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Confirm Password')
    profile_pic = forms.ImageField(label='Profile Picture', required=False)  # Add profile picture field to the form

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'user_type', 'department', 'job_title', 'hire_date', 'profile_pic']  # Include profile_pic in fields
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'user_type': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'hire_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        profile_pic = self.cleaned_data.get('profile_pic')  # Get the uploaded profile picture
        if profile_pic:
            user.profile_pic = profile_pic  # Save the profile picture to the user object
        if commit:
            user.save()
        return user
    
class LoginForm(forms.Form):
    email=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

class PerformanceMetricForm(forms.ModelForm):
    class Meta:
        model = PerformanceMetric
        fields = ['name', 'description', 'weight', 'category']
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "weight": forms.NumberInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"})
        }

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['employee_id', 'metric_id', 'start_date', 'target_date', 'description', 'status']
        widgets = {
            'employee_id': forms.Select(attrs={'class': 'form-control'}),
            'metric_id': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'target_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter employee_id queryset
        self.fields['employee_id'].queryset = CustomUser.objects.filter(user_type='employee')
        
        if user and user.user_type == 'employee':
            # Disable editing for all fields except status
            for field_name, field in self.fields.items():
                if field_name != 'status':
                    field.widget.attrs['readonly'] = True
                    # field.widget.attrs['disabled'] = True
class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['employee_id', 'metric_id', 'evaluation_date', 'self_score', 'manager_score', 'feedback']
        widgets = {
            'employee_id': forms.Select(attrs={'class': 'form-control'}),
            'metric_id': forms.Select(attrs={'class': 'form-control'}),
            'evaluation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'self_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'manager_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'feedback': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter employee_id queryset
        self.fields['employee_id'].queryset = CustomUser.objects.filter(user_type='employee')
        
        if user and user.user_type == 'employee':
            # Disable editing for all fields except status
            for field_name, field in self.fields.items():
                if field_name != 'self_score':
                    field.widget.attrs['readonly'] = True
class RewardForm(forms.ModelForm):
    class Meta:
        model = Reward
        fields = ['reward_name', 'reward_description', 'awarded_date','employee_id']
        widgets = {
            'reward_name': forms.TextInput(attrs={'class': 'form-control'}),
            'reward_description': forms.Textarea(attrs={'class': 'form-control'}),
            'awarded_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'employee_id': forms.Select(attrs={'class': 'form-control'}),
            
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        self.fields['employee_id'].queryset = CustomUser.objects.filter(user_type='employee')


class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ['name', 'description', 'completion_date', 'reward_id','employee_id']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'completion_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'reward_id':forms.Select(attrs={'class':'form-control'}),
            'employee_id':forms.Select(attrs={'class':'form-control'}),
            
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter employee_id field queryset based on user_type
        self.fields['employee_id'].queryset = CustomUser.objects.filter(user_type='employee')



class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'department', 'manager_id', 'creation_date','employees']

        widgets = {
                'name': forms.TextInput(attrs={'class': 'form-control'}),
                'department': forms.TextInput(attrs={'class': 'form-control'}),
                'manager_id': forms.Select(attrs={'class': 'form-control'}),
                'creation_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
                  'employees': forms.SelectMultiple(attrs={'class': 'form-control', 'size': 5})  # SelectMultiple widget
                
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        self.fields['manager_id'].queryset = CustomUser.objects.filter(user_type='manager')
        self.fields['employees'].queryset = CustomUser.objects.filter(user_type='employee')

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description', 'category']

        widgets = {
                'name': forms.TextInput(attrs={'class': 'form-control'}),
                'description': forms.Textarea(attrs={'class': 'form-control'}),
                'category': forms.TextInput(attrs={'class': 'form-control'}),
                
                
            }

class EmployeeSkillForm(forms.ModelForm):
    class Meta:
        model = EmployeeSkill
        fields = ['employee_id', 'skill_id', 'proficiency']

        widgets = {
                'employee_id': forms.Select(attrs={'class': 'form-control'}),
                'skill_id': forms.Select(attrs={'class': 'form-control'}),
                'proficiency': forms.Select(attrs={'class': 'form-control'}),
                
                
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter employee_id field queryset based on user_type
        self.fields['employee_id'].queryset = CustomUser.objects.filter(user_type='employee')


