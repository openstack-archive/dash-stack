import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from django import forms

class UserRegisterForm(forms.Form):
    username = forms.CharField(
        label='Username',
        max_length=64
    )
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
    )
    password2 = forms.CharField(
        label='Password (Again)',
        widget=forms.PasswordInput(),
    )
    tos = forms.BooleanField(
        required=True,
        error_messages={'required': 'You must accept TOS.'}
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only contain'
                                        'alphanumeric characters '
                                        'and the underscore.')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Username already taken.')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError('Email address is not available.')

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2, password1
        raise forms.ValidationError('Password do not match.')
