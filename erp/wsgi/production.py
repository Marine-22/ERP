import os
import sys
import site

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
site_packages = os.path.join(PROJECT_ROOT, '/var/environments/erp/lib/python2.7/site-packages')
site.addsitedir(os.path.abspath(site_packages))
sys.path.insert(0, PROJECT_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'erp.settings.production'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()