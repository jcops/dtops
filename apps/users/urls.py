from django.conf.urls import url


from  users.views import LoginView,UserListView

app_name = 'users'
urlpatterns = [
    url(r'login/$', LoginView.as_view(), name='login'),
    url(r'user_list/$', UserListView.as_view(), name='user_list'),
]