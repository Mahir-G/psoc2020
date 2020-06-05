from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import User, Mentor
from projects.models import Project
from mentees.models import Mentee
from .forms import MentorForm, UserForm
from projects.forms import ProjectForm

# view to handle the registration form for mentors
class Register(View):
    form_class = UserForm
    registered = False
    template_name = 'mentors/register.html'
    errors = []

    def get(self, request, *args, **kwargs):
        self.errors = []
        return render(request, self.template_name, {'registered': self.registered})

    def post(self, request, *args, **kwargs):
        data = {
            'username': request.POST.get('username'),
            'email': request.POST.get('email'),
            'password': request.POST.get('password')
        }
        self.errors=[]
        form = self.form_class(data=data)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()

            mentor = Mentor(user=user)
            mentor.save()

            self.registered = True
        else:
            self.errors.append(form.errors)
        return render(request, self.template_name, {'form': form, 'registered': self.registered, 'errors': self.errors})


# view to handle login
class Login(View):
    template_name = 'mentors/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = authenticate(username=username, password=password)
        except:
            messages.add_message(request, messages.ERROR, 'Invalid Username or Password')

        if user:
            if user.is_active:
                login(request, user)
                if hasattr(request.user, 'mentor'):
                    return HttpResponseRedirect(reverse('mentors:dashboard'))
                elif hasattr(request.user, 'mentee'):
                    return HttpResponseRedirect(reverse('mentees:dashboard'))
                else:
                    messages.add_message(request, messages.ERROR, 'You are Admin')
            else:
                messages.add_message(request, messages.ERROR, 'Your Account was Inactive')
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(
                username, password))
            messages.add_message(request, messages.ERROR, 'Invalid Username or Password')
        return render(request, self.template_name)


# view to handle logout of users
class LogOut(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('main_page'))


# view to handle the dashboard of mentors
class DashBoard(View):
    template_name = 'mentors/dashboard.html'
    show_button = True

    def get(self, request, *args, **kwargs):
        if hasattr(request.user, 'mentor'):
            if not ((request.user.mentor.name !="") and (request.user.mentor.linkedin !="" or request.user.mentor.cv !="")):
                return redirect('mentors:profile')
            else:
                if (request.user.mentor.project_set.all().count() >= 3):
                    self.show_button = False
                return render(request, 'mentors/dashboard.html', {'show_button': self.show_button})
        else:
            return HttpResponse("You are not a mentor")

    def post(self, request, *args, **kwargs):
        if hasattr(request.user, 'mentor'):
            project_id = request.POST.get('project')
            project = Project.objects.get(pk=project_id)

            pk = request.POST.get('mentee_id')
            mentee = Mentee.objects.get(pk=pk)

            if mentee.selected == None:
                mentee.selected = project
                mentee.save()
                return HttpResponseRedirect(reverse('projects:detail', args=(project_id,)))

            else:
                return HttpResponse('This mentee is already selected for another project.')
        else:
            return HttpResponse("You are not a mentor")


# view to handle profile section of mentor
class Profile(View):
    template_name = 'mentors/profile.html'
    form_class = MentorForm

    def get(self, request, *args, **kwargs):
        if hasattr(request.user, 'mentor'):
            mentor = request.user.mentor
            data = {
                'name': mentor.name,
                'linkedin': mentor.linkedin,
                'github': mentor.github,
            }
            if mentor.cv == "":
                data['display'] = 'block'
            else:
                data['display'] = 'none'
            return render(request, 'mentors/profile.html', {'data': data})
        else:
            return HttpResponse("You are not a mentor.")

    def post(self, request, *args, **kwargs):
        if hasattr(request.user, 'mentor'):
            mentor = request.user.mentor
            name = request.POST.get('name')
            linkedin = request.POST.get('linkedin')
            github = request.POST.get('github')
            if mentor.cv == "":
                cv = request.FILES['CV']

            mentor.name = name
            mentor.linkedin = linkedin
            mentor.github = github
            if mentor.cv == "":
                mentor.cv = cv
            mentor.save()
            return HttpResponseRedirect(reverse('mentors:dashboard'))
        else:
            return HttpResponse("You are not a mentor.")


# implemented the view to create a new project by a mentor
class CreateProject(View):
    template_name = 'mentors/create_project.html'
    form_class = ProjectForm

    def get(self, request, *args, **kwargs):
        if hasattr(request.user, 'mentor'):
            return render(request, 'mentors/create_project.html')
        else:
            return HttpResponse("You are not a mentor")

    def post(self, request, *args, **kwargs):
        if hasattr(request.user, 'mentor'):
            title = request.POST.get('title')
            description = request.POST.get('description')
            stack = request.POST.get('stack')

            if (title!="" and description!="" and stack!="") and request.user.mentor.project_set.all().count() < 3:
                new_project = Project(title=title, description=description, stack=stack)
                new_project.mentor = request.user.mentor
                if Project.objects.all().count() < 10:
                    new_project.code = 'PSOC0' + \
                        str(Project.objects.all().count())
                else:
                    new_project.code = 'PSOC' + \
                        str(Project.objects.all().count())
                new_project.save()
            else:
                return HttpResponse("Can only add 3 projects")
            return HttpResponseRedirect(reverse('mentors:dashboard'))
        else:
            return HttpResponse('You are not a mentor.')
