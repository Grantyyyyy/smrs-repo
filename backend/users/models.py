from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser




class AcademicYear(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return f"{self.start_year}-{self.end_year} ({self.status})"

class YearLevel(models.Model):
    YEAR_CHOICES = [
        ('1st Year', '1st Year'),
        ('2nd Year', '2nd Year'),
        ('3rd Year', '3rd Year'),
        ('4th Year', '4th Year'),
    ] 
    LEVEL_CHOICES = [
        ('1st Semester', '1st Semester'),
        ('2nd Semester', '2nd Semester'),
    ]
    year = models.CharField(max_length=10, choices=YEAR_CHOICES, default='1st Year')
    level = models.CharField(max_length=15, choices=LEVEL_CHOICES, default='1st Semester')

    def __str__(self):
        return f"{self.year} - {self.level}"
    
class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Curriculum(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='curriculums')
    year = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.course.name} ({self.year})"
    

class User(AbstractUser):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    
    is_student = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    is_dsa = models.BooleanField(default=False)

    @property
    def user_type(self):
        if self.is_student:
            return 'student'
        elif self.is_instructor:
            return 'instructor'
        elif self.is_dsa:
            return 'dsa'
        return 'unknown'

class StudentProfile(models.Model):
    STUDENT_TYPE_CHOICES = [
        ('Freshman', 'Freshman'),
        ('Transferee', 'Transferee'),
    ]

    ACCOUNT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved',),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    account_status = models.CharField(max_length=10, choices=ACCOUNT_STATUS_CHOICES, default='Pending')
    student_type = models.CharField(max_length=10, choices=STUDENT_TYPE_CHOICES, default='Freshman')

    date_of_birth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_contact = models.CharField(max_length=15, blank=True, null=True)
    
    elementary_school = models.CharField(max_length=100, blank=True, null=True)
    high_school = models.CharField(max_length=100, blank=True, null=True)
    senior_high = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.last_name}, {self.user.first_name} - {self.student_type}"

@receiver(models.signals.post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.is_student:
        StudentProfile.objects.create(user=instance)



class Enrollment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='enrollments')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='enrollments')
    year_level = models.ForeignKey(YearLevel, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments_made', null=True, blank=True)
    enrollment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.academic_year.start_year}-{self.academic_year.end_year} ({self.year_level.year} - {self.year_level.level})"
