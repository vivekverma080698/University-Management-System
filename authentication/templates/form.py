from django import forms
from authentication.models import authTable


class LoginForm(forms.ModelForm):
    class Meta:
        model = authTable
        fields = ['emailID','password']