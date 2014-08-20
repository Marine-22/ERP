import os
import urlparse
from erp import settings
from django.template.base import Library

register = Library()

@register.simple_tag
def media(filename, flags=''):
    flags = set(f.strip() for f in flags.split(','))
    url = urlparse.urljoin(settings.STATIC_URL, filename)
    if 'absolute' in flags:
        url = _absolute_url(url)
    if (filename.endswith('.css') or filename.endswith('.js')) and 'no-timestamp' not in flags or \
       'timestamp' in flags:
        fullname = os.path.join(settings.MEDIA_ROOT, filename)
        if os.path.exists(fullname):
            url += '?%d' % os.path.getmtime(fullname)
    return url