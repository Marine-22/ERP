from django import forms


datepicker_class = {'class':'datepicker'}

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