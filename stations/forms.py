from django import forms


class MountForm(forms.Form):
    name = forms.CharField(label='İsim', max_length=100)