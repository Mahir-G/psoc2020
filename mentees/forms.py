from django.forms import ModelForm, CharField, PasswordInput 

from .models import Mentee

class MenteeForm(ModelForm):
    class Meta():
        model = Mentee
        fields = ['name', 'phone', 'organization']