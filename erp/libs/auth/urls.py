from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='auth_login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/erp/'}, name='logout'),
    )