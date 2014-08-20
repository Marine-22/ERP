#Reporting URLs

from django.conf.urls import patterns, url

urlpatterns = patterns('erp.apps.reporting.views',
    url(r'^$', 'company_dashboard', name='company_dashboard'),
    url(r'^holiday_report/$', 'holiday_report', name='holiday_report'),
    url(r'^holiday_report/ajax/$', 'holiday_ajax_report', name='holiday_ajax_report'),
    url(r'^internal_report/$', 'internal_summary_report', name='internal_summary_report'),
)