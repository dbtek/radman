from django import forms
from django.forms import PasswordInput


class MountForm(forms.Form):
    name = forms.CharField(label='İsim', max_length=100, required=True)
    slug = forms.CharField(label='Dinleme adresi (path)', max_length=6, required=True)
    password = forms.CharField(label='Dinleyici Şifresi', max_length=100, widget=PasswordInput, required=False)