from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from notification.views import queue

from erp.apps.internal.models import Internal
from erp.apps.timesheet.models import InternalTimeSheet
from erp.libs.workflows import utils
from erp.libs.workflows.models import Workflow


class InternalForm(forms.Form):
    dueDate = forms.DateField(
        label = _(u'Due date'),
        required = True,
        error_messages = {'required':_(u'Internal must have a due date defined')},
        widget = forms.TextInput(attrs={'class':'datepicker'})
    )

    hours = forms.IntegerField(
        label = _(u'Hours'),
        required = True,
        error_messages = {'required':_(u'Internal must have a number of hours defined')}
    )

    internal = forms.ModelChoiceField(
        label = _(u'Internal'),
        required = True,
        queryset = Internal.objects.all(),
        error_messages = {'required':_(u'You must specify an internal type')}
    )

    activity = forms.CharField(
        label = _(u'Activity'),
        required = False
    )

    def save(self, user, id=None):
        if id is not None:
            singleInternal = InternalTimeSheet.objects.get(pk=int(id))
        else:
            singleInternal = InternalTimeSheet()

        singleInternal.InternalDueDate = self.cleaned_data['dueDate']
        singleInternal.Hours = self.cleaned_data['hours']
        singleInternal.Internal = self.cleaned_data['internal']
        singleInternal.User = user
        singleInternal.Activity = self.cleaned_data['activity']

        singleInternal.save()

        workflow = Workflow.objects.get(name='Timesheet')
        utils.set_workflow(singleInternal, workflow)

        singleInternal.Status = utils.get_state(singleInternal)
        singleInternal.save()

        n_user = User.objects.filter(pk=42)

        if singleInternal.Internal.Name == 'Holiday':
            queue(n_user, "holiday_created", sender=user)

        return singleInternal