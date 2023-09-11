from typing import Any, Dict
from app.models import *
from django import forms
from django.core.exceptions import ValidationError

class UserRegForm(forms.Form):
    username = forms.CharField(max_length= 100)
    email = forms.EmailField(max_length= 30)
    password = forms.CharField(max_length=20, widget= forms.PasswordInput)
    re_password = forms.CharField(max_length=20, widget= forms.PasswordInput)
    phone_number = forms.CharField(max_length= 12)
    image = forms.ImageField()
    widget = {'password' : forms.HiddenInput,'re_password' : forms.HiddenInput}

    def clean(self):
        validate_psw = self.cleaned_data['password']
        validate_rpsw = self.cleaned_data['re_password']
        email = self.cleaned_data['email']
        email_queryset = UserProfile.objects.filter(email = email)
        print(email_queryset)
        import re
        temp = re.match('[a-zA-Z]+(\w+\d+| \d+\w+)[a-zA-Z]*', validate_psw)
        if email_queryset:
            raise ValidationError('Wrong')
        elif validate_psw != validate_rpsw:
            raise ValidationError('Wrong')
        elif temp == None:
            raise ValidationError('Wrong')
        elif ' ' in validate_psw:
            raise ValidationError('Wrong')