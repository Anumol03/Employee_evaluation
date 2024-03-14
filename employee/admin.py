from django.contrib import admin
from employee.models import *
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(PerformanceMetric)
admin.site.register(Goal)
admin.site.register(Assessment)
admin.site.register(Reward)
admin.site.register(Training)
admin.site.register(Team)
admin.site.register(Skill)
admin.site.register(EmployeeSkill)