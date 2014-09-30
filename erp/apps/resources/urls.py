from django.conf.urls import patterns, url


urlpatterns = patterns('erp.apps.resources.views',
    url(r'^$', 'resource_list', name='resource_list'),
    url(r'^(\d+)/$', 'resource_details', name='resource_details'),
    url(r'^update/(\d+)/$', 'resource_update', name='resource_update'),
    url(r'^create/$', 'resource_create', name='resource_create'),
    #url(r'^(?P<id>\d+)/edit/$', 'resource_edit', name='editResource'),
)