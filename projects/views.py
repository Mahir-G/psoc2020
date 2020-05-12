from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import Project


#view for the main page
class Main(View):
    template_name = 'projects/main.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


#view for the list of projects
class Index(View):
    template_name = 'projects/index.html'

    def get(self, request, *args, **kwargs):
        projects = Project.objects.all()
        return render(request, self.template_name, {'projects':projects})


#view for the details page of each project
class ProjectDetail(View):
    template_name = 'projects/detail.html'
    is_mentee = False
    is_max_count_not_reached = True
    already_applied = False

    def get(self, request, *args, **kwargs):
        project = Project.objects.get(pk=kwargs['pk'])
        if hasattr(request.user, 'mentee'):
            self.is_mentee = True
            if request.user.mentee.projects.all().count()>=3:
                self.is_max_count_not_reached = False
            if project in request.user.mentee.projects.all():
                self.already_applied = True
        return render(request, self.template_name, {'project': project, 'is_mentee': self.is_mentee, 'not_reached': self.is_max_count_not_reached, 'already_applied': self.already_applied})

    def post(self, request, *args, **kwargs):
        if hasattr(request.user, 'mentee'):
            mentee = request.user.mentee
            project = Project.objects.get(pk=kwargs['pk'])
            
            if mentee.projects.all().count()<3:
                mentee.projects.add(project)
                return HttpResponseRedirect(reverse('projects:detail', args=(project.id,)))
            else:
                return HttpResponse("Cannot apply for another project.")
