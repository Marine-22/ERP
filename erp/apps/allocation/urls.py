#Allocation URLs

from django.conf.urls import patterns, include, url

urlpatterns = patterns('erp.apps.allocation.views',
    url(r'^(\d+)/add/$', 'add_allocation', name='add_allocation'),
    url(r'^(\d+)/edit/$', 'edit_allocation', name='edit_allocation'),
    url(r'^(\d+)/delete/$', 'delete_allocation', name='delete_allocation'),
)