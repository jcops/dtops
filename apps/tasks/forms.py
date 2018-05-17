#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Author:Eric
from django import forms
from .models import Deploy_Model,KeyList

class DeployMelForm(forms.ModelForm):
    class Meta:
        model  =Deploy_Model
        fields = ['name','detail']
        help_texts={
            'name':'必填',
            # 'host':'必填'
        }
        labels = {
            'name':'模块名',
            # 'host':'执行主机',
            'detail':'备注'
        }
        widgets = {
                'name':forms.RadioSelect( attrs={'class': 'flat'}),
                # 'host':forms.SelectMultiple(attrs={'class': 'select2', }),
            'detail': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': '备注信息', 'cols': 20, 'rows': 3}),

        }


class DMelForm(forms.ModelForm):
    class Meta:
        model  =KeyList
        fields = ['name']
        help_texts={
            'name':'必填',
            # 'host':'必填'
        }
        labels = {
            'name':'执行主机',
            # 'host':'执行主机',

        }
        widgets = {
                'name':forms.SelectMultiple(attrs={'class': 'flat'}),
                # 'host':forms.SelectMultiple(attrs={'class': 'select2', }),


        }
