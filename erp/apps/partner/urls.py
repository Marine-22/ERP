from django.conf.urls import patterns, url


urlpatterns = patterns('erp.apps.partner.views',
    url(r'^$', 'partner_list', name='partner_list'),
    url(r'^create/$', 'partner_create', name='partner_create'),
    url(r'^(\d+)/$', 'partner_details', name='partner_details'),
    url(r'^(\d+)/edit/?$', 'partner_edit', name='partner_edit'),
    url(r'^(\d+)/add_contact/$', 'partner_add_contact', name='partner_add_contact'),
    url(r'^(\d+)/edit_contact/$', 'partner_edit_contact', name='partner_edit_contact'),
    url(r'^(\d+)/delete_contact/$', 'partner_delete_contact', name='partner_delete_contact'),
)