from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect
from django.views.generic import View,TemplateView,DetailView,CreateView,UpdateView,FormView,ListView,DeleteView
from django.views.generic.base import View
from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.contrib.auth import logout,login,authenticate

from users.models import UserProfile,UserLog
from  users.forms import UserLoginForm
# Create your views here.

#
# class LoginView(FormView):
#     template_name = 'login_two_columns.html'
#     form_class = UserLoginForm
#     # success_url = ''
#
#     def form_valid(self, form):
#         login(self.request, form.get_user())
#         return  redirect(self.get_success_url())



class LoginView(View):

    def get(self,request):
        redirect_url = request.POST.get('next','')
        return  render(request,'login_two_columns.html',{"redirect_url":redirect_url})

    def post(self,request):
        form_class = UserLoginForm(request.POST)
        if form_class.is_valid():
            username = request.POST.get('username','')
            password = request.POST.get('password','')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                request.session['is_login'] = True
                redirect_url = request.POST.get('next', '')
                if redirect_url:
                    return HttpResponseRedirect(redirect_url)

                return HttpResponseRedirect(reverse('index'))
        else:
            return  render(request,'login_two_columns.html',{'msg':'用户名或密码错误',})

class IndexView(View):

    def get(self,request):
        return render(request,'index.html',{})