from django import forms
from django.forms import PasswordInput


class PlayerForm(forms.Form):
    name = forms.CharField(label='İsminiz', max_length=100)
    password = forms.CharField(label='Şifre', max_length=100, widget=PasswordInput, required=False)