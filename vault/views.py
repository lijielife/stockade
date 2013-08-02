# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

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
    return render_to_response('vault/project-dialog.html',
        context_instance=RequestContext(request))


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
