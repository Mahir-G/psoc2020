from django.forms import ModelForm, CharField, PasswordInput 
from django.contrib.auth.models import User

from .models import Mentor

class UserForm(ModelForm):
    password = CharField(widget=PasswordInput())
    class Meta():
        model = User
        fields = ['username', 'password', 'email']

class MentorForm(ModelForm):
    class Meta():
        model = Mentor
        fields = ['name', 'phone', 'organisation']