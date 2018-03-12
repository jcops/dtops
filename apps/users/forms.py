from django import forms
from  django.contrib.auth.forms import AuthenticationForm

from users.models import UserLog,UserProfile
class UserLoginForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        max_length=20,
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput,
        max_length=20,
    )


