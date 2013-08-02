# Create your views here.
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from vault.forms import ProjectForm
from vault.models import Project


@login_required
def projects(request):
    project_list = Project.objects.order_by('name')
    num_projects = len(project_list)
    context = {'project_list': project_list, 'num_projects': num_projects}
    return render_to_response('vault/projects.html', context,
            context_instance=RequestContext(request))


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render_to_response('vault/project.html', {'project': project},
            context_instance=RequestContext(request))


@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = Project()
            project.name = form.cleaned_data['project_name']
            project.description = form.cleaned_data['project_desc']
            project.owner = request.user
            project.save()
            return HttpResponse(
                json.dumps({'success': 'Great Success!'}),
                content_type='application/json',
                status=201
            )
    return HttpResponse(
        json.dumps({'error': 'Epic Fail.'}),
        content_type='application/json',
        status=400
    )


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect('/')
            else:
                # Return a 'disabled account' error message
                return render_to_response('vault/login.html', {'error': 'Account is disabled'},
					  context_instance=RequestContext(request))
        else:
            # Return an 'invalid login' error message.
            return render_to_response('vault/login.html', {'error': 'Invalid login'},
                                      context_instance=RequestContext(request))
    else:
        return render_to_response('vault/login.html',  context_instance=RequestContext(request))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def search_users(request, username):
    return json.dumps(["Pawl", username])
