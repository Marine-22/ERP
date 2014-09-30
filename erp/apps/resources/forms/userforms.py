from django import forms
from django.http import QueryDict
from django.utils.translation import ugettext, ugettext_lazy as _

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class UserUpdateForm(forms.ModelForm):

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'wrong_password': _("Your old password was entered incorrectly."),
    }

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.user = kwargs.pop('instance')
        if(args and isinstance(args[0], QueryDict)):
            self.password_old = args[0].get('password_old', None)
            self.password_new1 = args[0].get('password_new1', None)
            self.password_new2 = args[0].get('password_new2', None)
            self.user_id = args[0].get('user_id', None)
    #Form pre zmenu udajov o pouzivatelovi, ked pouzivatel meni udaje o samom sebe (nie admin)    
    class Meta:
        model = User
        exclude = ('is_staff', 'is_active', 'last_login', 'date_joined', 'user_permissions', 'password')
    # Nastavim access pre pouzivatelov s roznymi opravneniami
    def setAccess(self, permissions):
        self.hidden = []
        self.fields['username'].widget.attrs['readonly'] = True
        if not (permissions.canEdit or permissions.officeManager):
            self.fields['first_name'].widget.attrs['readonly'] = True
            self.fields['last_name'].widget.attrs['readonly'] = True
            self.fields['email'].widget.attrs['readonly'] = True
            self.fields['phone_number'].widget.attrs['readonly'] = True
        if not permissions.isSuperLoggedIn:
            self.hidden.append('is_superuser')
        if not (permissions.officeManager or permissions.isSuperLoggedIn):
            self.hidden.append('groups')
        
    def add_fields(self, permissions):
        if permissions.canEdit:
            if permissions.needOldPassword:
                self.fields['password_old'] = forms.CharField(
                    required=False,
                    label=_('Actual password'),
                    widget=forms.PasswordInput())
            self.fields['password_new1'] = forms.CharField(
                required=False,
                label=_('New password'),
                widget=forms.PasswordInput())
            self.fields['password_new2'] = forms.CharField(
                required=False,
                label=_('Repeat new password'),
                widget=forms.PasswordInput())
        if(permissions.id):
            self.user_id = permissions.id
   

    def __str__(self):
        return 'UserUpdateForm[' + self.user_id + ']: username = ' + self.cleaned_data['username'] + '; first_name = ' + self.cleaned_data['first_name'] + '; last_name = ' + self.cleaned_data['last_name'] + '; email = ' + self.cleaned_data['email'] + '; phone_number = ' + self.cleaned_data['phone_number'] + '; is_superuser = ' + str(self.cleaned_data['is_superuser']) + '; groups = ' + str(self.cleaned_data['groups']) + '; password_old = ' + self.password_old + '; password_new1 = ' + self.password_new1

    def is_valid(self, needOldPassword=None):
        super(UserUpdateForm, self).is_valid()
        if self.password_new1 and self.password_new2:
            if self.password_new1 != self.password_new2:
                self._errors['password_new1'] = self.error_class([self.error_messages['password_mismatch']])
            if needOldPassword and not self.user.check_password(self.password_old):
                self._errors['password_old'] = self.error_class([self.error_messages['wrong_password']])
        return not bool(self.errors)

    def save(self, commit=True):
        if commit:
            if self.password_new1 and self.password_new2:
                self.user.set_password(self.password_new1)
            self.user.save()
        return super(UserUpdateForm, self).save()




class UserCreateForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields.insert(6, 'password_new2', forms.CharField(
            required=True,
            label=_('Repeat password'),
            widget=forms.PasswordInput()))
        self.fields['password'].widget = forms.PasswordInput()
        if(args and isinstance(args[0], QueryDict)):
            self.password_new2 = args[0].get('password_new2', None)

    class Meta:
        model = User
        exclude = ('is_staff', 'is_active', 'last_login', 'date_joined', 'user_permissions')
    
    def setAccess(self, is_superuser):
        if not is_superuser:
            self.fields['is_superuser'].widget.attrs['disabled'] = 'disabled'

    def is_valid(self):
        pss_equals = self.data['password'] == self.password_new2
        self.data['password'] = make_password(str(self.data['password']))
        super(UserCreateForm, self).is_valid()
        if not pss_equals:
            self._errors['password'] = self.error_class([self.error_messages['password_mismatch']])
        return not bool(self.errors)