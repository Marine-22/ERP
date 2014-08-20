from django import forms
from django.contrib.auth.models import User
from erp.apps.resources.models import UserProfile
from erp.apps.partner.models import Partner, PartnerType

class ProfileForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super (ProfileForm,self ).__init__(*args,**kwargs)
        type = PartnerType.objects.get(Type='Group')
        self.fields['Partner'].queryset = Partner.objects.filter(Type=type)
        self.fields['Phone'].widget.attrs['class'] = 'xlarge'
        self.fields['Partner'].widget.attrs['class'] = 'xlarge'
        self.fields['ManHourCost'].widget.attrs['class'] = 'xlarge'
    class Meta:
        model = UserProfile
        exclude = ['user']

class UserForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super (UserForm,self ).__init__(*args,**kwargs)
        self.fields['email'].widget.attrs['class'] = 'xlarge'
        self.fields['username'].widget.attrs['class'] = 'xlarge'

    class Meta:
        model = User
        exclude = ['password','is_staff','is_active','is_superuser','last_login','date_joined']