# Generated by Django 5.2.4 on 2025-07-13 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_schedule'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='subject',
            new_name='subject_offering',
        ),
    ]
