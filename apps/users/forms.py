from django import forms
from  django.contrib.auth.forms import AuthenticationForm

from users.models import UserLog,UserProfile
class LoginForm(forms.Form):
    # username = forms.CharField(
    #     # label='用户名',
    #     max_length=20,
    # )
    # password = forms.CharField(
    #     # label='密码',
    #     # widget=forms.PasswordInput,
    #     max_length=20,
    # )
    username = forms.CharField(required=True, label=u"用户名", error_messages={'required': u'请输入用户名'},
                               widget=forms.TextInput(attrs={'placeholder': u"用户名"}))
    password = forms.CharField(required=True, label=u"密码", error_messages={'required': u'请输入密码'},
                               widget=forms.PasswordInput(attrs={'placeholder': u"密码"}))



