from django.conf.urls import url


from  .views import AssetListView,SystemUserListAllView,ProductLineListAllView

app_name = 'asset'
urlpatterns = [
    #资产列表
    url(r'asset_list/$', AssetListView.as_view(), name='asset_list'),
    #系统用户列表
    url(r'system_user/$', SystemUserListAllView.as_view(), name='system_user'),
    #产品线列表
    url(r'product_list/$', ProductLineListAllView.as_view(), name='product_list'),

]