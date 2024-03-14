

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from employee.form import *
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import View
from django.db.models import Avg
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

def home(request):
    return render(request, 'home.html')

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)  # Pass request.FILES to handle file data
        if form.is_valid():
            user = form.save()
            
            # You might want to log in the user here if needed
            return redirect('login')  # Redirect to the desired page after registration
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'login.html', {"form": form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            print()

            if user:
                login(request, user)
                messages.success(request, 'Login successful')
                return redirect('index')

        messages.error(request, 'Invalid credentials')
        return render(request, 'login.html', {"form": form})
    
@login_required
def create_performance_metric(request):
    if request.user.user_type == 'manager':  # Check if the user is a manager
        if request.method == 'POST':
            form = PerformanceMetricForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('performance_metric_list')
        else:
            form = PerformanceMetricForm()
        return render(request, 'create_performance.html', {'form': form})
    else:
        # Redirect or render an error message if the user is not a manager
        return render(request, 'error.html', {'message': 'You do not have permission to access this page.'})
@login_required
def edit_performance_metric(request, metric_id):
    # Retrieve the PerformanceMetric instance
    metric = get_object_or_404(PerformanceMetric, pk=metric_id)

    if request.method == 'POST':
        # Populate the form with the POST data and instance
        form = PerformanceMetricForm(request.POST, instance=metric)
        if form.is_valid():
            form.save()
            return redirect('create_performance')
    else:
        # Populate the form with the instance data for editing
        form = PerformanceMetricForm(instance=metric)

    return render(request, 'edit_performance_metric.html', {'form': form})
@login_required
def delete_performance_metric(request, metric_id):
    metric = get_object_or_404(PerformanceMetric, pk=metric_id)
    metric.delete()
    return redirect('create_performance')

@login_required
def create_goal(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('goal_list')  
    else:
        form = GoalForm()
    return render(request, 'create_goal.html', {'form': form})
@login_required
def edit_goal(request, goal_id):
    employee_id = request.user.id
    goal = get_object_or_404(Goal, pk=goal_id)
    
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('edit_goal', goal_id=goal_id)  # Redirect wherever you want after editing
    else:
        form = GoalForm(instance=goal, user=request.user)  # Pass request.user to the form
    
    return render(request, 'edit_goal.html', {'form': form, 'employee_id': employee_id})
@login_required
def edit_employee_goal(request, employee_id, goal_id):
    employee = get_object_or_404(CustomUser, pk=employee_id)
    goal = get_object_or_404(Goal, pk=goal_id)

    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('goal_list')  # Redirect wherever you want after editing
    else:
        form = GoalForm(instance=goal)

    return render(request, 'edit_goal.html', {'form': form, 'employee': employee})
@login_required
def delete_goal(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    goal.delete()
    return redirect('goal_list')

@login_required
def goal_detail(request, goal_id):
    # Retrieve the goal object from the database
    goal = get_object_or_404(Goal, pk=goal_id)
    
    # Retrieve the employee_id associated with the goal
    employee_id = goal.employee_id.id
    
    # Construct the URL for the goal_detail view
    url = reverse('goal_detail', kwargs={'goal_id': goal_id})
    
    return render(request, 'goal_detail.html', {'goal': goal, 'employee_id': employee_id, 'url': url})

@login_required
def edit_user(request, user_id):
    employee_id = request.user.id
    user = get_object_or_404(CustomUser, pk=user_id)

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            
            return redirect('edit_user')
    else:
        form = UserRegistrationForm(instance=user)

    return render(request, 'edit_user.html', {'form': form,'employee_id':employee_id})

@login_required
def performance_metric_list(request):
    
    performance_metrics = PerformanceMetric.objects.all()
    return render(request, 'performance_list.html', {'performance_metrics': performance_metrics})
@login_required
def goal_list(request):
    goals = Goal.objects.all()
    return render(request, 'goal_list.html', {'goals': goals})

@login_required
def create_assessment(request):
    if request.method == 'POST':
        form = AssessmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('assessment_list')  
    else:
        form = AssessmentForm()
    return render(request, 'assessment_create.html', {'form': form})
@login_required
def assessment_list(request):
    assessments = Assessment.objects.all()
    return render(request, 'assessment_list.html', {'assessments': assessments})


@login_required
def edit_assessment(request, assessment_id):
    employee_id = request.user.id  # Fetch the employee_id from request.user
    assessment = get_object_or_404(Assessment, pk=assessment_id)

    if request.method == 'POST':
        form = AssessmentForm(request.POST, instance=assessment, user=request.user)  # Pass user to the form
        if form.is_valid():
            form.save()
            return redirect('assessment_edit', assessment_id=assessment_id)
        else:
            # Print form errors for debugging
            print(form.errors)
    else:
        form = AssessmentForm(instance=assessment, user=request.user)

    return render(request, 'edit_assessment.html', {'form': form, 'employee_id': employee_id})
@login_required
def delete_assessment(request, assessment_id):
    assessment = get_object_or_404(Assessment, pk=assessment_id)
    assessment.delete()
    return redirect('assessment_list')

@login_required
def create_reward(request):
    if request.method == 'POST':
        form = RewardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reward_list')  
    else:
        form = RewardForm()
    return render(request, 'reward_create.html', {'form': form})
@login_required
def employee_rewards(request, employee_id):
    # Retrieve goals belonging to the specified employee_id
    employee_rewards = Reward.objects.filter(employee_id=employee_id)
    
    return render(request, 'employee_rewards.html', {'employee_rewards': employee_rewards,'employee_id':employee_id})
@login_required
def list_rewards(request):
    rewards = Reward.objects.all()  
    return render(request, 'reward_list.html', {'rewards': rewards})
@login_required
def edit_reward(request, reward_id):
    # Get the reward object or return a 404 error if not found
    reward = get_object_or_404(Reward, pk=reward_id)

    if request.method == 'POST':
        # Populate the form with the POST data and instance of the reward object
        form = RewardForm(request.POST, instance=reward)
        if form.is_valid():
            form.save()
            return redirect('reward_list')  # Redirect to the list view after successful edit
    else:
        # If it's a GET request, render the form with the populated reward data
        form = RewardForm(instance=reward)

    return render(request, 'reward_edit.html', {'form': form})
@login_required
def delete_reward(request, reward_id):
    reward = get_object_or_404(Reward, pk=reward_id)
    reward.delete()
    return redirect('reward_list')

@login_required
def create_training(request):
    if request.method == 'POST':
        form = TrainingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('training_list')  
    else:
        form = TrainingForm()
    return render(request, 'training_create.html', {'form': form})

@login_required
def list_trainings(request):
    trainings = Training.objects.all()  
    return render(request, 'training_list.html', {'trainings': trainings})
@login_required
def edit_training(request, training_id):
    # Get the training object or return a 404 error if not found
    training = get_object_or_404(Training, pk=training_id)

    if request.method == 'POST':
        # Populate the form with the POST data and instance of the training object
        form = TrainingForm(request.POST, instance=training)
        if form.is_valid():
            form.save()
            return redirect('training_list')  # Redirect to the list view after successful edit
    else:
        # If it's a GET request, render the form with the populated training data
        form = TrainingForm(instance=training)

    return render(request, 'training_edit.html', {'form': form})
@login_required
def delete_training(request, training_id):
    training = get_object_or_404(Training, pk=training_id)
    training.delete()
    return redirect('training_create')
@login_required
def create_team(request):
    form = TeamForm()  # Define form outside the conditional block
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_team') 
    return render(request, 'team_create.html', {'form': form})
@login_required
def team_detail(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    print(team_id)
    return render(request, 'team_detail.html', {'team': team})
    

@login_required
def create_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('skill_list') 
    else:
        form = SkillForm()
    return render(request, 'skill_create.html', {'form': form})
@login_required
def skill_list(request):
    employee_id = request.user.id
    skills = Skill.objects.all()
    return render(request, 'skill_list.html', {'skills': skills,'employee_id':employee_id})
@login_required
def delete_skill(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)
    skill.delete()
    return redirect('skill_list')
@login_required
def edit_skill(request, skill_id):
    # Get the skill object or return a 404 error if not found
    skill = get_object_or_404(Skill, pk=skill_id)

    if request.method == 'POST':
        # Populate the form with the POST data and instance of the skill object
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('skill_list')  # Redirect to the list view after successful edit
    else:
        # If it's a GET request, render the form with the populated skill data
        form = SkillForm(instance=skill)

    return render(request, 'skill_edit.html', {'form': form})

@login_required
def create_employee_skill(request):
    if request.method == 'POST':
        form = EmployeeSkillForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_skill_list')  
    else:
        form = EmployeeSkillForm()
    return render(request, 'employee_skill_create.html', {'form': form})
@login_required
def employee_skill_list(request):
    employee_id = request.user.id
    employee_skills = EmployeeSkill.objects.all()
    return render(request, 'employee_skill_list.html', {'employee_skills': employee_skills,'employee_id':employee_id})
@login_required
def edit_employee_skill(request, pk):
    employee_skill = get_object_or_404(EmployeeSkill, pk=pk)
    if request.method == 'POST':
        form = EmployeeSkillForm(request.POST, instance=employee_skill)
        if form.is_valid():
            form.save()
            return redirect('employee_skill_list')  # Redirect to the list view after successful edit
    else:
        form = EmployeeSkillForm(instance=employee_skill)
    return render(request, 'employee_skill_edit.html', {'form': form})
@login_required
def delete_employee_skill(request, pk):
    employee_skill = get_object_or_404(EmployeeSkill, pk=pk)
    employee_skill.delete()
    return redirect('employee_skill_list')
@login_required
def index(request):
    if request.user.is_authenticated:
        employee_id = request.user.id
        try:
            # Retrieve the first goal associated with the user
            goal = Goal.objects.filter(employee_id=request.user.id).first()
            if goal:
                goal_id = goal.id
            else:
                goal_id = None
        except ObjectDoesNotExist:
            goal_id = None
        return render(request, 'index.html', {'employee_id': employee_id, 'goal_id': goal_id})
    else:
        return render(request, 'index.html')

def base(request):
    return render(request,'base.html')
@login_required
def logout_view(request):
    logout(request)
    # Redirect to a specific URL after logout
    return redirect('login') 
@login_required
def performance_metrics(request, employee_id):
    # Check if the employee exists
    employee = get_object_or_404(CustomUser, pk=employee_id)

    # Get all performance metrics
    metrics = PerformanceMetric.objects.all()
    performance_scores = {}
    total_score = 0  # Initialize total score

    for metric in metrics:
        # Initialize average_score to None
        average_score = None

        # Filter assessments for the current metric and employee
        assessments = Assessment.objects.filter(employee_id=employee_id, metric_id=metric)

        if assessments.exists():
            # Calculate average self score and manager score
            self_score_avg = assessments.aggregate(Avg('self_score'))['self_score__avg']
            manager_score_avg = assessments.aggregate(Avg('manager_score'))['manager_score__avg']

            # Calculate the average score
            if self_score_avg is not None and manager_score_avg is not None:
                average_score = (self_score_avg + manager_score_avg) / 2
            elif self_score_avg is not None:
                average_score = self_score_avg
            elif manager_score_avg is not None:
                average_score = manager_score_avg

            # Apply weight
            if average_score is not None:
                weighted_score = average_score * metric.weight
                total_score += weighted_score  # Add the weighted score to the total score
            else:
                weighted_score = None

            performance_scores[metric.name] = weighted_score
        else:
            # Handle case where no assessments are available
            performance_scores[metric.name] = None

    # Check if the total score is less than 25 and set a warning message
    warning_message = None
    if total_score < 25:
        warning_message = "Warning: Total score is less than 25."

    return render(request, 'performance_metrics.html', {'employee': employee, 'performance_scores': performance_scores, 'total_score': total_score, 'warning_message': warning_message ,'employee_id': employee_id})
@login_required
def employee_skills_by_employee(request, employee_id):
    # Retrieve all EmployeeSkill objects for the given employee ID
    employee_skills = EmployeeSkill.objects.filter(employee_id=employee_id)
    return render(request, 'employee_skill_list_id.html', {'employee_skills': employee_skills,'employee_id':employee_id})

@login_required
def employee_goals(request, employee_id):
    # Retrieve goals belonging to the specified employee_id
    employee_goals = Goal.objects.filter(employee_id=employee_id)
    
    return render(request, 'employee_goals.html', {'employee_goals': employee_goals,'employee_id': employee_id})
@login_required
def employee_training(request, employee_id):
    # Retrieve goals belonging to the specified employee_id
    employee_training = Training.objects.filter(employee_id=employee_id)
    
    return render(request, 'employee_training.html', {'employee_training': employee_training, 'employee_id':employee_id})
@login_required
def employee_skill(request, employee_id):
    # Retrieve goals belonging to the specified employee_id
    employee_skill = EmployeeSkill.objects.filter(employee_id=employee_id)
    
    return render(request, 'employee_skill.html', {'employee_skill': employee_skill,'employee_id':employee_id})
@login_required
def employee_assessment(request, employee_id):
    # Retrieve goals belonging to the specified employee_id
    employee_assessment = Assessment.objects.filter(employee_id=employee_id)
    
    return render(request, 'employee_assessment.html', {'employee_assessment': employee_assessment,'employee_id': employee_id})

@login_required
def user_detail(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    return render(request, 'user_detail.html', {'user': user})