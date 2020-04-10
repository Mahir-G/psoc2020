from django.db import models
from django.contrib.auth.models import User

#model class for mentor.
class Mentor(models.Model):
    name = models.CharField(max_length=64)
    phone = models.IntegerField()
    organisation = models.CharField(max_length=64)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name