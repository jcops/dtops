from django.shortcuts import render,HttpResponse
from  django.views.generic import TemplateView,ListView,View,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from  asset.models import Asset
from  pure_pagination import Paginator,PageNotAnInteger,EmptyPage
from dtops import settings
from django.db.models import Q
import json
import  logging
logger = logging.getLogger('tasks')
from  utils.retasset import getkeyall,salt_alive,accept_key,delete_key
from  .models import KeyList
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


def save_key_all():
    try:
        minions, minion_pre = getkeyall()
        print(minions, minion_pre)
        if minions:
            for min_list in minions:
                aa = KeyList.objects.filter(name=min_list)
                print(aa)
                # for i in aa:

                if aa:
                    KeyList.objects.filter(name=min_list).update(status=1)
                else:
                        # KeyList.objects.create(name=i, status=1)
                    aaa = KeyList()
                    aaa.name =min_list
                    aaa.status=1
                    aaa.save()

        if minion_pre:
            for min_pre in minion_pre:
                bb = KeyList.objects.filter(name=min_pre)
                if bb:
                    KeyList.objects.filter(name=bb, status=False).update()
                else:
                    KeyList.objects.create(name=min_pre, status=False)
    except Exception as e:
        print(e)


class GetKeyListView(LoginRequiredMixin,ListView):
    '''key节点列表'''
    queryset = KeyList
    template_name = 'tasks/key_list.html'

    def get_context_data(self, **kwargs):
        try:
            save_key_all()
            minions = self.queryset.objects.filter(status=True)
            minion_pre = self.queryset.objects.filter(status=False)
            context = {
                "minions": minions,
                "minion_pre": minion_pre,
            }
            kwargs.update(context)
            return  super(GetKeyListView,self).get_context_data(**kwargs)
            # return render(self.request, 'tasks/key_list.html', context={"minions": minions, "minion_pre": minion_pre})
        except Exception as e:
            logger.error(e)
        return super(GetKeyListView, self).get_context_data(**kwargs)



# class GetKeyListView(LoginRequiredMixin,View):
#     '''key节点列表'''
#     def get(self,request):
#         try:
#             save_key_all()
#             minions = KeyList.objects.filter(status=True)
#             minion_pre = KeyList.objects.filter(status=False)
#             # minions,minion_pre = getkeyall()
#             print(minions,minion_pre)
#             return render(self.request,'tasks/key_list.html',context={"minions":minions,"minion_pre":minion_pre})
#         except Exception as e:
#             logger.error(e)
#
#     def post(self,request):
#         pass

# class KeyDelView(LoginRequiredMixin,DeleteView):
class KeyTestView(LoginRequiredMixin,View):
    '''测试key节点连接'''
    def post(self,request):
        ret = {'status': True, 'error': None, 'host': ''}
        try:

            nid = request.POST.get('nid','')
            if nid:
                li = KeyList.objects.get(id=int(nid))
                sli =salt_alive(li)
                print(sli)
                print(type(sli))
                for i in sli:
                    if sli[i] == True:
                        ret = {'status': True, 'error': None, 'host':i}
                    return  HttpResponse(json.dumps(ret))
            else:
                ret = {'status': False, 'error': '不能为空', 'host': ''}
            return HttpResponse(json.dumps(ret))
        except Exception as  e:
            logger.error(e)
        finally:
            return HttpResponse(json.dumps(ret))

class AccKeyView(LoginRequiredMixin,View):
    def post(self,request):
        ret = {'status':True,'error':'','host':''}
        try:
            nid = self.request.POST.get('nid','')
            nids = KeyList.objects.get(id=int(nid))

            ret = accept_key(nids)
            if ret:
                KeyList.objects.filter(name=nids).update(status=1)
                ret = {'status': True, 'error': '', 'host': nids.name}
            return  HttpResponse(json.dumps(ret))
        except Exception as e:
            logger.error(e)

        finally:
            return HttpResponse(json.dumps(ret))

class KeyDelView(LoginRequiredMixin,View):
    def post(self,request):
        ret = {'status':True,'error':'','host':''}
        try:
            nid = self.request.POST.get('nid','')
            nids = KeyList.objects.get(id=int(nid))
            print(nids)
            if nids:
                print(nids)
                d  = delete_key(nids.name)
                if d:
                    # KeyList.objects.update(status=0)
                    KeyList.objects.get(name=nids.name).delete()
                    ret = {'status': True, 'error': '', 'host': nids.name}
                return  HttpResponse(json.dumps(ret))
        except Exception as e:
            logger.error(e)
        finally:

            return HttpResponse(json.dumps(ret))