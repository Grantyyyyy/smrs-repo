from django.contrib import admin
from .models import Course, Department, Subject, SubjectOffering, Schedule, StudentClearance




admin.site.register(StudentClearance)
admin.site.register(Course)
admin.site.register(Department)
admin.site.register(Subject)
admin.site.register(SubjectOffering)
admin.site.register(Schedule)