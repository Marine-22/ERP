# Override for notifications since they do not support Django 1.4 natively

import sys

from django.db.models import signals

from erp.libs.notification import views as notification_views
from erp.libs.notification import lockfile as notification_lockfile
from erp.libs.selects import widgets as selects_widgets


sys.modules['notification.views'] = notification_views
sys.modules['notification.lockfile'] = notification_lockfile
sys.modules['smart_selects.widgets'] = selects_widgets

# Notifications specific
from django.conf import settings
from django.utils.translation import ugettext_noop as _
from notification import models as notification

def create_notice_type(app, created_models, verbosity, **kwargs):
    notification.create_notice_type(
        'holiday_created',
        _('New holiday'),
        _('New holiday was created for approval')
    )

    notification.create_notice_type(
        'holiday_approved',
        _('Holiday approved'),
        _('Your holiday was approved')
    )

    notification.create_notice_type(
        'holiday_rejected',
        _('Holiday rejected'),
        _('Your holiday was rejected')
    )

signals.post_syncdb.connect(create_notice_type, sender=notification)