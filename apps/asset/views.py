from django.shortcuts import render,HttpResponseRedirect,HttpResponse,reverse
from django.db.models import Q
from django.views.generic import ListView,TemplateView,UpdateView,DetailView,DeleteView,View,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
import json
import  xlwt,time,xlrd
from  pure_pagination import PageNotAnInteger,Paginator,EmptyPage
from  dtops import settings
from  .models import Asset,System_User,ProductLine,Cloud_Platform,Tag
from .forms import AddAssetModelForm,AssetUpdateModelForm,SysUserCreateModelForm,SysUserUpdateModelForm,FileFrom
from utils.Saltapi import SaltAPI
from utils.retasset import auto_asset,MyThread
from utils.Export_assets import write_excel
#打印栈信息
import traceback
import logging
logger = logging.getLogger('asset')
salt = SaltAPI(url="https://118.25.39.84:8000", user="saltapi", password="saltapi123")
# Create your views here.

class AssetListView(LoginRequiredMixin,ListView):
    '''资产列表'''
    queryset = Asset.objects.all()
    template_name = 'asset/asset_list.html'

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
            page = self.request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(queryset,5,request=self.request)
        asset_list = p.page(page)
        # form_list = AddAssetModelForm
        files = FileFrom()
        context = {
            "asset_active":"active",
            "asset_list_active": "active",
            "asset_list":asset_list,
            # "form_list":form_list,
            "files":files,
            "web_ssh": getattr(settings, 'web_ssh'),
            "web_port": getattr(settings, 'web_port'),


        }
        kwargs.update(context)
        return super(AssetListView,self).get_context_data(**kwargs)

# 以下搜索方法对开启了分页模式就不会生效
    # def get_queryset(self):
    #     self.queryset = super().get_queryset()
    #     if self.request.GET.get('name'):
    #         query = self.request.GET.get('name', None)
    #         print(query)
    #         queryset = Asset.objects.filter(Q(hostname=query) | Q(inner_ip=query) | Q(pub_ip=query))
    #         print(queryset)
    #     else:
    #         queryset = super().get_queryset()
    #         print(queryset)
    #     return queryset


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
            else:
                ids = request.POST.getlist('id',None)
                print(ids)
                idstring = ','.join(ids)
                Asset.objects.extra(where=['id IN ('+ idstring +')']).delete()
        except Exception as e:
            ret = {"status": False, "error": '错误{}'.format(e)}
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
    '''资产更新'''
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
    '''更新资产信息'''
    def post(self,request):
        ret = {"status": True, "error": False}
        try:
            if self.request.POST.get('all') == 'all':
                ass =Asset.objects.all()
                ids_list =[ i.inner_ip for i in ass]
                files = range(len(ids_list))
                t_list = []
                t_data = []
                # for i in files:
                #     t = MyThread(auto_asset, (ids_list[i],))
                #     t_list.append(t)
                #     t.start()
                # for t in t_list:
                #     t.join()  # 一定要join，不然主线程比子线程跑的快，会拿不到结果
                #     t_data.append(t.get_result())
                # print(t_data)
                        # asset_info = auto_asset(ii.inner_ip)
                    # asset = ass.get(inner_ip=ii.inner_ip)
                for i in files:
                    t = MyThread(auto_asset, (ids_list[i],))
                    t_list.append(t)
                    t.start()
                for t in t_list:
                    t.join()  # 一定要join，不然主线程比子线程跑的快，会拿不到结果
                    t_data.append(t.get_result())



                for data_dicts in t_data:
                    asset = Asset.objects.get(inner_ip=data_dicts['ip4_interfaces'])
                    asset.osfinger = data_dicts['os']
                    asset.hostname = data_dicts['localhost']
                    asset.cpu_model = data_dicts['cpu_model']
                    asset.mac_addr = data_dicts['hwaddr_interfaces']
                    asset.mem_total =data_dicts['mem_total']
                    asset.num_cpus =data_dicts['num_cpus']
                    asset.virtual = data_dicts['virtual']
                    asset.serialnumber =data_dicts['serialnumber']
                    asset.dns =data_dicts['dns']
                    asset.kernelrelease = data_dicts['kernelrelease']
                    asset.inner_ip = data_dicts['ip4_interfaces']
                    for de, di in data_dicts['disks'].items():
                    #{'avail': '40.05', 'total': '49.09G', 'capacity': '15%', 'used': '6.54'}
                        asset.disk_total = ''.join(de + '=' + di['total'])
                    asset.save()
        except Exception as e:
            logger.error(e)
            ret = {"status": False, "error": '{}'.format(e)}
        return HttpResponse(json.dumps(ret))


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

class AddSysUserView(LoginRequiredMixin,CreateView):
    '''新建系统用户'''
    model = System_User
    form_class = SysUserCreateModelForm
    context_object_name = 'form_list'
    template_name = 'asset/sysuser_create.html'
    success_url = reverse_lazy('asset:system_user')

class Del_SysUserView(LoginRequiredMixin,View):
    '''删除系统用户(ajax)'''
    def post(self,request):
        ret = {"status":True,"error":False}
        try:
            nid = request.POST.get("nid", '')
            if nid:
                System_User.objects.get(id=int(nid)).delete()
        except Exception:
            ret = {"status": False, "error": '错误'}
        return HttpResponse(json.dumps(ret))

class SysUserDetailView(LoginRequiredMixin,DetailView):
    '''系统用户详情'''
    model = System_User
    template_name = 'asset/sysuser_detail.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg,None)
        detail = System_User.objects.get(id=pk)
        print(detail)
        contenxt = {
            "detail":detail,
        }
        kwargs.update(contenxt)
        return super(SysUserDetailView,self).get_context_data(**kwargs)

class SysUserUpdateView(LoginRequiredMixin,UpdateView):
    '''系统用户更新'''
    model = System_User
    form_class = SysUserCreateModelForm
    template_name = 'asset/sysuser_update.html'
    success_url = reverse_lazy('asset:system_user')
    context_object_name = 'sysuser_update'

    def get_context_data(self, **kwargs):
        context = {
            "asset_active": "active",
            "asset_list_active": "active",
        }
        kwargs.update(context)
        return super(SysUserUpdateView,self).get_context_data(**kwargs)

class ExAssetView(LoginRequiredMixin,View):
    '''资产导出'''
    def get(self,request):
        row = 1
        style_heading = xlwt.easyxf("""
                font:
                    name Arial,
                    colour_index white,
                    bold on,
                    height 0xA0;
                align:
                    wrap off,
                    vert center,
                    horiz center;
                pattern:
                    pattern solid,
                    fore-colour ocean_blue;
                borders:
                    left THIN,
                    right THIN,
                    top THIN,
                    bottom THIN;
                """)
        style_body = xlwt.easyxf("""
                font:
                    name Arial,
                    bold off,
                    height 0XA0;
                align:
                    wrap on,
                    vert center,
                    horiz left;
                borders:
                    left THIN,
                    right THIN,
                    top THIN,
                    bottom THIN;
                """)
        fmts = [
            'M/D/YY',
            'D-MMM-YY',
            'D-MMM',
            'MMM-YY',
            'h:mm AM/PM',
            'h:mm:ss AM/PM',
            'h:mm',
            'h:mm:ss',
            'M/D/YY h:mm',
            'mm:ss',
            '[h]:mm:ss',
            'mm:ss.0',
        ]

        style_green = xlwt.easyxf(" pattern: pattern solid,fore-colour 0x11;")
        style_red = xlwt.easyxf(" pattern: pattern solid,fore-colour 0x0A;")
        style_body.num_format_str = fmts[0]
        ass_all = Asset.objects.all()
        response = HttpResponse(content_type='application/vnd.ms-excel')#这里响应对象获得了一个特殊的mime类型,告诉浏览器这是个exell文件不是html
        response['Content-Disposition'] = 'attachment; filename=asset'+time.strftime('%Y%m%d',time.localtime(time.time()))+'.xls'#这里响应对象获得了附加的Content-Disposition协议头,它含有excel文件的名称,文件名随意,当浏览器访问它时,会以"另存为"对话框中使用它
        f = xlwt.Workbook()  # 创建工作簿
        sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
        # sheet1.write(0, 1, label='内网ip', style_heading)
        sheet1.write(0, 0, '主机名', style_heading)
        sheet1.write(0, 1, '内网ip', style_heading)
        sheet1.write(0, 2, '外网ip', style_heading)
        sheet1.write(0, 3, '端口', style_heading)
        sheet1.write(0, 4, '总内存', style_heading)
        sheet1.write(0, 5, '总磁盘', style_heading)
        sheet1.write(0, 6, 'CPU型号', style_heading)
        sheet1.write(0, 7, 'CPU核数', style_heading)
        sheet1.write(0, 8, '系统版本', style_heading)
        sheet1.write(0, 9, '系统发行版本', style_heading)
        sheet1.write(0, 10, 'DNS', style_heading)
        sheet1.write(0, 11, 'MAC地址', style_heading)
        sheet1.write(0, 12, '内核版本', style_heading)
        sheet1.write(0, 13, '序列号', style_heading)
        sheet1.write(0, 14, '虚拟化', style_heading)
        sheet1.write(0, 15, '状态', style_heading)
        sheet1.write(0, 16, '系统用户', style_heading)
        sheet1.write(0, 17, '产品线', style_heading)
        sheet1.write(0, 18, '标签', style_heading)
        sheet1.write(0, 19, '云平台', style_heading)
        sheet1.write(0, 20, '创建用户', style_heading)
        sheet1.write(0, 21, '备注', style_heading)
        sheet1.write(0, 22, '创建时间', style_heading)
        sheet1.write(0, 23, '更新时间', style_heading)
        for ass in ass_all:
            sheet1.write(row, 0, ass.hostname)
            sheet1.write(row, 1, ass.inner_ip)
            sheet1.write(row, 2, ass.pub_ip)
            sheet1.write(row, 3, ass.port)
            sheet1.write(row, 4, ass.mem_total)
            sheet1.write(row, 5, ass.disk_total)
            sheet1.write(row, 6, ass.cpu_model)
            sheet1.write(row, 7, ass.num_cpus)
            sheet1.write(row, 8, ass.osfinger)
            sheet1.write(row, 9, ass.osrelease)
            sheet1.write(row, 10, ass.dns)
            sheet1.write(row, 11, ass.mac_addr)
            sheet1.write(row, 12, ass.kernelrelease)
            sheet1.write(row, 13, ass.serialnumber)
            sheet1.write(row, 14, ass.virtual)
            if ass.status == '正常':

                sheet1.write(row, 15, ass.status,style_green)
            else:
                sheet1.write(row, 15, ass.status, style_red)

            sheet1.write(row, 16, ass.system_user.name + '--' + ass.system_user.username)
            sheet1.write(row, 17, ass.product.name)
            for tags in ass.tag.all():
                sheet1.write(row, 18, tags.name)
            sheet1.write(row, 19, ass.cloud_platform.cloud)
            sheet1.write(row, 20, ass.create_user)
            sheet1.write(row, 21, ass.detail)
            sheet1.write(row, 22, str(ass.create_time), style_body)
            sheet1.write(row, 23, str(ass.update_time), style_body)

            row += 1
        f.save(response)#写入表格
        return response

class ImAssetView(LoginRequiredMixin,View):
    '''资产导入'''
    def post(self, request):
        form = FileFrom(request.POST, request.FILES,'')
        # file_sjdr = request.POST.get('file_keywork')
        print(form)
        if form.is_valid():
            print(request.FILES['file'])
            files = request.FILES['file']
            with open('asset.xls', mode='wb') as f:
                for chunk in files.chunks():
                    f.write(chunk)
            data = xlrd.open_workbook('asset.xls')
            # 获取工作表sheet1
            table = data.sheet_by_name('sheet1')
            # 获取行数和列数
            nrows, ncols = table.nrows, table.ncols
            #
            colnames = table.row_values(0)
            w = []
            x = y = 0
            for i in range(1, nrows):
                # 获取每行的值
                row = table.row_values(i)
                for j in range(0, ncols):  #
                    if type(row[j]) == float:
                        row[j] = int(row[j])
                if row:
                    if Asset.objects.filter(hostname=row[0], inner_ip=row[1], pub_ip=row[2]).exists():
                        x += 1
                    else:
                        y += 1
                        w.append(Asset(hostname=row[0], inner_ip=row[1], pub_ip=row[2], port=row[3], mem_total=row[4],
                                       disk_total=row[5], cpu_model=row[6], num_cpus=row[7], osfinger=row[8],
                                       osrelease=row[9],
                                       dns=row[10], mac_addr=row[11], kernelrelease=row[12], serialnumber=row[13],
                                       virtual=row[14], status=row[15], detail=row[16]))

            Asset.objects.bulk_create(w)
            da = {"status": True, "success": '导入成功'}
            import  os
            os.remove('asset.xls')
            print('成功导入'+ str(y),'导入失败'+str(x))
            return  HttpResponseRedirect(reverse('asset:asset_list'))
        else:
            return HttpResponseRedirect(reverse('asset:asset_list'))