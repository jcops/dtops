from django.shortcuts import render
from  django.views.generic import TemplateView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from  asset.models import Asset
from  pure_pagination import Paginator,PageNotAnInteger,EmptyPage
from dtops import settings
from django.db.models import Q
# Create your views here.


class CmdListView(LoginRequiredMixin,ListView):
    template_name = 'tasks/command.html'
    '''资产列表'''
    queryset = Asset.objects.all()

    def get_context_data(self, **kwargs):
        '''搜索/分页开始'''
        self.queryset = super().get_queryset()
        if self.request.GET.get('name'):
            query = self.request.GET.get('name', None)

            queryset = Asset.objects.filter(Q(hostname__contains=query) | Q(inner_ip__contains=query) | Q(pub_ip=query))
            print(queryset)
        else:
            queryset = super().get_queryset()

        try:
            page = self.request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(queryset, 5, request=self.request)
        asset_list = p.page(page)
        # form_list = AddAssetModelForm

        context = {
            "tasks_active": "active",
            "tasks_list_active": "active",
            "asset_list": asset_list,
            # "form_list":form_list,

            "web_ssh": getattr(settings, 'web_ssh'),
            "web_port": getattr(settings, 'web_port'),

        }
        kwargs.update(context)
        return super(CmdListView, self).get_context_data(**kwargs)