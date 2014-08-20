from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'erp.apps.simplewiki.views.root_redirect', name='wiki_root'),
    url(r'^/?([a-zA-Z\d_-]*)/_edit/$', 'erp.apps.simplewiki.views.edit', name='wiki_edit'),
    url(r'^/?([a-zA-Z\d_-]*)/_create/$', 'erp.apps.simplewiki.views.create', name='wiki_create'),
    url(r'^/?([a-zA-Z\d_-]*)/_history/([0-9]*)/$', 'erp.apps.simplewiki.views.history', name='wiki_history'),
    url(r'^/?([a-zA-Z\d_-]*)/_random/$', 'erp.apps.simplewiki.views.random_article', name='wiki_random'),
    url(r'^/?([a-zA-Z\d_-]*)/_search/articles/$', 'erp.apps.simplewiki.views.search_articles', name='wiki_search_articles'),
    url(r'^/?([a-zA-Z\d_-]*)/_search/related/$', 'erp.apps.simplewiki.views.search_related', name='search_related'),
    url(r'^/?([a-zA-Z\d_-]*)/_related/add/$', 'erp.apps.simplewiki.views.add_related', name='add_related'),
    url(r'^/?([a-zA-Z\d_-]*)/_related/remove/(\d+)$', 'erp.apps.simplewiki.views.remove_related', name='wiki_remove_relation'),
    url(r'^/?([a-zA-Z\d_-]*)/_add_attachment/$', 'erp.apps.simplewiki.views_attachments.add_attachment', name='add_attachment'),
    url(r'^/?([a-zA-Z\d_-]*)/_view_attachment/(.+)?$', 'erp.apps.simplewiki.views_attachments.view_attachment', name='wiki_view_attachment'),
#    url(r'^/?([a-zA-Z\d/_-]*)/_view_attachment/?$', 'simplewiki.views_attachments.list_attachments', name='wiki_list_attachments'),
    url(r'^/?([a-zA-Z\d_-]*)/*$', 'erp.apps.simplewiki.views.view', name='wiki_view'),
    url(r'^(.*)$', 'erp.apps.simplewiki.views.encode_err', name='wiki_encode_err')
)
