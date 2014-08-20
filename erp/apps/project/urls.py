from django.conf.urls import patterns, include, url


urlpatterns = patterns('erp.apps.project.views',

    url(r'^$', 'project_list', name='project_list', kwargs={'list_type':'active'}),

    url(r'^l/(?P<list_type>\w+)/$', 'project_list', name='project_list'),

    url(r'^(\d+)/$', 'project_details', name='project_details'),
    url(r'^(\d+)/edit/$', 'project_edit', name='project_edit'),

    url(r'^delete/(\d+)/?$', 'project_delete', name='project_delete'),
    url(r'^create/$', 'project_create', name='project_create'),

    # Phase specific views
    url(r'^(\d+)/add_phase/$', 'project_add_phase', name='project_add_phase'),
    url(r'^(\d+)/edit_phase/$', 'project_edit_phase', name='project_edit_phase'),
    url(r'^(\d+)/delete_phase/$', 'project_delete_phase', name='project_delete_phase'),
    url(r'^(\d+)/restart_phase/$', 'project_restart_phase', name='project_restart_phase'),


    url(r'^(\d+)/finish/$', 'project_finish', name='project_finish'),
    url(r'^(\d+)/restart/$', 'project_restart', name='project_restart'),
    url(r'^(\d+)/finish_phase/$', 'project_finish_phase', name='project_finish_phase'),
)