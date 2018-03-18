from django.conf.urls import url


from  users.views import UserListView,user_login,logoutview,LoginView,UserCreateView,UserDeleteView

app_name = 'users'
urlpatterns = [
    url(r'login/$', LoginView.as_view(), name='login'),
    url(r'create_user/$', UserCreateView.as_view(), name='create_user'),
    url(r'user_delete/(?P<nid_pk>\d+)/$', UserDeleteView.as_view(), name='user_delete'),
    url(r'logout/$', logoutview, name='logout'),
    url(r'user_list/$', UserListView.as_view(), name='user_list'),
]