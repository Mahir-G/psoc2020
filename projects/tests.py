from django.test import TestCase

from .models import Project
from mentors.models import Mentor
from django.contrib.auth.models import User

# Create your tests here.
class ProjectModelTests(TestCase):
    
    def setUp(self):

        #create user
        u1 = User.objects.create(username='test', password='test')

        #create mentor
        m1 = Mentor.objects.create(name='test', phone=9999988888, organisation='test', user=u1)

        #create projects
        p1 = Project.objects.create(title='title1', description='description1', code='code01', stack='teststack1', mentor=m1)
        p1 = Project.objects.create(title='title2', description='description2', code='code02', stack='teststack2', mentor=m1)
        p1 = Project.objects.create(title='title3', description='description3', code='code03', stack='teststack3', mentor=m1)
        p1 = Project.objects.create(title='title4', description='description4', code='code04', stack='teststack4', mentor=m1)

    def test_has_at_most_three_projects(self):
        """ Mentor can have at most three projects """
        m = Mentor.objects.get(user=User.objects.get(username='test'))
        self.assertTrue(m.project_set.all().count()<=3)
