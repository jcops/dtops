from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect,reverse,render_to_response
from django.views.generic import View,TemplateView,DetailView,CreateView,UpdateView,FormView,ListView,DeleteView
from django.views.generic.base import View
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from  django.contrib.auth.hashers import make_password
import json
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.utils.decorators import method_decorator
from users.models import UserProfile,UserLog
from  users.forms import LoginForm,UserCreateForm
# # Create your views here.
#
# #
# # class LoginView(FormView):
# #     template_name = 'login_two_columns.html'
# #     form_class = UserLoginForm
# #     # success_url = ''
# #
# #     def form_valid(self, form):
# #         login(self.request, form.get_user())
# #         return  redirect(self.get_success_url())
#
#
#
# class LoginView(View):
#
#     def get(self,request):
#         redirect_url = request.GET.get('next','')
#         return render(request,'login_two_columns.html',{"redirect_url":redirect_url})
#
#     def post(self,request):
#         login_form = UserLoginForm(request.POST)
#         if login_form.is_valid():
#             # 取不到时为空，username，password为前端页面name值
#             username = request.POST.get("username", "")
#             password = request.POST.get("password", "")
#             # 成功返回user对象,失败返回null
#             user = authenticate(username=username, password=password)
#             # 如果不是null说明验证成功
#             print(user)
#             if user is not None:
#                 # login_in 两参数：request, user
#                 # 实际是对request写了一部分东西进去，然后在render的时候：
#                 # request是要render回去的。这些信息也就随着返回浏览器。完成登录
#                 login(request, user)
#                 # 跳转到首页 user request会被带回到首页
#                 redirect_url = request.POST.get('next', '')
#                 if redirect_url:
#                     return HttpResponseRedirect(redirect_url)
#                 # 跳转到首页 user request会被带回到首页
#                 return HttpResponseRedirect(reverse("index"))
#         else:
#             return render(request,'login_two_columns.html',{'msg':'用户名或密码错误','login_form':login_form})

# class LoginView(View):
#     '''基于类实现用户登录'''
#     #直接调用get方法免去判断
#     def get(self,request):
#         # render就是渲染html返回用户
#         # render三变量: request 模板名称 一个字典写明传给前端的值
#         redirect_url = request.GET.get('next', '')
#         return render(request,'users/login_two_columns.html',{'redirect_url': redirect_url,})
#     def post(self,request):
#         # 类实例化需要一个字典参数dict:request.POST就是一个QueryDict所以直接传入
#         # POST中的username,password，会对应到form中
#         login_form = LoginForm(request.POST)
#         # is_valid判断我们字段是否有错执行我们原有逻辑，验证失败跳回login页面
#         if login_form.is_valid():
#             # 取不到时为空，username，password为前端页面name值
#             user_name = login_form.cleaned_data['username']
#             pass_word = login_form.cleaned_data['password']
#             # 成功返回user对象,失败返回null
#             user = authenticate(username=user_name,password=pass_word)
#             # 如果不是null说明验证成功
#             if user is not None:
#                 # login_in 两参数：request, user
#                 # 实际是对request写了一部分东西进去，然后在render的时候：
#                 # request是要render回去的。这些信息也就随着返回浏览器。完成登录
#                 login(request,user)
#                 # 跳转到首页 user request会被带回到首页
#                 redirect_url = request.POST.get('next', '')
#                 if redirect_url:
#                     return HttpResponseRedirect(redirect_url)
#                 # 跳转到首页 user request会被带回到首页
#                 return HttpResponseRedirect(reverse("index"))
#         else:
#             login_form = LoginForm(self.request)
#             # 没有成功说明里面的值是None，并再次跳转回主页面
#             return render(request, 'users/login_two_columns.html', {"msg": "用户名或密码错误", "login_form":login_form})
#             #return HttpResponse("Please Check Your Registration Form")

def user_login(request):
    '''用戶登錄'''

    if request.method == "POST":
        form_login = LoginForm(request.POST)
        if form_login.is_valid():
            username = form_login.cleaned_data['username']
            password = form_login.cleaned_data['password']
            user = authenticate(username=username,password=password)
            # 如果不是null说明验证成功
            if user is not None:
                # login_in 两参数：request, user
                # 实际是对request写了一部分东西进去，然后在render的时候：
                # request是要render回去的。这些信息也就随着返回浏览器。完成登录
                login(request,user)
                # request.session['is_login']=request.user
                request.session["username"] = request.user.id
                request.session.set_expiry(600)
                # return HttpResponseRedirect(reverse('index'))
                # 跳转到首页 user request会被带回到首页
                redirect_url = request.POST.get('next', '')
                if redirect_url:
                    return HttpResponseRedirect(redirect_url)
                # 跳转到首页 user request会被带回到首页
                return HttpResponseRedirect(reverse("index"))
            return render(request,'users/login_two_columns.html',{"msg":"用户名不存在! ","form_login":form_login})
        else:

            # 没有成功说明里面的值是None，并再次跳转回主页面
            return render(request, 'users/login_two_columns.html',{"msg":"用户名或密码错误! ","form_login":form_login,'request': request,})

    # 获取登录页面为get
    elif request.method == "GET":
        # render就是渲染html返回用户
        form_login = LoginForm()
        # render三变量: request 模板名称 一个字典写明传给前端的值
        return render(request,'users/login_two_columns.html',{"form_login":form_login,'request': request,})

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
                UserLog.objects.create(username=request.user,ip=login_ip,user_agent=login_agent)
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
    request.session.clear()
    return HttpResponseRedirect(reverse('users:login'))


class IndexView(View):
    # model = 'UserProfile'
    # template_name = 'index.html'
    def get(self,request):
        if not request.user.is_authenticated():
            return  HttpResponseRedirect(reverse('users:login'))
        user_total = UserProfile.objects.all().count()
        return render(request,'index.html',{"user_total":user_total})

class UserListView(ListView):

    template_name = 'users/user_list.html'
    model = UserProfile
    context_object_name = 'user_list'
    # model = UserProfile
    # context_object_name = 'user_list'
    # def get(self,request):
    #     user_list = UserProfile.objects.all()
    #     form = UserCreateForm()
    #     redirect_url = request.GET.get('next', '')
    #     return render(request,'users/user_list.html',
    #                   {"form":form,
    #                     "user_list":user_list,
    #                   })

    def get_context_data(self, **kwargs):
        context = {
            "user_active": "active",
            "user_list_active": "active",
        }
        kwargs.update(context)
        return super(UserListView, self).get_context_data(**kwargs)

class UserCreateView(View):
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


class UserDeleteView(View):

    def get(self,request,nid_pk):
        ret = {'status': True, 'error': None}
        # user_id = request.POST.get('nid',None)

        UserProfile.objects.get(id=int(nid_pk)).delete()

        # return HttpResponse(json.dumps(ret))
        return HttpResponseRedirect(reverse('users:user_list'))

class UserHistoryView(ListView):
    '''
    平台登录日志
    '''

    queryset = UserLog.objects.all().order_by('-login_time')
    template_name = 'users/user_history.html'
    context_object_name = 'user_history'


    def get_context_data(self, **kwargs):
        context = {
            "platform_active": "active",
            "user_log_active": "active",
        }
        kwargs.update(context)
        return super(UserHistoryView, self).get_context_data(**kwargs)