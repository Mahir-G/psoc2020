# Generated by Django 3.0.3 on 2020-05-23 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentors', '0004_auto_20200524_0032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentor',
            name='linkedin',
            field=models.CharField(default='', max_length=100, null=True),
        ),
    ]
