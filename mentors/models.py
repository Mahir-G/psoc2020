from django.db import models
from django.contrib.auth.models import User

#model class for mentor.

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.username, filename)

class Mentor(models.Model):
    name = models.CharField(max_length=64, default="")
    linkedin = models.CharField(max_length=100, null=True, default="")
    cv = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_mentor = models.BooleanField(default=True)

    def __str__(self):
        return self.name