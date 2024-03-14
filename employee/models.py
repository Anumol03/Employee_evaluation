from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = [
        ('employee', 'Employee'),
        ('manager', 'Manager'),
        # Add more choices as needed
    ]

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    user_type = models.CharField(max_length=255, choices=USER_TYPE_CHOICES)
    department = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    hire_date = models.DateField()
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, null=True)  # Add profile picture field
    
    # Add any other fields you need

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'user_type', 'department', 'job_title', 'hire_date']

    # Provide related_name for the ManyToManyField
    groups = models.ManyToManyField('auth.Group', related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='customuser_set', blank=True)

    def __str__(self):
        return self.email


class PerformanceMetric(models.Model):
    CATEGORY_CHOICES = [
        ('technical', 'Technical Skills'),
        ('teamwork', 'Teamwork'),
        ('communication', 'Communication'),
        # Add more choices as needed
    ]
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    weight = models.FloatField(null=False)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, null=False)

    class Meta:
        unique_together = ('name', 'category')

    def __str__(self):
        return self.name    
    


class Goal(models.Model):
    STATUS_CHOICES = [
        ('In progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Overdue', 'Overdue'),
     
    ]

    employee_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    metric_id = models.ForeignKey(PerformanceMetric, on_delete=models.CASCADE)
    start_date = models.DateField(null=False)
    target_date = models.DateField(null=False)
    description = models.TextField(null=False)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, null=False)

    def __str__(self):
        return f" Metric: {self.metric_id}, Status: {self.status}"  

class Assessment(models.Model):
    employee_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    metric_id = models.ForeignKey(PerformanceMetric, on_delete=models.CASCADE)
    evaluation_date = models.DateField(null=False)  
    self_score = models.FloatField(default='0')
    manager_score = models.FloatField(null=False)
    feedback = models.TextField(null=False)  


class Reward(models.Model):
    reward_name =models.CharField(max_length=100,null=False)
    reward_description =models.TextField(null=False)
    awarded_date =models.DateField(null=False)
    employee_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    def __str__(self):
        return self.reward_name   
    
class Training(models.Model):
    name=models.CharField(max_length=200,null=False)
    description =models.TextField(null=False)
    completion_date =models.DateField(null=False)
    reward_id=models.ForeignKey(Reward,on_delete=models.CASCADE)
    employee_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)



    def __str__(self) :
        return self.name
class Team(models.Model):
    name=models.CharField(max_length=100,null=False)
    department=models.CharField(max_length=100,null=False)
    manager_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    creation_date=models.DateField(null=False)
    employees = models.ManyToManyField(CustomUser, related_name='teams')

    def __str__(self) :
        return self.name
    
class Skill(models.Model):
    name=models.CharField(max_length=100,null=False)
    description=models.TextField(null=False)
    category=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class EmployeeSkill(models.Model):
    employee_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    skill_id=models.ForeignKey(Skill,on_delete=models.CASCADE)
    proficiency = models.CharField(max_length=20,null=False,default='Beginner' ,choices=[
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Expert', 'Expert'),
    ])





