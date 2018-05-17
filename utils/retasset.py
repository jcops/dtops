#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Author:Eric

import os,django
import threading
from time import sleep, ctime


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dtops.settings")# project_name 项目名称
django.setup()
from utils.Saltapi import SaltAPI
from  asset.models import Asset
from  tasks.models import KeyList
# salt = SaltAPI(url="https://118.25.39.84:8000", user="saltapi", password="saltapi123")
salt = SaltAPI()
def getkeyall():
    '''获取key主机节点'''
    minions,minions_pre = salt.list_all_key()
    # print(minions,minions_pre)
    return minions,minions_pre

def salt_alive(tgt):
    '''测试key节点连通性'''
    status = salt.salt_alive(tgt)
    return  status

# salt_alive('10.105.75.82')
def accept_key(tgt):
    '''认证节点'''
    ret = salt.accept_key(tgt)
    return ret
def delete_key(tgt):
    ret = salt.delete_key(tgt)
    return ret

def disks(tgt,fun):
    dis = salt.remote_noarg_execution_sigle(tgt,fun)
    # print(dis)
    disk = {}
    for partition in dis.values():
        # print(partition)
        for i in partition.values():
            # print(i)
            fs = i['filesystem']
            if fs.startswith("/dev"):
                total = '%.2f' % (float(i['1K-blocks']) / 1024 / 1024) + 'G'
                avail = '%.2f' % (float(i['available']) / 1024 / 1024)
                capacity = i['capacity']
                used = '%.2f' % (float(i['used']) / 1024 / 1024)
                disk[fs] = { 'total': total, 'avail': avail,'used':used,'capacity':capacity}
            else:
                continue

        return disk



def auto_asset(node):
    try:
        ret = salt.remote_grains_execution_sigle(node)
        # asset_info = {'ls':'pwd','os':'oooo','dns':'1.1.1.1'}
        asset_info={}
        asset_info['os']= ret[node]['oscodename']
        asset_info['kernelrelease']= ret[node]['kernelrelease']
        asset_info['cpu_model']= ret[node]['cpu_model']
        asset_info['dns']= ','.join(ret[node]['dns']['ip4_nameservers'])
        asset_info['serialnumber'] =  ret[node]['serialnumber']
        asset_info['virtual'] =  ret[node]['virtual']
        asset_info['localhost'] = ret[node]['localhost']
        asset_info['mem_total'] =  ret[node]['mem_total']
        asset_info['num_cpus'] =  ret[node]['num_cpus']
        asset_info['ip4_interfaces'] = " ".join(ret[node]['ip4_interfaces']['eth0'])
        asset_info['hwaddr_interfaces'] = ret[node]['hwaddr_interfaces']['eth0']
        asset_info['disks'] = disks(node,'disk.usage')

        # selinux = ret[node]['enabled']
        return asset_info
    except Exception as e:
        print('错误',e)
# ass = Asset.objects.all()
# for ii in ass:
#     asset_info=auto_asset(ii.inner_ip)
#     asset = Asset.objects.get(inner_ip=ii.inner_ip)
#     asset.osfinger = asset_info['os']
#     asset.hostname = asset_info['localhost']
#     asset.cpu_model = asset_info['cpu_model']
#     asset.mac_addr = asset_info['hwaddr_interfaces']
#     asset.mem_total = asset_info['mem_total']
#     asset.num_cpus = asset_info['num_cpus']
#     asset.virtual = asset_info['virtual']
#     asset.serialnumber = asset_info['serialnumber']
#     asset.dns = asset_info['dns']
#     asset.kernelrelease = asset_info['kernelrelease']
#     asset.inner_ip = asset_info['ip4_interfaces']
#     for de,di in asset_info['disks'].items():
#         #{'avail': '40.05', 'total': '49.09G', 'capacity': '15%', 'used': '6.54'}
#         asset.disk_total = ''.join(de + di['total'])
#     asset.save()

# class MyThread(threading.Thread):
#     def __init__(self, func,args):
#         super(MyThread, self).__init__()
#         self.func = func
#         self.args =args
#
#
#     def run(self):
#         self.result = self.func(*self.args)
#         # 相当于执行auto_asset(node)
#     def get_result(self):
#         try:
#             return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
#         except Exception:
#             return None
class MyThread(threading.Thread):
    def __init__(self, func,args):
        super(MyThread, self).__init__()
        self.func = func
        self.args =args


    def run(self):
        self.result = self.func(*self.args)
        # 相当于执行auto_asset(node)
    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None

def getss():
    obj = Asset.objects.all()
    b = []
    for i in obj:
        b.append(i.inner_ip)
    files = range(len(b))
    t_list = []
    for i in files:
        t = MyThread(auto_asset,(b[i],))
        t_list.append(t)
        t.start()
    for t in t_list:
        t.join()  # 一定要join，不然主线程比子线程跑的快，会拿不到结果
        # aa = t.get_result()
    return t_list
# bb = getss()


#     #启动线程
#     for i in files:
#         t_list[i].start()
#         tt = t_list[i].join()
#         print(tt)
#
#     for i in files:
#         t_list[i].join()

#     #主线程
#         print ( 'end:%s' %ctime())
# for iii in t_list:
#     iii.join()
#     print(iii['os'])

