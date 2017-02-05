import re
from oslo_i18n import translate as _
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from django import forms

class UserRegisterForm(forms.Form):
    email = forms.EmailField(label=_('Email'))
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(),
    )
    password2 = forms.CharField(
        label=_('Password (Again)'),
        widget=forms.PasswordInput(),
    )
    tos = forms.BooleanField(
        required=True,
        error_messages={'required': _('You must accept TOS.')}
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError(_('Email address is not available.'))

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError(_('Password do not match.'))
