from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from erp.apps.partner.models import Partner
from erp.apps.project.models import Project, ProjectSegment, ProjectType
from erp.libs.workflows.models import Workflow
from erp.libs.workflows import utils

datepicker_class = {'class':'datepicker'}


class ProjectForm(forms.Form):
    name = forms.CharField(
            required=True,
            label=_(u'Project name'),
            error_messages={'required':_(u'Project name is required')},
            widget=forms.TextInput())
    project_client = forms.ModelChoiceField(
            required=True,
            label=_(u'Project client'),
            error_messages={'required':_(u'Project client is required')},
            queryset=Partner.objects.all(),
            empty_label=None)
    start = forms.DateField(
            required=True,
            label=_(u'Project start date'),
            error_messages={'required':_(u'Project start date is required')},
            widget=forms.TextInput(attrs=dict(datepicker_class)))
    end = forms.DateField(
            required=True,
            label=_(u'Project end date'),
            error_messages={'required':_(u'Project end date is required')},
            widget=forms.TextInput(attrs=dict(datepicker_class)))
    project_manager = forms.ModelChoiceField(
            required=True,
            label=_(u'Project manager'),
            error_messages={'required':_(u'Project manager is required')},
            queryset=User.objects.all(),
            empty_label=None)
    quality_assurance = forms.ModelChoiceField(
            required=True,
            label=_(u'Quality assurance'),
            error_messages={'required':_(u'Quality assurance is required')},
            queryset=User.objects.all(),
            empty_label=None)
    price = forms.DecimalField(
            required=True, label=_(u'Project price'),
            help_text=_(u'In euro, without VAT'),
            error_messages={'required':_(u'Project price is required')})
    segment = forms.ModelChoiceField(
            required=True,
            label=_(u'Project segment'),
            error_messages={'required':_(u'Project segment is required')},
            queryset=ProjectSegment.objects.all(),
            empty_label=None)
    type = forms.ModelChoiceField(
            required=True,
            label=_(u'Project type'),
            error_messages={'required':_(u'Project type is required')},
            queryset=ProjectType.objects.all(),
            empty_label=None)

    def save(self, project_id=None):
        """
        Saves the given instance of the project or creates a new one
        if no ID was provided.
        """
        if project_id is not None:
            project = Project.objects.get(pk=int(project_id))
        else:
            project = Project()
        # Fill out the data of the given project and prepare it
        # for saving into database.
        project.Name = self.cleaned_data['name']
        project.ProjectClient = self.cleaned_data['project_client']
        project.Start = self.cleaned_data['start']
        project.End = self.cleaned_data['end']
        project.ProjectManager = self.cleaned_data['project_manager']
        project.QualityAssurance = self.cleaned_data['quality_assurance']
        project.Price = self.cleaned_data['price']
        project.Segment = self.cleaned_data['segment']
        project.Type = self.cleaned_data['type']
        project.save()
        # If the item was just created, set up workflow for it
        if project_id is None:
            workflow = Workflow.objects.get(name='Project')
            utils.set_workflow(project, workflow)
            state = utils.get_state(project)
            project.Status = state
            project.save()
        return project