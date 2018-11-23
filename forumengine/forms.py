from django import forms
from .models import *
from django.core.exceptions import ValidationError


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = ForumUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        attrs = {'class': 'form-control', 'required': True}
        vidgets = {
            'username': forms.TextInput(attrs=attrs),
            'first_name': forms.TextInput(attrs=attrs),
            'last_name': forms.TextInput(attrs=attrs),
            'email': forms.EmailInput(attrs=attrs),
            'password': forms.PasswordInput(attrs=attrs)
        }
