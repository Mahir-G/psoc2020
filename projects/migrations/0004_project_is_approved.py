# Generated by Django 3.0.3 on 2020-05-23 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_remove_project_mentees'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
