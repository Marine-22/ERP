from django import forms
from django.utils.translation import ugettext_lazy as _

from erp.apps.partner.models import PartnerType, PartnerSector, PartnerSegment, BankName, Partner

class PartnerForm(forms.Form):
    partner_name = forms.CharField(
            required=True,
            label=_(u'Partner name'),
            widget=forms.TextInput(),
            error_messages={'required': _(u'Partner name can not remain empty')})
    type = forms.ModelChoiceField(
            required=True,
            label=_(u'Partner type'),
            queryset=PartnerType.objects.all(),
            error_messages={'required': _(u'Partner type must be chosen')})
    sector = forms.ModelChoiceField(
            required=True,
            label=_(u'Partner sector'),
            queryset=PartnerSector.objects.all(),
            error_messages={'required': _(u'Partner sector must be chosen')})
    segment = forms.ModelChoiceField(
            required=True,
            label=_(u'Partner segment'),
            queryset=PartnerSegment.objects.all(),
            error_messages={'required': _(u'Partner segment must be chosen')})
    company_id = forms.CharField(
            required=True,
            label=_(u'Company ID'),
            error_messages={'required': _(u'You must provide a company ID')})
    bank_account = forms.CharField(
            required=False,
            label=_(u'Bank account number'))
    bank = forms.ModelChoiceField(
            required=False,
            queryset=BankName.objects.all(),
            label=_(u'Bank name'))
    tax_id = forms.CharField(
            required=False,
            label=_(u'Tax ID'))
    vat_id = forms.CharField(
            required=False,
            label=_(u'Vat ID'))

    def save(self, partner_id=None):
        if partner_id is not None:
            partner = Partner.objects.get(pk=int(partner_id))
        else:
            partner = Partner()
        partner.PartnerName = self.cleaned_data['partner_name']
        partner.Type = self.cleaned_data['type']
        partner.Sector = self.cleaned_data['sector']
        partner.Segment = self.cleaned_data['segment']
        partner.CompanyId = self.cleaned_data['company_id']
        partner.BankAccount = self.cleaned_data['bank_account']
        partner.Bank = self.cleaned_data['bank']
        partner.TaxId = self.cleaned_data['tax_id']
        partner.VatId = self.cleaned_data['vat_id']
        partner.save()
        return partner