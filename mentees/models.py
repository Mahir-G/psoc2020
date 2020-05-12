from django.db import models
from django.contrib.auth.models import User

from projects.models import Project

#model class for mentee
class Mentee(models.Model):
    name = models.CharField(max_length=64, default=0)
    organization = models.CharField(max_length=64, default=0)
    phone = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_mentor = models.BooleanField(default=False)
    projects = models.ManyToManyField(Project, related_name='mentee_applications')
    selected = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, related_name='selected_mentee')

    def __str__(self):
        return self.user.username