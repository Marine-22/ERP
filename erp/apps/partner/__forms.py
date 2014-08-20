from django import forms
from erp.apps.partner.models import Partner, PartnerContact

class PartnerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PartnerForm, self).__init__(*args, **kwargs)
        self.fields['PartnerName'].widget.attrs['class'] = 'xxlarge'
    class Meta:
        model = Partner

class PartnerContactForm(forms.ModelForm):
    class Meta:
        model = PartnerContact
        exclude = ['Partner']