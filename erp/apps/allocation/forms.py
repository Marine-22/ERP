from django import forms
from django.contrib.auth.models import User
from erp.apps.allocation.models import Allocation

class AllocationForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super (AllocationForm,self ).__init__(*args,**kwargs)
        self.fields['Resource'].queryset = User.objects.all().order_by('first_name')
        self.fields['Start'].widget.attrs['class'] = 'datepicker'
        self.fields['End'].widget.attrs['class'] = 'datepicker'

    class Meta:
        model = Allocation
        exclude = ['created','author','company']