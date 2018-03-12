from django.conf.urls import url


from  users.views import LoginView

app_name = 'users'
urlpatterns = [
    url(r'login/$', LoginView.as_view(), name='login'),

]