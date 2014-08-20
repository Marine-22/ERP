from django import forms
from django.contrib.auth.models import User
from erp.apps.resources.models import InternalRole, UserType, UserProfile
from erp.apps.partner.models import Partner
from erp.apps.project.models import Project
from erp.apps.timesheet.models import TimeSheet, InternalTimeSheet
from erp.libs.workflows.models import State, Workflow
from erp.apps.timesheet.models import Workshop

class TimeSheetForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super (TimeSheetForm,self ).__init__(*args,**kwargs)

        deleted_projects = State.objects.get(name='Deleted', workflow=Workflow.objects.get(name='Project'))
        finished_projects = State.objects.get(name='Finished', workflow=Workflow.objects.get(name='Project'))

        projects = Project.objects.all().exclude(Status=deleted_projects).exclude(Status=finished_projects).values('ProjectClient')

        self.fields['Partner'].queryset = Partner.objects.filter(pk__in=projects).order_by('PartnerName')

        self.fields['DueDate'].widget.attrs['class'] = 'datepicker'
        self.fields['Activity'].widget.attrs['cols'] = '65'
        self.fields['Activity'].widget.attrs['rows'] = '5'
    class Meta:
        model = TimeSheet

class WorkshopForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super (WorkshopForm,self ).__init__(*args,**kwargs)

        deleted_projects = State.objects.get(name='Deleted', workflow=Workflow.objects.get(name='Project'))
        finished_projects = State.objects.get(name='Finished', workflow=Workflow.objects.get(name='Project'))

        projects = Project.objects.all().exclude(Status=deleted_projects).exclude(Status=finished_projects).values('ProjectClient')

        self.fields['Ws_Partner'].queryset = Partner.objects.filter(pk__in=projects).order_by('PartnerName')

        internal_list = InternalRole.objects.all().exclude(Role='Ex-employee').values_list('Role', flat=True)
        internal = UserType.objects.get(Type='Internal')
        iquap = Partner.objects.get(pk=int(30))
        resource_list = UserProfile.objects.filter(Partner=iquap, UserType=internal, InternalRole__Role__in=internal_list).values('id')

        self.fields['Resources'].queryset = User.objects.filter(pk__in=resource_list)

        self.fields['Start'].widget.attrs['style'] = 'width:70px'
        self.fields['End'].widget.attrs['style'] = 'width:70px'
        self.fields['Resources'].widget.attrs['style'] = 'width:400px'
        self.fields['DueDate'].widget.attrs['class'] = 'datepicker'
        self.fields['Activity'].widget.attrs['cols'] = '65'
        self.fields['Activity'].widget.attrs['rows'] = '5'

    class Meta:
        model = Workshop

class InternalForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super (InternalForm,self ).__init__(*args,**kwargs)
        self.fields['InternalDueDate'].widget.attrs['class'] = 'datepicker'
        self.fields['Activity'].widget.attrs['cols'] = '65'
        self.fields['Activity'].widget.attrs['rows'] = '5'
    class Meta:
        model = InternalTimeSheet
        exclude = ['User']