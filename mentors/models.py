from django.db import models
from django.contrib.auth.models import User

#model class for mentor.
class Mentor(models.Model):
    name = models.CharField(max_length=64, default=0)
    phone = models.IntegerField(default=0)
    organisation = models.CharField(max_length=64, default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_mentor = models.BooleanField(default=True)

    def __str__(self):
        return self.name