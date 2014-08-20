#Project URLs

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('erp.apps.internal.views',
    url(r'^$', 'internal_summary_report', name='internal_summary_report'),
    url(r'^summary_report/$', 'internal_summary_report', name='internal_summary_report'),
    url(r'^summary_report/test/$', 'xls_all_types', name='xls_all_types'),
    url(r'^create/$', 'internal_create', name='internal_create'),
    url(r'^edit/(\d+)/$', 'internal_edit', name='internal_edit'),
    url(r'^delete/(\d+)/$', 'internal_delete', name='internal_delete'),
)