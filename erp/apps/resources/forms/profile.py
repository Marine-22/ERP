from django import forms
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

class ProfileForm(forms.Form):
    firstName = forms.CharField(
        required = True,
        label = _(u'First name'),
        error_messages = {'required':_(u'First name is required')}
    )

    lastName = forms.CharField(
        required = True,
        label = _(u'Last name'),
        error_messages = {'required':_(u'Last name is required')}
    )

    userEmail = forms.EmailField(
        required = True,
        label = _(u'E-mail'),
        error_messages = {'required':_(u'E-mail is required')}
    )

    userPhone = forms.CharField(
        required = False,
        label = _(u'Phone number')
    )

    userLdap = forms.CharField(
        required = True,
        label = _(u'LDAP username'),
        error_messages = {'required':_(u'LDAP login is required')}
    )

    userRoles = forms.MultipleChoiceField(
        required = True,
        label = _(u'User roles'),
        #queryset = Group.objects.all(),
        error_messages = {'required':_(u'User must have at least one role is assigned')}
    )

    #def __init__(self):
    #    super(ProfileForm, self).__init__()