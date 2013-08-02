from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('vault.views',
    # Examples:
    # url(r'^$', 'stockade.views.home', name='home'),
    # url(r'^stockade/', include('stockade.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'projects'),
	url(r'^login/$', 'login_view'),
    url(r'^logout/$', 'logout_view'),
	url(r'^project/(?P<project_id>\d+)/$', 'project_detail'),
	url(r'^project/new/$', 'create_project')
)
