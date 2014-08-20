from django import forms
from erp.apps.internal.models import Internal

class InternalForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super (InternalForm,self ).__init__(*args,**kwargs)
        self.fields['Name'].widget.attrs['class'] = 'xxlarge'
        self.fields['Description'].widget.attrs['cols'] = '100'
        
    class Meta:
        model = Internal