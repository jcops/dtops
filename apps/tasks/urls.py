from django.conf.urls import url


from  .views import CmdListView,GetKeyListView,KeyTestView,AccKeyView,KeyDelView,RunCmdView,HistoryView,DeployModelView
app_name = 'tasks'
urlpatterns = [
    #资产列表
    url(r'cmd_list/$', CmdListView.as_view(), name='cmd_list'),
    # key列表
    url(r'key_list/$', GetKeyListView.as_view(), name='key_list'),
    # key连接测试
    url(r'key_con/$', KeyTestView.as_view(), name='key_con'),
    # 授权认证节点
    url(r'key_accept/$', AccKeyView.as_view(), name='key_accept'),
    # 删除节点
    url(r'del_accept/$', KeyDelView.as_view(), name='del_accept'),
    # salt执行命令
    url(r'run_cmd/$', RunCmdView.as_view(), name='run_cmd'),
    # salt执行命令记录
    url(r'cmd_hist/$', HistoryView.as_view(), name='cmd_hist'),
    # 模块部署列表
    url(r'deploy_model/$', DeployModelView.as_view(), name='deploy_model'),

]