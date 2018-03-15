from django import forms
from  django.contrib.auth.forms import AuthenticationForm
import  re
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
    username = forms.CharField(required=True, label="用户名", error_messages={'required': '你的账号不能为空'},
                               widget=forms.TextInput(attrs={'class':'form-control','placeholder': u"请输入用户名"}))
    password = forms.CharField(required=True, label="密码", error_messages={'required': '请输入你的密码'},
                               widget=forms.PasswordInput(attrs={'class':'form-control','placeholder': "请输入密码"}))



class UserCreateForm(forms.Form):

    # username = forms.CharField(required=True, label="用户名",
    #                            error_messages={'required': '用户名不能为空'},
    #                            max_length=15,
    #                            widget=forms.TextInput(attrs={'class':'form-control','placeholder': u"用户名"}))
    #
    # nick_name = forms.CharField(label="昵称",
    #                             widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'昵称'}))
    #
    # password = forms.CharField(required=True, label="密码",
    #                            error_messages={'required': '密码不能为空',},
    #                            max_length=20,
    #                            widget=forms.PasswordInput(attrs={'class':'form-control','data-placeholder': "密码"}))
    #
    # mobile = forms.CharField(required=True,label="手机号",
    #                          error_messages={'required': '手机号不能为空'},
    #                          max_length=11,
    #                          widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'手机号'}))
    #
    # email = forms.EmailField(required=True,label='邮箱',
    #                          error_messages={'required': '邮箱不能为空'},
    #                          widget=forms.EmailInput(attrs={'class':'form-control','placeholder': u"邮箱"}))
    username = forms.CharField()

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError("手机号码非法", code="mobile_invalid")