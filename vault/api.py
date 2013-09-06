# myapp/api.py
from tastypie.resources import ModelResource
from models import Project, Secret, ProjectMember
from django.contrib.auth.models import User



class ProjectResource(ModelResource):
    class Meta:
        queryset = Project.objects.all()
        resource_name = 'projects'


class SecretResource(ModelResource):
    class Meta:
        queryset = Secret.objects.all()
        resource_name = 'secrets'


class ProjectMemberResource(ModelResource):
    class Meta:
        queryset = ProjectMember.objects.all()
        resource_name = 'membership'


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'