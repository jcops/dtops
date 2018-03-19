from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect,reverse,render_to_response
from django.views.generic import View,TemplateView,DetailView,CreateView,UpdateView,FormView,ListView,DeleteView
from django.views.generic.base import View
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from  django.contrib.auth.hashers import make_password
from  django.contrib.auth.decorators import login_required
import json
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.utils.decorators import method_decorator

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


from users.models import UserProfile,UserLog
from  users.forms import LoginForm,UserCreateForm,UserUpdateModelForm
from utils.get_ip import Get_Ip
# # Create your views here.



class LoginView(View):
    '''用户登录'''
    error=""
    def get(self, request):

        form_login = LoginForm()
        redirect_url = request.GET.get('next', '')
        return render(request,'users/login_two_columns.html',{"form_login":form_login,"redirect_url":redirect_url})

    def post(self, request):
        form_login = LoginForm(request.POST)
        if form_login.is_valid():
            # username = form_login.cleaned_data['username']
            # password = form_login.cleaned_data['password']
            username = request.POST.get("username","")
            password = request.POST.get("password","")
            user = authenticate(username=username, password=password)
            # 如果不是null说明验证成功
            if user is not None:
                # login_in 两参数：request, user
                # request是要render回去的。这些信息也就随着返回浏览器。完成登录
                login(request, user)
                # request.session['is_login']=request.user
                request.session["username"] = request.user.id
                request.session.set_expiry(600)
                # 跳转到首页 user request会被带回到首页
                login_ip = request.META.get("REMOTE_ADDR","unknown")
                login_agent = request.META.get("HTTP_USER_AGENT","unknown")
                get_ip = Get_Ip(login_ip)
                get_ip ="".join(get_ip.getip())
                UserLog.objects.create(username=request.user,ip=login_ip,city=get_ip,user_agent=login_agent)
                redirect_url = request.POST.get('next', '')
                if redirect_url:
                    return HttpResponseRedirect(redirect_url)
                # 跳转到首页 user request会被带回到首页
                return HttpResponseRedirect(reverse("index"))

            return render(request, 'users/login_two_columns.html',
                          {"msg": "用户名不存在!",
                           "form_login": form_login,
                           })




def logoutview(request):
    '''用户退出'''
    request.session.clear()
    return HttpResponseRedirect(reverse('users:login'))


class IndexView(LoginRequiredMixin,View):
    '''首页仪表盘'''
    # model = 'UserProfile'
    # template_name = 'index.html'
    # @method_decorator(login_required)
    def get(self,request):
        if not request.user.is_authenticated():
            return  HttpResponseRedirect(reverse('users:login'))
        user_total = UserProfile.objects.all().count()
        return render(request,'index.html',{"user_total":user_total})


class UserListView(LoginRequiredMixin,ListView):
    '''用户列表'''

    template_name = 'users/user_list.html'
    model = UserProfile
    context_object_name = 'user_list'
    queryset = UserProfile.objects.all()


    def get_context_data(self, **kwargs):
        context = {
            "user_active": "active",
            "user_list_active": "active",

        }
        kwargs.update(context)
        return super(UserListView, self).get_context_data(**kwargs)

    def get_queryset(self,*args,**kwargs):
        self.queryset = super().get_queryset()
        if self.request.GET.get('search'):
            query = self.request.GET.get('search','')
            queryset = self.queryset.filter(Q(username =query )|Q(nick_name=query)|Q(mobile=query)|Q(email=query))
        else:
            queryset = super().get_queryset()
        return queryset

class UserCreateView(LoginRequiredMixin,View):
    '''创建用户'''
    def get(self,request):

        form = UserCreateForm()
        return render(request,'users/create_user.html',
                      {"form":form,
                      })

    def post(self,request):
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = UserProfile.objects.filter(username=form.cleaned_data['username'])
            if user:
                return render(request,'users/create_user.html', {'msg': '用户已存在'})
            else:
                comment = UserProfile()
                comment.username = form.cleaned_data['username']
                comment.password = make_password(form.cleaned_data['password'])
                comment.nick_name = form.cleaned_data['nick_name']
                comment.email = form.cleaned_data['email']
                comment.mobile = form.cleaned_data['mobile']
                comment.save()
                return HttpResponseRedirect(reverse('users:user_list'))

        else:
            form =UserCreateForm()

        return render(request,'users/create_user.html', {'form': form})


class UserDeleteView(LoginRequiredMixin,View):
    '''删除用户'''
    def get(self,request,nid_pk):
        ret = {'status': True, 'error': None}
        # user_id = request.POST.get('nid',None)

        UserProfile.objects.get(id=int(nid_pk)).delete()

        # return HttpResponse(json.dumps(ret))
        return HttpResponseRedirect(reverse('users:user_list'))



class UserDelView(LoginRequiredMixin,View):
    '''删除用户(ajax)'''
    model = UserProfile

    def post(self,request):

        ret = {"status":True,"error":"None"}

        nid = request.POST.get("nid",'')
        UserProfile.objects.get(id=int(nid)).delete()
        return HttpResponse(json.dumps(ret))


class UserHistoryView(LoginRequiredMixin,ListView):
    '''平台登录日志'''
    queryset = UserLog.objects.all().order_by('-login_time')
    template_name = 'users/user_history.html'
    # context_object_name = 'user_history'

    def get_context_data(self, **kwargs):
        try:
            page = self.request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
            # 这里指从allorg中取五个出来，每页显示3个
        p = Paginator(self.queryset, 10, request=self.request)
        page_list = p.page(page)
        print(page_list)
        context = {
            "platform_active": "active",
            "user_log_active": "active",
            "page_list":page_list,
        }
        kwargs.update(context)
        return super(UserHistoryView, self).get_context_data(**kwargs)

class UserDeatilView(LoginRequiredMixin,DetailView):
    '''用户详情页'''
    model = UserProfile
    template_name = 'users/user_detail.html'
    def get_context_data(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        detail = UserProfile.objects.get(id=pk)
        context = {
            "detail_list":detail,
            "user_list":detail,
            "nid": pk,
        }
        kwargs.update(context)
        return  super(UserDeatilView,self).get_context_data(**kwargs)

class UserUpdateView(LoginRequiredMixin,UpdateView):
    '''用户信息更新'''
    model = UserProfile
    form_class = UserUpdateModelForm
    template_name = 'users/user_update.html'
    context_object_name = 'user_update'
    success_url = reverse_lazy('users:user_list')
    def get_context_data(self, **kwargs):
        return  super(UserUpdateView,self).get_context_data(**kwargs)
    def form_valid(self, form):
        return  super(UserUpdateView,self).form_valid(form)
