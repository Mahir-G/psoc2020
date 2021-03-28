from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import Project
from mentees.models import Proposal


#view for the main page
class Main(View):
    template_name = 'projects/main.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


#view for the list of projects
class Index(View):
    template_name = 'projects/index.html'
    proposal_list = {}

    def get_proposal_list(self, project_id):
        project = Project.objects.get(pk=project_id)
        for proposal in project.proposal_set.all():
            self.proposal_list[proposal.mentee.user.username] = proposal.proposal_link
        return self.proposal_list

    def get(self, request, *args, **kwargs):
        projects = Project.objects.filter(is_approved='True')
        projects_details = []
        project_detail = {}
        for project in projects:
            project_detail['project'] = project
            proposal_list = self.get_proposal_list(project.id)
            project_detail['proposal_list'] = proposal_list
            projects_details.append(project_detail)
        return render(request, self.template_name, {'projects':projects, 'projects_details': projects_details, 'proposals': self.proposal_list})


#view for the details page of each project
class ProjectDetail(View):
    template_name = 'projects/detail.html'
    is_mentee = False
    is_mentor = False
    is_max_count_not_reached = True
    already_applied = False
    proposal_list = {}

    def get(self, request, *args, **kwargs):
        project = Project.objects.get(pk=kwargs['pk'])
        if project.is_approved:
            if hasattr(request.user, 'mentee'):
                self.is_mentee = True
                if request.user.mentee.projects.all().count()>=3:
                    self.is_max_count_not_reached = False
                if project in request.user.mentee.projects.all():
                    self.already_applied = True
            if hasattr(request.user, 'mentor'):
                if (project.mentor == request.user.mentor):
                    self.is_mentor = True
                    for proposal in project.proposal_set.all():
                        self.proposal_list[proposal.mentee.user.username] = proposal.proposal_link
            return render(request, self.template_name, {'project': project, 'is_mentee': self.is_mentee,'is_mentor': self.is_mentor, 'not_reached': self.is_max_count_not_reached, 'already_applied': self.already_applied, 'proposals': self.proposal_list})
        return HttpResponse("Error 404: Page not Found")

    def post(self, request, *args, **kwargs):
        if hasattr(request.user, 'mentee'):
            mentee = request.user.mentee
            project = Project.objects.get(pk=kwargs['pk'])
            proposal_link = request.POST.get('proposal_link')
            
            if mentee.projects.all().count()<3:
                mentee.projects.add(project)
                proposal = Proposal(mentee=mentee, project=project, proposal_link=proposal_link)
                proposal.save()
                return HttpResponseRedirect(reverse('projects:detail', args=(project.id,)))
            else:
                return HttpResponse("Cannot apply for another project.")


class AdminIndex(View):
    template_name = 'projects/adminindex.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            projects = Project.objects.all()
            return render(request, self.template_name, {'projects':projects})
        else:
            return HttpResponse("You are not authorized to access this page.")

class AdminProjectDetail(View):
    template_name = 'projects/admindetail.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            project = Project.objects.get(pk=kwargs['pk'])
            return render(request, self.template_name, {'project': project})
        else:
            return HttpResponse("You are not authorized to access this page.")

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            project = Project.objects.get(pk=kwargs['pk'])
            project.is_approved = True
            project.save()
            return redirect('admin_panel_project_detail', project.id)
        else:
            return HttpResponse("You are not authorized to access this page.")


def conduct(request):

    return render(request, 'projects/conduct.html')

def psoc2020(request):

    return render(request, 'projects/psoc2020.html')
