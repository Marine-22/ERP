#Project URLs

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('erp.apps.timesheet.views',
    url(r'^$', 'timesheet', name='timesheet'),
    url(r'^all/$', 'timesheet_all', name='timesheet_all'),
    url(r'^get_timesheet/$', 'get_timesheet', name='get_timesheet'),
    url(r'^get_timesheet/(?P<argument>\w+)/$', 'get_timesheet', name='get_timesheet'),
    url(r'^approve/$', 'timesheet_approval', name='approveTimesheet'),
    url(r'^approve/fetch/(?P<id>\d+)/(?P<page>\d+)$', 'timesheet_approval_fetch', name='approveTimesheetFetch'),
    url(r'^approve/fetch/(?P<id>\d+)$', 'timesheet_approval_fetch', name='approveTimesheetFetch'),
    url(r'^form/$', 'timesheet_form', name='timesheetForm'),
    url(r'^form/edit/(?P<type>\w+)/(?P<id>\d+)/$', 'timesheet_edit_form', name='timesheetEditForm'),
    url(r'^form/save/(?P<type>\w+)/$', 'form_save', name='timesheetFormSave'),
    url(r'^form/save/(?P<type>\w+)/(?P<id>\d+)/$', 'form_save', name='timesheetFormSave'),
    url(r'^delete/(?P<type>\w+)/(?P<id>\d+)/$', 'delete', name='delete_timesheet'),

    #url(r'^add_timesheet/$', 'add', name='add_timesheet'),
    #url(r'^add_internal/$', 'add_internal', name='add_internal'),
    #url(r'^add_workshop/$', 'add_workshop', name='add_workshop'),
    #url(r'^edit/(?P<type>\w+)/(?P<id>\d+)/$', 'edit', name='edit_timesheet'),

    #url(r'^edit_timesheet/(\d+)/$', 'edit_timesheet', name='edit_timesheet'),
    #url(r'^edit_internal/(\d+)/$', 'edit_internal', name='edit_internal'),
    #url(r'^edit_workshop/(\d+)/$', 'edit_workshop', name='edit_workshop'),

    #url(r'^delete_timesheet/(\d+)/$', 'delete_timesheet', name='delete_timesheet'),
    #url(r'^delete_internal/(\d+)/$', 'delete_internal', name='delete_internal'),
    #url(r'^delete_workshop/(\d+)/$', 'delete_workshop', name='delete_workshop'),
    url(r'^clone_timesheet/$', 'clone_timesheet', name='clone_timesheet'),
)