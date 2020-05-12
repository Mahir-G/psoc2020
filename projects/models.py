from django.db import models

from mentors.models import Mentor

#model class for project
class Project(models.Model):
        title = models.CharField(max_length=80)
        description = models.TextField()
        code = models.CharField(max_length=5, default='')
        stack = models.CharField(max_length=100)
        mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)

        def __str__(self):
            return self.title