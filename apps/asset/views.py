from django.shortcuts import render,HttpResponseRedirect,HttpResponse,reverse
from django.db.models import Q
from django.views.generic import ListView,TemplateView,UpdateView,DetailView,DeleteView,View,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from  pure_pagination import PageNotAnInteger,Paginator,EmptyPage

from  .models import Asset,System_User,ProductLine,Cloud_Platform,Tag
from .forms import AddAssetModelForm
# Create your views here.

class AssetListView(LoginRequiredMixin,ListView):
    '''资产列表'''
    queryset = Asset.objects.all()

    template_name = 'asset/asset_list.html'

    def get_context_data(self, **kwargs):
        try:
            page = self.request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(self.queryset,5,request=self.request)
        asset_list = p.page(page)
        form_list = AddAssetModelForm()
        context = {
            "asset_active":"active",
            "asset_list_active": "active",
            "asset_list":asset_list,
            "form_list":form_list,
        }
        kwargs.update(context)
        return super(AssetListView,self).get_context_data(**kwargs)


class SystemUserListAllView(LoginRequiredMixin,ListView):
    '''系统用户列表'''
    queryset = System_User.objects.all().order_by('-create_time')
    template_name = 'asset/sys_user.html'

    def get_context_data(self, **kwargs):
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
    model = Asset
    form_class = AddAssetModelForm
    context_object_name = 'form_list'
    template_name = 'asset/create_asset.html'
    success_url = reverse_lazy('asset:asset_list')