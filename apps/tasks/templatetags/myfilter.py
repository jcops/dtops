#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Author:Eric
from django import template
from tasks.models import KeyList

register = template.Library()
@register.filter(name='str_split')
def show_user_group_minions( user_type,list_type):
    '''
    远程命令、模块部署及文件上传中显示主机列表
    '''
    if user_type:
        tgt_list = [i['name'] for i in KeyList.objects.filter(status=True).values('name')]
    return {'tgt_list':sorted(list(set(tgt_list))), 'list_type':list_type}

# register.inclusion_tag('tasks/deploy_model.html')(show_user_group_minions)