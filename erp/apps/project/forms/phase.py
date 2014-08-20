from django import forms

from erp.apps.project.models import ProjectPhase


class ProjectPhaseForm(forms.ModelForm):

    class Meta:
        model = ProjectPhase
        exclude = ['Status','Project']

    def __init__(self,*args,**kwargs):
        super (ProjectPhaseForm,self ).__init__(*args,**kwargs)
        self.fields['Start'].widget.attrs['class'] = 'datepicker'
        self.fields['End'].widget.attrs['class'] = 'datepicker'