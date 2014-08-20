from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from erp.settings import development as settings


admin.autodiscover()

urlpatterns = patterns('',
    url('^$', 'erp.apps.dashboard.views.dashboard', name='dashboard'),
    url(r'^resources/', include('erp.apps.resources.urls')),
    url(r'^projects/', include('erp.apps.project.urls')),
    url(r'^timesheet/', include('erp.apps.timesheet.urls')),
    url(r'^reporting/', include('erp.apps.reporting.urls')),
    url(r'^notifications/', include('notification.urls')),
    url(r'^accounts/', include('erp.libs.auth.urls')),
    url(r'^wiki/', include('erp.apps.simplewiki.urls')),
    url(r'^allocations/', include('erp.apps.allocation.urls')),
    url(r'^partners/', include('erp.apps.partner.urls')),
    #url(r'^internals/', include('master.internal.urls')),
    #url(r'^vat/', include('master.vat.urls')),
    #url(r'^reports/', include('master.reporting.urls')),
    url(r'^validation/', include('erp.libs.validation.urls')),
    #url(r'^assets/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    # Chain selects
    url(r'^chaining/', include('smart_selects.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
