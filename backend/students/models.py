from django.db import models
from users.models import User





    
class Department(models.Model):
    code = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Course(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.name} ({self.code})"
    
class Subject(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='subjects')
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    units = models.DecimalField(max_digits=3, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} ({self.name}) - {self.department}"
    

class SubjectOffering(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='subject_offerings')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='offerings')


    def __str__(self):
        return f"{self.subject} - {self.department}"
    
class Schedule(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]
    TIME_CHOICES = [
        ('7:00-9:00 AM', '7:00-9:00 AM'),
        ('9:00-11:30 AM', '9:00-11:30 AM'),
        ('1:00-3:00 PM', '1:00-3:00 PM'),
        ('3:00-5:00 PM', '3:00-5:00 PM'),
        ('5:00-7:00 PM', '5:00-7:00 PM'),
    ]

    subject_offering = models.ForeignKey(SubjectOffering, on_delete=models.CASCADE, related_name='schedules')
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    time = models.CharField(max_length=20, choices=TIME_CHOICES, blank=True, null=True)
    instructor = models.CharField(max_length=100, blank=True, null=True)
    section = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True )

    def __str__(self):
        return f"{self.subject_offering} - {self.day} - {self.time} - {self.instructor}"
    

class StudentClearance(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
    ]
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clearances')
    registrar_approval = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    instructor_approval = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    dsa_approval = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.student} - {self.registrar_approval} - {self.instructor_approval} - {self.dsa_approval}"