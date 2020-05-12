from django.shortcuts import render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Mentee
from projects.models import Project
from mentors.forms import UserForm
from .forms import MenteeForm


#view for handling the registrations form for mentee.
class Register(View):
    form_class = UserForm
    registered = False
    template_name = 'mentees/register.html'
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'registered': self.registered})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            
            mentee = Mentee(user=user)
            mentee.save()

            self.registered = True
        else:
            print(form.errors)
        return render(request, self.template_name, {'form': form, 'registered': self.registered})


#view for handling the dashboard for mentee.
class DashBoard(View):
    template_name = 'mentees/dashboard.html'

    def get(self, request, *args, **kwargs):
        if hasattr(request.user, 'mentee'):
            return render(request, 'mentees/dashboard.html', {})
        else:
            return HttpResponse("You are not a mentee")

        
#view to handle profile section of mentee
class Profile(View):
    template_name = 'mentees/profile.html'
    form_class = MenteeForm

    def get(self, request, *args, **kwargs):
        if hasattr(request.user, 'mentee'):
            mentee = request.user.mentee
            if mentee.name==0 or mentee.phone==0 or mentee.organization==0:
                form = self.form_class()
            else:
                form = self.form_class(instance=mentee)
            return render(request, 'mentees/profile.html', {'form': form})
        else:
            return HttpResponse("You are not a mentee.")

    def post(self, request, *args, **kwargs):
        if hasattr(request.user, 'mentee'):
            mentee = request.user.mentee
            form = self.form_class(request.POST, instance=mentee)
            if form.is_valid:
                form.save()
            else:
                print(form.errors)
            return HttpResponseRedirect(reverse('mentees:dashboard'))
        else:
            return HttpResponse("You are not a mentee.")