from django.shortcuts import render,HttpResponseRedirect,HttpResponse,reverse
from django.db.models import Q
from django.views.generic import ListView,TemplateView,UpdateView,DetailView,DeleteView,View,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
import json
from  pure_pagination import PageNotAnInteger,Paginator,EmptyPage
from  dtops import settings
from  .models import Asset,System_User,ProductLine,Cloud_Platform,Tag
from .forms import AddAssetModelForm,AssetUpdateModelForm
from utils.Saltapi import SaltAPI
from utils.retasset import auto_asset

salt = SaltAPI(url="https://118.25.39.84:8000", user="saltapi", password="saltapi123")
# Create your views here.

class AssetListView(LoginRequiredMixin,ListView):
    '''资产列表'''
    queryset = Asset.objects.all()
    template_name = 'asset/asset_list.html'

    def get_context_data(self, **kwargs):
        '''分页开始'''
        try:
            page = self.request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(self.queryset,5,request=self.request)
        asset_list = p.page(page)
        # form_list = AddAssetModelForm
        context = {
            "asset_active":"active",
            "asset_list_active": "active",
            "asset_list":asset_list,
            # "form_list":form_list,
            "web_ssh": getattr(settings, 'web_ssh'),
            "web_port": getattr(settings, 'web_port'),

        }
        kwargs.update(context)
        return super(AssetListView,self).get_context_data(**kwargs)

    # def get_queryset(self):
    #     self.queryset = super().get_queryset()
    #     if self.request.GET.get('search'):
    #         query = self.request.GET.get('search', None)
    #         print(query)
    #         queryset = self.queryset.filter(Q(hostname=query) | Q(inner_ip=query) | Q(pub_ip=query))
    #     else:
    #         queryset = super().get_queryset()
    #     return queryset
    def get_queryset(self):
        queryset = super(AssetListView, self).get_queryset()

        q = self.request.GET.get('search','')
        print(q)
        if q:
            return self.queryset.filter(Q(hostname=q) | Q(inner_ip=q) | Q(pub_ip=q))
        return queryset

class SystemUserListAllView(LoginRequiredMixin,ListView):
    '''系统用户列表'''
    queryset = System_User.objects.all().order_by('-create_time')
    template_name = 'asset/sys_user.html'

    def get_context_data(self, **kwargs):
        '''分页开始'''
        try:
            page = self.request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(self.queryset,10,request=self.request)
        system_user_list = p.page(page)

        context = {
            "asset_active":"active",
            "system_user_active":"active",
            "system_user_list":system_user_list,
        }
        kwargs.update(context)
        return super(SystemUserListAllView,self).get_context_data(**kwargs)

class ProductLineListAllView(LoginRequiredMixin,ListView):
    '''产品线列表'''
    queryset = ProductLine.objects.all()

    template_name = 'asset/productline_list.html'

    def get_context_data(self, **kwargs):
        '''分页开始'''
        try:
            page = self.request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(self.queryset,10,request=self.request)
        product_list = p.page(page)

        context = {
            "asset_active":"active",
            "produce_list_active":"active",
            "product_list": product_list,
        }
        kwargs.update(context)
        return super(ProductLineListAllView,self).get_context_data(**kwargs)


# class AddAssetView(View):
#     def get(self,request):
#         form_list = AddAssetModelForm()
#         return  render(request,'asset/create_asset.html',locals())
#
#     def post(self, request):
#         form_list = AddAssetModelForm(request.POST)
#         if form_list.is_valid():
#             add_host = form_list.cleaned_data['inner_ip']
#             if Asset.objects.get(inner_ip=add_host):
#                 return HttpResponse('{"status":"fail", "msg":"记录已存在！"}', content_type='application/json')
#
#             else:
#                 a = Asset()
#                 a.hostname = form_list.cleaned_data['hostname']
#                 a.inner_ip = form_list.cleaned_data['inner_ip']
#                 a.pub_ip = form_list.cleaned_data['pub_ip']
#                 a.save()
#             return HttpResponse('{"status":"success", "msg":"记录添加成功！"}', content_type='application/json')
#         else:
#             return HttpResponse('{"status":"fail", "msg":"记录添加失败！"}', content_type='application/json')

class AddAssetView(LoginRequiredMixin,CreateView):
    '''新建资产'''
    model = Asset
    form_class = AddAssetModelForm
    context_object_name = 'form_list'
    template_name = 'asset/create_asset.html'
    success_url = reverse_lazy('asset:asset_list')

class DelAssetView(LoginRequiredMixin,View):
    '''删除资产(ajax)'''
    def post(self,request):
        ret = {"status":True,"error":False}
        try:
            nid = request.POST.get("nid", '')
            if nid:
                Asset.objects.get(id=int(nid)).delete()
        except Exception:
            ret = {"status": False, "error": '错误'}
        return HttpResponse(json.dumps(ret))

class AssetDetailView(LoginRequiredMixin,DetailView):
    '''资产详情页'''
    model = Asset
    template_name = 'asset/asset_detail.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg,None)
        detail = Asset.objects.get(id=pk)
        context = {
            "asset_active": "active",
            "asset_list_active": "active",
            "detail_list": detail,
        }
        kwargs.update(context)
        return super(AssetDetailView,self).get_context_data(**kwargs)

class AssetUpdateView(LoginRequiredMixin,UpdateView):
    model = Asset
    form_class = AssetUpdateModelForm
    template_name = 'asset/asset_update.html'
    success_url = reverse_lazy('asset:asset_list')
    context_object_name = 'asset_update'
    def get_context_data(self, **kwargs):
        context = {
            "asset_active": "active",
            "asset_list_active": "active",
        }
        kwargs.update(context)
        return super(AssetUpdateView,self).get_context_data(**kwargs)


class auto_update_assets(View):
    def post(self,request):
        ret = {"status": True, "error": False}
        try:
            if self.request.POST.get('all') == 'all':
                ass =Asset.objects.all()
                for ii in ass:
                    asset_info = auto_asset(ii.inner_ip)
                    asset = Asset.objects.get(inner_ip=ii.inner_ip)
                    asset.osfinger = asset_info['os']
                    asset.hostname = asset_info['localhost']
                    asset.cpu_model = asset_info['cpu_model']
                    asset.mac_addr = asset_info['hwaddr_interfaces']
                    asset.mem_total = asset_info['mem_total']
                    asset.num_cpus = asset_info['num_cpus']
                    asset.virtual = asset_info['virtual']
                    asset.serialnumber = asset_info['serialnumber']
                    asset.dns = asset_info['dns']
                    asset.kernelrelease = asset_info['kernelrelease']
                    asset.inner_ip = asset_info['ip4_interfaces']
                    for de, di in asset_info['disks'].items():
                        #{'avail': '40.05', 'total': '49.09G', 'capacity': '15%', 'used': '6.54'}
                        asset.disk_total = ''.join(de + '=' + di['total'])
                    asset.save()
        except Exception:
            ret = {"status": False, "error": False}
        return HttpResponse(json.dumps(ret))

import traceback
class AssetWebView(LoginRequiredMixin,View):
    '''
    终端登录
    '''

    def post(self, request, *args, **kwargs):
        ret = {'status': True, }
        try:
            id = request.POST.get('id', None)
            obj = Asset.objects.get(id=id)

            ip = obj.pub_ip
            port = obj.port
            username = obj.system_user.username
            password = obj.system_user.password
            try:
                privatekey = obj.system_user.private_key.path
            except Exception as e:
                privatekey = None

            ret.update({"ip": ip, 'port': port, "username": username, 'password': password, "privatekey": privatekey})
            # login_ip = request.META['REMOTE_ADDR']
        except Exception as e:
            ret['status'] = False
            ret['error'] = '请求错误,{}'.format(e)
        finally:
            return HttpResponse(json.dumps(ret))

