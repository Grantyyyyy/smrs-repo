from django.contrib import admin
from .models import User, StudentProfile, AcademicYear, YearLevel, Course, Curriculum, Enrollment



admin.site.register(User)
admin.site.register(StudentProfile)
admin.site.register(AcademicYear)
admin.site.register(YearLevel)
admin.site.register(Course)
admin.site.register(Curriculum)
admin.site.register(Enrollment)
