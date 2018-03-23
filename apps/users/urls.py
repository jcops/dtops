from django.conf.urls import url


from  users.views import UserListView,logoutview,LoginView,UserCreateView, \
                         UserDeleteView,UserHistoryView,UserDeatilView,UserUpdateView,UserDelView,UpdateUserView

app_name = 'users'
urlpatterns = [
    #登录
    url(r'login/$', LoginView.as_view(), name='login'),
    #创建用户
    url(r'create_user/$', UserCreateView.as_view(), name='create_user'),
    #删除用户
    # url(r'user_delete/(?P<nid_pk>\d+)/$', UserDeleteView.as_view(), name='user_delete'),
    # 用户删除（ajax）
    url(r'user_del/$', UserDelView.as_view(), name='user_del'),
    #用户登出
    url(r'logout/$', logoutview, name='logout'),
    #用户列表
    url(r'user_list/$', UserListView.as_view(), name='user_list'),
    #用户登录平台日志
    url(r'user_history/$', UserHistoryView.as_view(), name='user_history'),
    #用户详情
    url(r'user_detail/(?P<pk>\d+)/$', UserDeatilView.as_view(), name='user_detail'),
    #用户更新
    url(r'user_update/(?P<pk>\d+)/$', UserUpdateView.as_view(), name='user_update'),
    # 用户更新
    url(r'pwd_update/$', UpdateUserView.as_view(), name='pwd_update'),

]