from django.conf.urls.defaults import patterns, include, url

from erp.apps.timesheet.forms.timesheet import TimeSheetForm
from erp.apps.timesheet.forms.internal import InternalForm
from erp.apps.project.forms.project import ProjectForm
from erp.apps.partner.forms.partner import PartnerForm


urlpatterns = patterns('ajax_validation.views',
    # Timesheet form validation.
    url(r'^timesheet/$', 'validate', {'form_class': TimeSheetForm}, 'timesheet_form_validate'),
    # Internal form validation.
    url(r'^internal/$', 'validate', {'form_class': InternalForm}, 'internal_form_validate'),
    # Project form validation
    url(r'^project/$', 'validate', {'form_class': ProjectForm}, 'project_form_validate'),
    # Partner form validation
    url(r'partner/$', 'validate', {'form_class': PartnerForm}, 'partner_form_validate')
)