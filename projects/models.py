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

        # modified save function to only save projects if and only if the count of projects under one mentor
        # is less than or equal to 3
        def save(self, *args, **kwargs):
            if Mentor.objects.get(pk=self.mentor.id).project_set.all().count()<3:
                super().save(*args, **kwargs)
            else:
                print("already three projects, can't add another")
                return
