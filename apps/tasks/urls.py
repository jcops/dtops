from django.conf.urls import url


from  .views import CmdListView
app_name = 'tasks'
urlpatterns = [
    #资产列表
    url(r'cmd_list/$', CmdListView.as_view(), name='cmd_list'),

]