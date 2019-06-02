from django import forms

from .models import Register

class RegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    email = forms.CharField()
    full_name = forms.CharField()
