from django.shortcuts import render, get_object_or_404

from vault.models import Project


def projects(request):
    project_list = Project.objects.order_by('name')
    context = {'project_list': project_list}
    return render(request, 'vault/projects.html', context)


def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'vault/project.html', {'project': project})


def create_project(request, project_id):
    return render(request, 'vault/project-detail.html')

def login(request):
    return render(request, 'vault/login.html')
