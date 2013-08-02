# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from vault.models import Project


def projects(request):
    project_list = Project.objects.order_by('name')
    context = {'project_list': project_list}
    return render_to_response('vault/projects.html', context,
            context_instance=RequestContext(request))


def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render_to_response('vault/project.html', {'project': project},
            context_instance=RequestContext(request))


def create_project(request):
    return render_to_response('vault/project-dialog.html',
        context_instance=RequestContext(request))


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
        else:
            # Return a 'disabled account' error message
            pass
    else:
        # Return an 'invalid login' error message.
        pass
