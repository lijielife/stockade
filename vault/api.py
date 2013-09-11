
from tastypie.resources import ModelResource
from models import Project, Secret, ProjectMember
from django.contrib.auth.models import User
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication, MultiAuthentication
from tastypie.authorization import DjangoAuthorization




class ProjectResource(ModelResource):
    class Meta:
        queryset = Project.objects.all()
        resource_name = 'projects'
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        authorization = DjangoAuthorization()


class SecretResource(ModelResource):
    class Meta:
        queryset = Secret.objects.all()
        resource_name = 'secrets'
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        authorization = DjangoAuthorization()


class ProjectMemberResource(ModelResource):
    class Meta:
        queryset = ProjectMember.objects.all()
        resource_name = 'memberships'
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        authorization = DjangoAuthorization()


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        authorization = DjangoAuthorization()

