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
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'required': True, 'name': 'password'})
        }


class MessageFilterForm(forms.Form):
    attrs = {'class': 'form-control'}
    CHOICES_time_range = (('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Monthly', 'Monthly'), ('All time', 'All time'))
    CHOICES_sort = (('Message', 'Message'), ('Author', 'Author'), ('Topic', 'Topic'),
                    ('Rating', 'Rating'), ('Date of pub', 'Date of pub'),)
    username = forms.CharField(
        label='username',
        max_length=50,
        widget=forms.TextInput({'class': 'form-control', 'name': 'username'}),
        required=False
    )
    time_range = forms.CharField(
        widget=forms.Select(choices=CHOICES_time_range, attrs={'class': 'form-control', 'name': 'time_range'})
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
    order = forms.CharField(
        label='Sort by',
        widget=forms.Select(choices=CHOICES_sort, attrs={'class': 'form-control', 'name': 'order'})
    )


class TopicFilterForm(forms.Form):
    attrs = {'class': 'form-control'}
    CHOICES = (('Rating', 'Rating'), ('Author', 'Author'), ('Category', 'Category'),
               ('Date of pub', 'Date of pub'), ('Count of messages', 'Count of messages'),)
    title = forms.CharField(
        label='Title',
        max_length=50,
        widget=forms.TextInput({'class': 'form-control', 'name': 'title'}),
        required=False
    )
    username = forms.CharField(
        label='Username',
        max_length=50,
        widget=forms.TextInput({'class': 'form-control', 'name': 'username'}),
        required=False
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
    order = forms.CharField(
        label='Sort by',
        widget=forms.Select(choices=CHOICES, attrs={'class': 'form-control', 'name': 'order'})
    )


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']
        vidgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }
