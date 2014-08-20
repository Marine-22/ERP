from django import forms
from django.contrib.auth.models import User
from erp.apps.partner.models import Partner, PartnerType
from erp.apps.project.models import Project, ProjectPhase, ProjectSegment, ProjectType
from django.utils.translation import ugettext_lazy as _

datepicker_class = {'class':'datepicker'}

# Definition of ProjectForm class with all bound methods
class ProjectForm(forms.Form):
    Name = forms.CharField(
        required=True,
        label=_(u'Project name'),
        error_messages={'required':_(u'Project name is required')},
        widget=forms.TextInput())

    ProjectClient = forms.ModelChoiceField(
        required=True, label=_(u'Project client'),
        error_messages={'required':_(u'Project client is required')},
        queryset=None,
        empty_label=None)

    Start = forms.DateField(
        required=True,
        label=_(u'Project start date'),
        error_messages={'required':_(u'Project start date is required')},
        widget=forms.TextInput(attrs=dict(datepicker_class)))

    End = forms.DateField(
        required=True,
        label=_(u'Project end date'),
        error_messages={'required':_(u'Project end date is required')},
        widget=forms.TextInput(attrs=dict(datepicker_class)))

    ProjectManager = forms.ModelChoiceField(
        required=True,
        label=_(u'Project manager'),
        error_messages={'required':_(u'Project manager is required')},
        queryset=None,
        empty_label=None)

    QualityAssurance = forms.ModelChoiceField(
        required=True,
        label=_(u'Quality assurance'),
        error_messages={'required':_(u'Quality assurance is required')},
        queryset=None,
        empty_label=None)

    Price = forms.DecimalField(
        required=True, label=_(u'Project price'),
        help_text=_(u'In euro, without VAT'),
        error_messages={'required':_(u'Project price is required')})

    Segment = forms.ModelChoiceField(
        required=True,
        label=_(u'Project segment'),
        error_messages={'required':_(u'Project segment is required')},
        queryset=None,
        empty_label=None)

    Type = forms.ModelChoiceField(
        required=True,
        label=_(u'Project type'),
        error_messages={'required':_(u'Project type is required')},
        queryset=None,
        empty_label=None)

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['ProjectClient'].queryset = Partner.objects.all().order_by('PartnerName')
        self.fields['ProjectManager'].queryset = User.objects.all().order_by('username')
        self.fields['QualityAssurance'].queryset = User.objects.all().order_by('username')
        self.fields['Segment'].queryset = ProjectSegment.objects.all()
        self.fields['Type'].queryset = ProjectType.objects.all()

    def save(self):
        new_project = Project.objects.create(
            Name = self.cleaned_data['Name'],
            ProjectClient = self.cleaned_data['ProjectClient'],
            Start = self.cleaned_data['Start'],
            End = self.cleaned_data['End'],
            ProjectManager = self.cleaned_data['ProjectManager'],
            QualityAssurance = self.cleaned_data['QualityAssurance'],
            Price = self.cleaned_data['Price'],
            Segment = self.cleaned_data['Segment'],
            Type = self.cleaned_data['Type']
        )

        return new_project

class ProjectPhaseForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super (ProjectPhaseForm,self ).__init__(*args,**kwargs)
        self.fields['Start'].widget.attrs['class'] = 'datepicker'
        self.fields['End'].widget.attrs['class'] = 'datepicker'
    class Meta:
        model = ProjectPhase
        exclude = ['Status','Project']

class AllocationForm(forms.ModelForm):
    Star = forms.DateField(
        label=_(u'Start date'),
        required=True,
        error_messages={'required':(u'Allocation start date is required')},
        widget=forms.TextInput(attrs=dict(datepicker_class)))

    End = forms.DateField(
        label=_(u'End date'),
        required=True,
        error_messages={'required':(u'Allocation end date is required')},
        widget=forms.TextInput(attrs=dict(datepicker_class)))

    Mandays = forms.DecimalField(
        label=_(u'Manday count'))

    HourSale = forms.DecimalField(
        label=_(u'Hour sale')
    )

    FixedPrice = forms.DecimalField(
        label=_(u'Project fixed price'))