from django.conf.urls import url


from  users.views import UserListView,user_login,logoutview

app_name = 'users'
urlpatterns = [
    url(r'login/$', user_login, name='login'),
    url(r'logout/$', logoutview, name='logout'),
    url(r'user_list/$', UserListView.as_view(), name='user_list'),
]