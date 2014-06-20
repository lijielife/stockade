# Create your views here.
import json

from barbicanclient import client
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from vault.forms import ProjectForm
from vault.models import Project, Secret, ProjectMember


@login_required
def projects(request):
    project_list = request.user.project_set.all()
    num_projects = len(project_list)
    context = {'project_list': project_list, 'num_projects': num_projects}
    return render_to_response('vault/projects.html', context,
            context_instance=RequestContext(request))


@login_required
def project_table(request):
    project_list = request.user.project_set.all()
    num_projects = len(project_list)
    context = {'project_list': project_list,
               'num_projects': num_projects}
    return render_to_response('vault/projects_table.html', context,
            context_instance=RequestContext(request))


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project not in request.user.project_set.all():
        raise PermissionDenied
    return render_to_response('vault/project.html', {'project': project},
            context_instance=RequestContext(request))


@login_required
def project_edit(request, project_id):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = get_object_or_404(Project, pk=project_id)
            name = form.cleaned_data['project_name']
            if name:
                project.name = name
            description = form.cleaned_data['project_desc']
            if description:
                project.description = description
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


@login_required
def secrets_table(request):
    if request.method != 'POST':
        return HttpResponse(
            json.dumps({'error': 'Post at me, bro!'}),
            content_type='application/json',
            status=400
        )
    project_id = request.POST.get('project_id')
    if not project_id:
        return HttpResponse(
            json.dumps({'error': 'Invalid project.'}),
            content_type='application/json',
            status=400
        )
    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        return HttpResponse(
            json.dumps({'error': 'Invalid project.'}),
            content_type='application/json',
            status=400
        )
    if project not in request.user.project_set.all():
        return HttpResponse(
            json.dumps({'error': "Don't hack me, bro!"}),
            content_type='application/json',
            status=401
        )
    return render_to_response('vault/secrets_table.html', {'project': project},
            context_instance=RequestContext(request))


@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = Project()
            project.name = form.cleaned_data['project_name']
            project.description = form.cleaned_data['project_desc']
            project.save()
            project_member = ProjectMember()
            project_member.project = project
            project_member.user = request.user
            project_member.owner = True
            project_member.save()
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


@login_required
def create_secret(request):
    # TODO Make sure user is part of the project
    if request.method == 'POST':
       project_id = request.POST.get('project_id')
    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        return HttpResponse(
            json.dumps({'error': 'Invalid project.'}),
            content_type='application/json',
            status=400
        )

    description = request.POST.get('description')
    password = request.POST.get('password')

    if description == '' or password == '':
        return HttpResponse(
            json.dumps({'error': 'Invalid description or password.'}),
            content_type='application/json',
            status=400
        )

    secret = Secret()
    secret.project = project
    secret.category = request.POST.get('category')
    secret.description = description
    secret.username = request.POST.get('username')
    secret.url = request.POST.get('url')
    secret.last_user = request.user


    secret.secret_ref = _store_secret_as_plain_text(secret, password)
    secret.save()

    return HttpResponse(
        json.dumps({'success': 'Great Success!'}),
        content_type='application/json',
        status=201
    )


@login_required
def fetch_secret(request):
    if request.method != 'POST':
        return HttpResponse(
            json.dumps({'error': 'Post at me, bro!'}),
            content_type='application/json',
            status=400
        )
    secret_id = request.POST.get('secret_id')
    secrets = Secret.objects.filter(pk=secret_id)
    if not secrets or not len(secrets):
        return HttpResponse(
            json.dumps({'error': 'Not in this castle'}),
            content_type='application/json',
            status=401
        )
    if request.user not in secrets[0].project.members.all():
        return HttpResponse(
            json.dumps({'error': 'Not found'}),
            content_type='application/json',
            status=404
        )

    payload = _decrypt_secret_as_plain_text(secrets[0].secret_ref)

    # keystone_username = 'demo'
    # auth_token = 'be1526d82e5e496e8a037ade5a3616cd'
    # barbican_endpoint = 'http://api-02-int.cloudkeep.io:9311/v1'
    # conn = client.Connection('keystone.com', keystone_username, 'password', 'demo',
    #              token=auth_token,
    #              endpoint=barbican_endpoint)
    # payload = conn.get_raw_secret_by_id(secret.secret_id, 'text/plain')

    return HttpResponse(json.dumps({'payload': payload}), content_type='application_json')


@login_required
def secret_edit(request, secret_id):
    if request.method == 'POST':

        secrets = Secret.objects.filter(pk=secret_id)
        if not secrets or not len(secrets):
            return HttpResponse(
                json.dumps({'error': 'Not in this castle'}),
                content_type='application/json',
                status=401
            )
        secret_db = secrets[0]

        if request.user not in secret_db.project.members.all():
            return HttpResponse(
                json.dumps({'error': 'Not found'}),
                content_type='application/json',
                status=404
            )

        description = request.POST.get('description')
        passwordNew = request.POST.get('password')
        if description == '' or passwordNew == '':
            return HttpResponse(
                json.dumps({'error': 'Invalid description or password.'}),
                content_type='application/json',
                status=400
            )

        secret = Secret()
        secret.id = secret_db.id
        secret.secret_ref = secret_db.secret_ref
        secret.create_date = secret_db.create_date
        secret.project = secret_db.project
        secret.category = request.POST.get('category') or secret_db.category
        secret.description = description or secret_db.description
        secret.username = request.POST.get('username') or secret_db.username
        secret.url = request.POST.get('url') or secret_db.url
        secret.last_user = request.user

        # If the password changed, then need to create a new secret in Barbican.
        passwordCurrent = _decrypt_secret_as_plain_text(secret_db.secret_ref)
        if passwordNew and passwordCurrent != passwordNew:
            secret.secret_ref = _store_secret_as_plain_text(secret, passwordNew)

        secret.save()
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


@login_required
def delete_secret(request):
    secret_id = request.POST.get('secret_id')
    secrets = Secret.objects.filter(pk=secret_id)
    if not secrets or not len(secrets):
        return HttpResponse(
            json.dumps({'error': 'Not in this castle'}),
            content_type='application/json',
            status=401
        )

    if request.user not in secrets[0].project.members.all():
        return HttpResponse(
            json.dumps({'error': 'Not found'}),
            content_type='application/json',
            status=404
        )

    secrets[0].delete()

    return HttpResponse(
        json.dumps({'success': 'Great Success!'}),
        content_type='application/json',
        status=201
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


def _store_secret_as_plain_text(secret, password):
    barbican_client = _get_barbican_client()
    return barbican_client.secrets.store(name=secret.description,
                                         payload=password,
                                         payload_content_type='text/plain',
                                         payload_content_encoding=None,
                                         algorithm=None,
                                         bit_length=None,
                                         mode=None,
                                         expiration=None)

    # TODO(jwood) Iff Keystone auth is utilized.
    # keystone_username = 'demo'
    # auth_token = 'be1526d82e5e496e8a037ade5a3616cd'
    # barbican_endpoint = 'http://api-02-int.cloudkeep.io:9311/v1'
    # conn = client.Connection('keystone.com', keystone_username, 'password', 'demo',
    #              token=auth_token,
    #              endpoint=barbican_endpoint)
    # secret.secret_ref = conn.create_secret('text/plain',
    #             plain_text=password).secret_ref


def _decrypt_secret_as_plain_text(secret_ref):
    barbican_client = _get_barbican_client()
    return barbican_client.secrets.decrypt(secret_ref)


def _get_barbican_client():
    return client.Client(endpoint=settings.BARBICAN['endpoint'], 
                         tenant_id=settings.BARBICAN['tenant_id'])
