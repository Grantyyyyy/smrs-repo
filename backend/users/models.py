from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser







class User(AbstractUser):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    ACCOUNT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved',),
    ]
    
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    account_status = models.CharField(max_length=10, choices=ACCOUNT_STATUS_CHOICES, default='pending')
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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    
    elementary_school = models.CharField(max_length=100, blank=True, null=True)
    high_school = models.CharField(max_length=100, blank=True, null=True)
    senior_high = models.CharField(max_length=100, blank=True, null=True)

@receiver(models.signals.post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.is_student:
        StudentProfile.objects.create(user=instance)











class DsaClearance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cleared = models.BooleanField(default=False)
    date_cleared = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Cleared: {self.cleared}"