import os
import sys
sys.stdout = sys.stderr
# Add the virtual Python environment site-packages directory to the path
import site
site.addsitedir('/var/www/environment/lib/python2.6/site-packages')

# Avoid ``[Errno 13] Permission denied: '/var/www/.python-eggs'`` messages
import os
os.environ['PYTHON_EGG_CACHE'] = '/var/www/egg-cache'

#If your project is not on your PYTHONPATH by default you can add the following
sys.path.append('/var/www')
os.environ['DJANGO_SETTINGS_MODULE'] = 'erp.settings.production'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

#import os, sys
#import django.core.handlers.wsgi

#sys.path.append('/var/www/')

#os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

#application = django.core.handlers.wsgi.WSGIHandler()
