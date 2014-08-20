from django.db.models import signals
from django.conf import settings
from django.utils.translation import ugettext_noop as _
from notification import models as notification

def create_notice_types(app, created_models, verbosity, **kwargs):
    notification.create_notice_type("holiday_created", _("Holiday object created"), _("holiday object was created"))

signals.post_syncdb.connect(create_notice_types, sender=notification)