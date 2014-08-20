from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from notification.views import send
from erp.apps.partner.models import Partner
from erp.apps.project.models import Project, ProjectPhase
from erp.libs.workflows import utils
from erp.libs.workflows.models import State
from erp.libs.workflows.models import Workflow
from smart_selects.widgets import ChainedSelect
from erp.apps.timesheet.models import TimeSheet

deleted_projects = State.objects.get(name='Deleted', workflow=Workflow.objects.get(name='Project'))
finished_projects = State.objects.get(name='Finished', workflow=Workflow.objects.get(name='Project'))
projects = Project.objects.all().exclude(Status=deleted_projects).exclude(Status=finished_projects).values('ProjectClient')

class TimeSheetForm(forms.Form):
    dueDate = forms.DateField(
        label = _(u'Due date'),
        required = True,
        error_messages = {'required':_(u'Timesheet must have a due date defined')},
        widget = forms.TextInput(attrs={'class':'datepicker'})
    )

    hours = forms.IntegerField(
        label = _(u'Hours'),
        required = True,
        error_messages = {'required':_(u'Timesheet must have a number of hours defined')}
    )

    partner = forms.ModelChoiceField(
        label = _(u'Partner'),
        queryset = Partner.objects.filter(pk__in=projects).order_by('PartnerName'),
        required = True,
        error_messages = {'required':_(u'Timesheet must have a partner assigned')}
    )

    project = forms.ModelChoiceField(
        queryset = Project.objects.all(),
        label = _(u'Project'),
        widget = ChainedSelect(
            app_name = 'project',
            model_name = 'Project',
            chain_field = 'partner',
            model_field = 'ProjectClient',
            show_all = False,
            auto_choose = False
        ),
        required = True,
        error_messages = {'required':_(u'Timesheet must have a project assigned')}
    )

    phase = forms.ModelChoiceField(
        queryset = ProjectPhase.objects.all(),
        label = (u'Project phase'),
        required = False,
        widget = ChainedSelect(
            app_name = 'project',
            model_name = 'ProjectPhase',
            chain_field = 'project',
            model_field = 'Project',
            show_all = False,
            auto_choose = False
        )
    )

    activity = forms.CharField(
        label = (u'Activity'),
        required = False
    )

    def save(self, user, id=None):
        if id is not None:
            singleTimeSheet = TimeSheet.objects.get(pk=int(id))
        else:
            singleTimeSheet = TimeSheet()

        singleTimeSheet.DueDate = self.cleaned_data['dueDate']
        singleTimeSheet.Hours = self.cleaned_data['hours']
        singleTimeSheet.Partner = self.cleaned_data['partner']
        singleTimeSheet.Project = self.cleaned_data['project']
        singleTimeSheet.Phase = self.cleaned_data['phase']
        singleTimeSheet.Activity = self.cleaned_data['activity']
        singleTimeSheet.User = user

        singleTimeSheet.save()

        workflow = Workflow.objects.get(name='Timesheet')
        utils.set_workflow(singleTimeSheet, workflow)

        singleTimeSheet.Status = utils.get_state(singleTimeSheet)
        singleTimeSheet.save()

        return singleTimeSheet