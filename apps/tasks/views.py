from django.shortcuts import render,HttpResponse
from  django.views.generic import TemplateView,ListView,View,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from  asset.models import Asset
from  pure_pagination import Paginator,PageNotAnInteger,EmptyPage
from dtops import settings
from django.db.models import Q
import json,time,datetime
import  logging
logger = logging.getLogger('tasks')
from  utils.retasset import getkeyall,salt_alive,accept_key,delete_key
from utils import Saltapi
from  .models import KeyList,CmdLog,Deploy_Model
from .forms import DeployMelForm,DMelForm
# Create your views here.
import pymysql

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
    '''认证节点'''
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
    '''删除节点'''
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

def ret_job(jid):

    salt = Saltapi.SaltAPI()
    ret = []
    for ji in jid:
        r = salt.salt_get_jid_ret(ji)
        ret.append(r)
        print(ret)
    return ret

class RunCmdView(LoginRequiredMixin,View):
    '''命令远程执行'''
    def post(self,request):
        try:
            cmd = self.request.POST.get('command','')
            host_id = self.request.POST.getlist('form_all', '')
            host_id = ','.join(host_id).replace('&',',').replace('id=','')
            asset = Asset.objects.extra(where=['id IN (' + host_id + ')'])
            host_inner=[]
            [host_inner.append(host.inner_ip) for host in asset ]
            host_inner = ','.join(host_inner)
            data = []
            time_t = time.strftime("%Y-%m-%d:%H:%M:%S",time.localtime(time.time()))
            #拒绝执行的危险命令
            deny_cmd = ["rm -rf /","echo","init 0","reboot",]
            try:
                salt = Saltapi.SaltAPI()
                # ret = salt.remote_execution_single(host_inner, 'cmd.run', cmd)
                if cmd in deny_cmd:
                    return HttpResponse(json.dumps({"result": False,"message": cmd +"命令不允许执行,领导会不高兴的"}))
                # for host in host_inner:
                ret = salt.remote_async_execution_module(host_inner,cmd + ';echo "执行状态:"$?')
                rst = salt.salt_get_jid_ret(ret)
                for k,v in rst.items():
                    data.append({'hostname': k, 'data': v})
                # for aaa in ret:
                #     for k, v in aaa.items():
                #         CmdLog.objects.create(host=k,cmd=cmd,ret_code=v,user=request.user)
                #         data.append({'hostname': k, 'data': v})
                # print(ret)
                print(data)

                return HttpResponse(json.dumps({"result": True, "data": data,"set_time":time_t, "message": "执行成功"}))
                # else:
                #     return HttpResponse(json.dumps({"result": False, "data": ret, "message": "执行失败"}))
            except Exception as e:
                logger.error(e)
                return HttpResponse(json.dumps({"result":False,"set_time":time_t,"message":"执行失败,请检查"}))
        except Exception as e:
            logger.error(e)
        return  HttpResponse(json.dumps({"result":True,"message":""}))



class HistoryView(LoginRequiredMixin,ListView):
    '''执行命令记录'''
    template_name = 'tasks/cmd_history.html'
    queryset = CmdLog.objects.all().order_by('-set_time')

    def get_context_data(self, **kwargs):
        '''分页开始'''
        self.queryset = super().get_queryset()
        try:
            page = self.request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(self.queryset, 5, request=self.request)
        asset_list = p.page(page)
        context = {
            "tasks_active": "active",
            "tasks_list_active": "active",
            "cmd_list": asset_list,
        }
        kwargs.update(context)
        return super(HistoryView, self).get_context_data(**kwargs)


class DeployModelView(LoginRequiredMixin,View):
    '''模块部署'''
    def get(self,request):
        model_list = Deploy_Model.objects.all()
        host_list = KeyList.objects.filter(status=True)
        form  = DeployMelForm()
        forms = DMelForm()
        return render(self.request,'tasks/deploy_model.html',context={'forms':forms,'form':form,'model_list':model_list,'host_list':host_list})
    def post(self,request):
        # form = DeployMelForm(request.POST, '')
        # if form.is_valid():
        data = []
        time_t = time.strftime("%Y-%m-%d:%H:%M:%S", time.localtime(time.time()))
        try:
            model_id = request.POST.get('form_all')
            host =  request.POST.get('command')
            # host_inner = []
            # [host_inner.append(host.inner_ip) for host in asset]
            # host_inner = ','.join(host_inner)
            try:
                ress = Deploy_Model.objects.get(name=model_id)
            except Exception as e:
                    logger.error(e,'模块不存在')
                    return HttpResponse(json.dumps({"result": False, "set_time": time_t, "message": "此模块暂未开放,请等待~"}))

                
            salt = Saltapi.SaltAPI()
            # pid = Deploy_Model.objects.filter(name=model_id)
            w = salt.salt_state(host,ress.detail,'list')
            print(w['jid'])
            rst = {}
            t = 0
            r = None
            while (t < 10):
                rst =salt.salt_get_jid_ret(w['jid'])
                print(rst)
                if rst:
                    print(len(rst))
                    r = True
                    break
                t +=1
            print(r)
            print(rst)
            if r:

                # nn = salt.salt_get_jid_ret(w['jid'])
                for k,v in rst.items():
                    print(k,v)
                    # # data.append({'hostname':k})
                    # for kk,vv in v.items():

                        # v = ','.join(v)
                        # print(v)
                    data.append({ 'hostname':k,'data':str(v)})
                # if not data:
                #     return HttpResponse(json.dumps({"result": True, "data": data, "set_time": time_t, "message": "稍后查询"}))

            print(data)
            return HttpResponse(json.dumps({"result": True, "data": data, "set_time": time_t, "message": "执行成功"}))

        except Exception as e:
            logger.error(e)
            return HttpResponse(json.dumps({"result": False, "data": data, "set_time": time_t, "message": "执行失败"}))

        return HttpResponse(json.dumps({"result": True, "data": data, "set_time": time_t, "message": "执行成功"}))





