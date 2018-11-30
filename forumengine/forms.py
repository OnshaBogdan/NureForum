from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.admin import widgets

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


class FilterForm(forms.Form):
    attrs = {'class': 'form-control'}
    CHOICES = (('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Monthly', 'Monthly'), ('All time', 'All time'))
    username = forms.CharField(
        label='username',
        max_length=50,
        widget=forms.TextInput({'class': 'form-control', 'name': 'username'}),
        required=False
    )
    time_range = forms.CharField(
        widget=forms.Select(choices=CHOICES, attrs={'class': 'form-control', 'name': 'time_range'})
    )
    lowest_rating = forms.IntegerField(
        label='Rating from',
        widget=forms.NumberInput({'class': 'form-control', 'name': 'lowest_rating'}),
        required=False

    )
    highest_rating = forms.IntegerField(
        label='Rating to',
        widget=forms.NumberInput({'class': 'form-control', 'name': 'highest_rating'}),
        required=False
    )


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body', 'rating']
        vidgets = {
            'body': forms.Textarea(attrs={'class': 'form-control w-100'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
        }



