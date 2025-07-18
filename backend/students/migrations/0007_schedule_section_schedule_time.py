# Generated by Django 5.2.4 on 2025-07-13 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0006_rename_subject_schedule_subject_offering'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='section',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='schedule',
            name='time',
            field=models.CharField(blank=True, choices=[('7:00-9:00 AM', '7:00-9:00 AM'), ('9:00-11:30 AM', '9:00-11:30 AM'), ('1:00-3:00 PM', '1:00-3:00 PM'), ('3:00-5:00 PM', '3:00-5:00 PM'), ('5:00-7:00 PM', '5:00-7:00 PM')], max_length=20, null=True),
        ),
    ]
